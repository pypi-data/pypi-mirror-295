import torch
import numpy as np
from einops import rearrange

from api_accuracy_checker.common.function_factory import npu_custom_functions, npu_custom_grad_functions
from api_accuracy_checker.common.utils import logger

gtype = torch.float64  # arm host必须选择float64，x86环境选择float32即可，64也行。arm计算很慢，s=8k的场景建议使用x86
softmax_build_mode = "QKV"  # "MAX_SUM"

"""
# 前向函数声明对比
标杆实现:fusion_attention_forward: q, k, v, drop_mask, atten_mask, pse, scale, keep_prob
融合算子:npu_fusion_attention_forward: query, key, value, head_num, input_layout, *, pse=None, padding_mask=None,
                                      atten_mask=None, scale=1.0, keep_prob=1.0, pre_tockens=2147483647,
                                      next_tockens=2147483647, inner_precise=0, prefix=None, sparse_mode=0,
                                      gen_mask_parallel=True, sync=False

# 反向函数声明对比
标杆实现:fusion_attention_backward: dx, q, k, v, softmax_res, drop_mask, pse, scale, keep_prob
融合算子:npu_fusion_attention_backward: query, key, value, dy, head_num, input_layout, *, pse=None, padding_mask=None,
                                       atten_mask=None, softmax_max=None, softmax_sum=None, softmax_in=None,
                                       attention_in=None, scale_value=1.0, keep_prob=1.0, pre_tockens=2147483647,
                                       next_tockens=2147483647, inner_precise=0, seed=0, offset=0,
                                       numels=0, prefix=None, sparse_mode=0, gen_mask_parallel=True, sync=False
"""


def softmax_forward(x):
    x_max = torch.max(x, dim=-1, keepdims=True)[0]
    x_sub = x.sub(x_max)
    y = torch.exp(x_sub)
    x_sum = y.sum(dim=-1, keepdims=True)
    res = y.div(x_sum)
    return res, x_max, x_sum


def softmax_grad(dp, softmax_res):
    muls = dp * softmax_res
    muls_r = muls.sum(dim=-1, keepdims=True)
    sub_r = dp - muls_r
    res = sub_r * softmax_res
    return res


def broadcast_kv(num_heads, num_kv_heads, kv_tensor, dtype):
    if num_kv_heads == 0 or num_kv_heads < num_heads:
        raise ValueError(f"num_kv_heads must be non-zero and less than num_heads.")

    factor = num_heads // num_kv_heads
    kv_shape = kv_tensor.shape
    B = kv_shape[0]
    S = kv_shape[2]
    D = kv_shape[3]
    kv_res = torch.zeros([B, num_heads, S, D]).to(dtype)
    for i in range(num_heads):
        j = i // factor
        kv_res[:, i:i + 1, :, :] = kv_tensor[:, j:j + 1, :, :]
    return kv_res


def calculate_qk(q, k, atten_mask, pse, scale):
    if pse is None or len(pse.shape) == 0:
        qk = torch.matmul(q, k.permute(0, 1, 3, 2)).mul(scale)
    else:
        qk = (torch.matmul(q, k.permute(0, 1, 3, 2)) + pse).mul(scale)
    if atten_mask is None or len(atten_mask.shape) == 0:
        return qk
    else:
        qk = qk + atten_mask.bool() * (-40000.0)  # -10000
    return qk


def fusion_attention_forward(q, k, v, drop_mask, atten_mask, pse, scale, keep_prob):
    qk = calculate_qk(q, k, atten_mask, pse, scale)
    softmax_res, softmax_max, softmax_sum = softmax_forward(qk)
    if drop_mask is None or len(drop_mask.shape) == 0:
        drop_res = softmax_res
    else:
        drop_res = softmax_res * drop_mask * (1.0 / keep_prob)
    y = torch.matmul(drop_res, v)
    return y, softmax_max, softmax_sum


def fusion_attention_backward(dx, q, k, v, softmax_res, drop_mask, pse, scale, keep_prob):
    dp = torch.matmul(dx, v.permute(0, 1, 3, 2))
    if drop_mask is None or len(drop_mask.shape) == 0:
        drop_res = softmax_res.permute(0, 1, 3, 2)
        dp_drop = dp
    else:
        drop_res = softmax_res.mul(drop_mask).mul(1.0 / keep_prob).permute(0, 1, 3, 2)
        dp_drop = dp * drop_mask * (1.0 / keep_prob)
    dv = torch.matmul(drop_res, dx)
    softmax_grad_res = (softmax_grad(dp_drop, softmax_res) * scale)
    dq = torch.matmul(softmax_grad_res, k)
    dk = torch.matmul(softmax_grad_res.permute(0, 1, 3, 2), q)
    return dq, dk, dv


