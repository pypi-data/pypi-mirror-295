import torch
from api_accuracy_checker.common.function_factory import npu_custom_functions


@npu_custom_functions
def npu_apply_adam_w(beta1_power, beta2_power, lr, weight_decay,
                     beta1, beta2, eps, grad, max_grad_norm, amsgrad, maximize, out):
    var, m, v = out
    if amsgrad:
        max_grad_norm = (torch.rand(var.shape) * 10.0 - 5.0).to(var.dtype)
    gt = -grad if maximize else grad
    m_out = m * beta1 - (beta1 + (-1)) * gt
    v_out = v * beta2 - (beta2 + (-1)) * gt * gt
    var_t = var * (1 + (-lr * weight_decay))
    beta1_power_out = beta1_power * beta1
    beta2_power_out = beta2_power * beta2
    if amsgrad:
        max_grad_norm_out = torch.max(max_grad_norm, v_out)
        if (1 - beta2_power_out) == 0:
            beta2_power_out -= eps
        denom = torch.sqrt(torch.div(max_grad_norm_out, (1 - beta2_power_out))) + eps
    else:
        vraintain = torch.div(v_out, (1 - beta2_power_out))
        denom = torch.sqrt(vraintain) + eps

    if (1 - beta1_power_out) == 0:
        beta1_power_out -= eps
    var_out = var_t + torch.div(-lr * m_out, (1 - beta1_power_out)).div(denom)
    return var_out.cpu(), m_out.cpu(), v_out.cpu()