def parse_bsnd_args(query, key, head_num, input_layout):
    supported_input_layout = ["BSH", "SBH", "BSND", "BNSD", "TND"]
    B, S1, S2, N1, N2, D, H1, H2 = None, None, None, head_num, None, None, None, None

    if not isinstance(input_layout, str) or input_layout not in supported_input_layout:
        raise ValueError(f"Invalid input_layout arg which must be one of {supported_input_layout}.")

    if input_layout == "TND":
        raise ValueError(f"input_layout {input_layout} does not supported for now.")
    try:
        if input_layout == "BSH":
            B, S1, H1 = query.shape
            _, S2, H2 = key.shape
            D = H1 // N1
            N2 = H2 // D
        elif input_layout == "SBH":
            S1, B, H1 = query.shape
            S2, _, H2 = key.shape
            D = H1 // N1
            N2 = H2 // D
        elif input_layout == "BSND":
            B, S1, N1, D = query.shape
            _, S2, N2, _ = key.shape
            H1 = N1 * D
            H2 = N2 * D
        elif input_layout == "BNSD":
            B, N1, S1, D = query.shape
            _, N2, S2, _ = key.shape
            H1 = N1 * D
            H2 = N2 * D
    except Exception as e:
        raise ValueError(f"query.shape: {query.shape}, key.shape: {key.shape}, parse_bsnd_args error: {e}") from e

    if D == 0:
        raise ValueError(f"Value D must be non-zero.")
    DTYPE = query.dtype
    return B, S1, S2, N1, N2, D, H1, H2, DTYPE


def convert_from_bnsd(_input, input_layout):
    if input_layout == "BSH":
        # (B,N,S,D)=>(B,S,N*D)
        out = rearrange(_input, 'b n s d -> b s (n d)').contiguous()
    elif input_layout == "SBH":
        # (B,N,S,D)=>(S,B,N*D)
        out = rearrange(_input, 'b n s d -> s b (n d)').contiguous()
    elif input_layout == "BSND":
        # (B,N,S,D)=>(B,S,N,D)
        out = rearrange(_input, 'b n s d -> b s n d').contiguous()
    elif input_layout == "TND":
        raise ValueError(f"input_layout {input_layout} does not supported for now.")
    else:
        out = _input
    return out


def convert_to_bnsd(_input, n, input_layout):
    # 默认"BNSD"无需处理
    if input_layout == "BSH":
        # (B,S,N*D)=>(B,N,S,D)
        out = rearrange(_input, 'b s (n d) -> b n s d', n=n)
    elif input_layout == "SBH":
        # (S,B,N*D)=>(B,N,S,D)
        out = rearrange(_input, 's b (n d) -> b n s d', n=n)
    elif input_layout == "BSND":
        # (B,S,N,D)=>(B,N,S,D)
        out = rearrange(_input, 'b s n d -> b n s d', n=n)
    elif input_layout == "TND":
        raise ValueError(f"input_layout {input_layout} does not supported for now.")
    else:
        out = _input
    if out.dim() != 4:
        raise ValueError(f"convert qkv format failed with input_layout {input_layout}.")
    return out.to(gtype)


def generate_atten_mask(sparse_mode, atten_mask, B, N1, S1, S2, pre_tocken, next_tocken, dtype):
    """
    # 当sparse_mode=2、3、4时小算子到融合算子会走这个优化，反过来看就要拆解回原来的基本实现
    ===> atten_mask = torch.from_numpy(np.triu(np.ones([2048, 2048]), k=1)).to(dtype)
    """
    shape = [S1, S2]

    if atten_mask is not None:
        # 当FA的输入已经包含atten_mask时，可以认为已经是转换之后的mask矩阵了，有三种特殊场景，即稀疏矩阵场景，需要进行逆向还原
        if sparse_mode == 2 or sparse_mode == 3 or sparse_mode == 4:
            print(S1, S2, atten_mask.shape, atten_mask.dtype)

            if atten_mask.dim() == 2 and atten_mask.shape[0] == 2048 and atten_mask.shape[1] == 2048:
                if atten_mask.equal(torch.from_numpy(np.triu(np.ones([2048, 2048]), k=1)).to(atten_mask.dtype)):
                    if sparse_mode == 2:
                        atten_mask = torch.from_numpy(np.triu(np.ones(shape), k=1))
                    elif sparse_mode == 3:
                        atten_mask = torch.from_numpy(np.triu(np.ones(shape), k=S2 - S1 + 1))
                    elif sparse_mode == 4:
                        atten_mask_u = torch.from_numpy(np.triu(np.ones(shape), k=next_tocken + 1))
                        atten_mask_l = torch.from_numpy(np.tril(np.ones(shape), k=-pre_tocken - 1))
                        atten_mask = atten_mask_u + atten_mask_l
                    logger.debug(f"反向转换atten_mask {atten_mask.shape}")
                    return atten_mask.to(dtype)

        return atten_mask.to(dtype)

    if atten_mask is not None:
        if atten_mask.dim() == 2:
            if atten_mask.shape[0] != S1 or atten_mask.shape[1] != S2:
                raise ValueError(f"Invalid atten_mask shape `SS` {atten_mask.shape}")
            shape = [S1, S2]
        elif atten_mask.dim() == 4:
            if atten_mask.shape[1] == 1:
                shape = [B, 1, S1, S2] if B != 1 else [1, 1, S1, S2]
            else:
                shape = [B, N1, S1, S2] if B != 1 else [1, N1, S1, S2]

    if sparse_mode == 0:
        atten_mask_u = torch.from_numpy(np.triu(np.ones(shape), k=next_tocken + 1))
        atten_mask_l = torch.from_numpy(np.tril(np.ones(shape), k=-pre_tocken - 1))
        atten_mask = atten_mask_u + atten_mask_l
    elif sparse_mode == 1:  # no sparse
        atten_mask = torch.from_numpy(np.zeros(shape))
    elif sparse_mode == 2:
        atten_mask = torch.from_numpy(np.triu(np.ones(shape), k=1))
    elif sparse_mode == 3:
        atten_mask = torch.from_numpy(np.triu(np.ones(shape), k=S2 - S1 + 1))
    elif sparse_mode == 4:
        atten_mask_u = torch.from_numpy(np.triu(np.ones(shape), k=next_tocken + 1))
        atten_mask_l = torch.from_numpy(np.tril(np.ones(shape), k=-pre_tocken - 1))
        atten_mask = atten_mask_u + atten_mask_l
    # 注:不会出现sparse_mode=5的情况，该情况要求必须要传入atten_mask，且atten_mask矩阵数据格式须为BNSS或B1SS，
    # 因此可以认为FA的输入已经是正确的atten_mask了
    return atten_mask.to(dtype)


def generate_kv(key, value, N1, N2):
    # N不等长适配by cdy
    if not (N1 == N2):
        k_new = broadcast_kv(N1, N2, key, key.dtype)
        v_new = broadcast_kv(N1, N2, value, value.dtype)
    else:
        k_new = key
        v_new = value
    return k_new, v_new


def rebuid_softmax_by_qkv(q, k, atten_mask, pse, scale):
    """
    attention = softmax(QK^T/sqrt(d))V
    softmax(x_i) = e^(x_i - x_max) / sum(e^(x_i - x_max))
    """
    print(f"Using QKV to rebuild original softmax")
    qk = calculate_qk(q, k, atten_mask, pse, scale)
    softmax_res, x_max, x_sum = softmax_forward(qk)
    return softmax_res


def rebuild_softmax_by_max_sum(q, k, atten_mask, pse, scale, softmax_max, softmax_sum):
    """
    attention = softmax(QK^T/sqrt(d))V
    softmax(x_i) = e^(x_i - x_max_i) / x_sum_i)
    """
    print(f"Using softmax_max and softmax_sum to rebuild original softmax")
    qk = calculate_qk(q, k, atten_mask, pse, scale)
    if softmax_max.shape[-1] == 0:
        raise ValueError(f"softmax_max.shape[-1] must be non-zero, softmax_max.shape: {softmax_max.shape}")
    repeat_dim = qk.shape[-1] // softmax_max.shape[-1]
    softmax_res = torch.exp(qk.sub(softmax_max.repeat(1, 1, 1, repeat_dim))).div(
        softmax_sum.repeat(1, 1, 1, repeat_dim))
    return softmax_res


def npu_fusion_attention_forward_patch(*args, **kwargs):
    # query, key, value, head_num, input_layout
    if len(args) != 5:
        raise ValueError(f"Unsupported npu_fusion_attention args {args}.")

    B, S1, S2, N1, N2, D, H1, H2, DTYPE = parse_bsnd_args(args[0], args[1], args[3], args[4])
    if N1 == N2 and S1 == S2:
        logger.debug(f"running case : BNSD = {B}_{N1}_{S1}_{D}, sparse = {kwargs.get('sparse_mode', 0)}")
    else:
        logger.debug(f"running case: BNSD = {B}_{N1}({N2})_{S1}({S2})_{D}, sparse = {kwargs.get('sparse_mode', 0)}")
    if not (N1 % N2 == 0 and N1 >= N2):
        raise ValueError(f"N1与N2不匹配,请检查: N1 = {N1}, N2 = {N2}.")

    dims_kwargs = {"B": B, "S1": S1, "S2": S2, "N1": N1, "N2": N2,
                   "D": D, "H1": H1, "H2": H2, "DTYPE": DTYPE}

    new_kwargs = {"keep_prob": 1,
                  "scale": kwargs.get("scale", 1 / (D ** 0.5)),
                  "sparse_mode": kwargs.get("sparse_mode", 0),
                  "prefix": kwargs.get("prefix"),
                  "pre_tockens": kwargs.get("pre_tockens", 2147483647),
                  "next_tockens": kwargs.get("next_tockens", 2147483647),
                  "pse": kwargs.get("pse"),
                  "padding_mask": kwargs.get("padding_mask"),
                  "atten_mask": kwargs.get("atten_mask")}

    return args, dims_kwargs, new_kwargs


def npu_fusion_attention_backward_patch(*args, **kwargs):
    if len(args) != 6:
        raise ValueError(f"Unsupported npu_fusion_attention_grad args {args}.")

    B, S1, S2, N1, N2, D, H1, H2, DTYPE = parse_bsnd_args(args[0], args[1], args[4], args[5])
    if N1 == N2 and S1 == S2:
        print(f"running case : BNSD = {B}_{N1}_{S1}_{D}, sparse = {kwargs.get('sparse_mode', 0)}")
    else:
        print(f"running case: BNSD = {B}_{N1}({N2})_{S1}({S2})_{D}, sparse = {kwargs.get('sparse_mode', 0)}")
    if not (N1 % N2 == 0 and N1 >= N2):
        raise ValueError(f"N1与N2不匹配,请检查: N1 = {N1}, N2 = {N2}.")

    dims_kwargs = {"B": B, "S1": S1, "S2": S2, "N1": N1, "N2": N2,
                   "D": D, "H1": H1, "H2": H2, "DTYPE": DTYPE}

    new_kwargs = {"keep_prob": 1,
                  "scale_value": kwargs.get("scale_value", 1 / (D ** 0.5)),
                  "sparse_mode": kwargs.get("sparse_mode", 0),
                  "prefix": kwargs.get("prefix"),
                  "pre_tockens": kwargs.get("pre_tockens", 2147483647),
                  "next_tockens": kwargs.get("next_tockens", 2147483647),
                  "pse": kwargs.get("pse"),
                  "padding_mask": kwargs.get("padding_mask"),
                  "softmax_max": kwargs.get("softmax_max"),
                  "softmax_sum": kwargs.get("softmax_sum"),
                  "softmax_in": kwargs.get("softmax_in"),
                  "attention_in": kwargs.get("attention_in"),
                  "seed": kwargs.get("seed", 0),
                  "offset": kwargs.get("offset", 0),
                  "numels": kwargs.get("numels", 0),
                  "atten_mask": kwargs.get("atten_mask")}

    return args, dims_kwargs, new_kwargs


@npu_custom_functions
def npu_fusion_attention(*args, **kwargs):
    new_args, dims_kwargs, new_kwargs = npu_fusion_attention_forward_patch(*args, **kwargs)
    query, key, value, input_layout = new_args[0], new_args[1], new_args[2], new_args[4]
    N1 = dims_kwargs.get("N1")
    N2 = dims_kwargs.get("N2")
    S1 = dims_kwargs.get("S1")
    S2 = dims_kwargs.get("S2")
    B = dims_kwargs.get("B")
    DTYPE = dims_kwargs.get("DTYPE")
    atten_mask = new_kwargs.get("atten_mask")
    keep_prob = new_kwargs.get("keep_prob")
    sparse_mode = new_kwargs.get("sparse_mode")
    pre_tockens = new_kwargs.get("pre_tockens")
    next_tockens = new_kwargs.get("next_tockens")
    pse = new_kwargs.get("pse")
    scale = new_kwargs.get("scale")

    atten_mask = generate_atten_mask(sparse_mode, atten_mask, B, N1, S1, S2, pre_tockens, next_tockens, DTYPE)
    query = convert_to_bnsd(query, N1, input_layout)
    key = convert_to_bnsd(key, N2, input_layout)
    value = convert_to_bnsd(value, N2, input_layout)
    k_new, v_new = generate_kv(key, value, N1, N2)
    out_golden, softmax_max, softmax_sum = fusion_attention_forward(q=query, k=k_new, v=v_new,
                                                                    drop_mask=None, atten_mask=atten_mask,
                                                                    pse=pse, scale=scale,
                                                                    keep_prob=keep_prob)
    if out_golden.dim() == 5:
        out_golden = out_golden.reshape(out_golden.size(0), out_golden.size(1) * out_golden.size(2), out_golden.size(3),
                                        out_golden.size(4))
    out_golden = convert_from_bnsd(out_golden, input_layout)

    return out_golden.cpu(), softmax_max.repeat(1, 1, 1, 8).cpu(), softmax_sum.repeat(1, 1, 1, 8).cpu()


@npu_custom_grad_functions
def npu_fusion_attention_grad(*args, **kwargs):
    # dx, q, k, v, softmax_res, drop_mask, pse, scale, keep_prob
    new_args, dims_kwargs, new_kwargs = npu_fusion_attention_backward_patch(*args, **kwargs)
    query, key, value, dx, input_layout = new_args[0], new_args[1], new_args[2], new_args[3], new_args[5]
    N1 = dims_kwargs.get("N1")
    N2 = dims_kwargs.get("N2")
    S1 = dims_kwargs.get("S1")
    S2 = dims_kwargs.get("S2")
    B = dims_kwargs.get("B")
    D = dims_kwargs.get("D")
    DTYPE = dims_kwargs.get("DTYPE")
    atten_mask = new_kwargs.get("atten_mask")
    keep_prob = new_kwargs.get("keep_prob")
    sparse_mode = new_kwargs.get("sparse_mode")
    pre_tockens = new_kwargs.get("pre_tockens")
    next_tockens = new_kwargs.get("next_tockens")
    pse = new_kwargs.get("pse")
    softmax_max = new_kwargs.get("softmax_max")
    softmax_sum = new_kwargs.get("softmax_sum")
    scale_value = new_kwargs.get("scale_value")

    atten_mask = generate_atten_mask(sparse_mode, atten_mask, B, N1, S1, S2, pre_tockens, next_tockens, DTYPE)
    query = convert_to_bnsd(query, N1, input_layout)
    dx = convert_to_bnsd(dx, N1, input_layout)
    key = convert_to_bnsd(key, N2, input_layout)
    value = convert_to_bnsd(value, N2, input_layout)
    k_new, v_new = generate_kv(key, value, N1, N2)

    if softmax_build_mode == "QKV":
        softmax_res = rebuid_softmax_by_qkv(query, k_new, atten_mask, pse, scale_value)
    else:
        softmax_res = rebuild_softmax_by_max_sum(query, k_new, atten_mask, pse, scale_value, softmax_max, softmax_sum)

    dq, dk, dv = fusion_attention_backward(dx, query, k_new, v_new, softmax_res, None, pse, scale_value, keep_prob)

    # N不等长适配by cdy
    if not (N1 == N2):
        if N2 == 0:
            raise ValueError("dims_kwargs.N2 must be non-zero.")
        G = int(N1 / N2)
        dk = torch.sum(dk.reshape(B, N2, G, S2, D), dim=2, keepdim=True).reshape(B, N2, S2, D)
        dv = torch.sum(dv.reshape(B, N2, G, S2, D), dim=2, keepdim=True).reshape(B, N2, S2, D)

    if dq.dim() == 5:
        dq = dq.reshape(dq.size(0), dq.size(1) * dq.size(2), dq.size(3), dq.size(4))
    if dk.dim() == 5:
        dk = dk.reshape(dk.size(0), dk.size(1) * dk.size(2), dk.size(3), dk.size(4))
    if dv.dim() == 5:
        dv = dv.reshape(dv.size(0), dv.size(1) * dv.size(2), dv.size(3), dv.size(4))

    dq = convert_from_bnsd(dq, input_layout)
    dk = convert_from_bnsd(dk, input_layout)
    dv = convert_from_bnsd(dv, input_layout)

    return dq.cpu(), dk.cpu(), dv.cpu()
