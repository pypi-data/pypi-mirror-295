# 进行比对及结果展示
import os
from collections import namedtuple

import torch
import numpy as np
from api_accuracy_checker.common.utils import get_json_contents, write_csv, print_info_log, Const
from api_accuracy_checker.compare.compare_utils import CompareConst, check_dtype_comparable, DETAIL_TEST_ROWS, \
    precision_configs, BENCHMARK_COMPARE_SUPPORT_LIST, AbsoluteStandardApi, BinaryStandardApi, ULPStandardApi, \
    ThousandthStandardApi, apis_threshold
from api_accuracy_checker.compare.compare_column import CompareColumn
from api_accuracy_checker.compare.algorithm import get_rmse, get_error_balance, get_max_rel_err, get_mean_rel_err, \
    get_rel_err, get_abs_err, get_max_abs_err, get_rel_err_ratio, cosine_sim, get_rel_err_origin, \
    get_small_value_err_ratio, get_finite_and_infinite_mask, get_small_value_mask, check_inf_nan_value, \
    check_small_value, check_norm_value, get_abs_bench_with_eps, get_ulp_err
from api_accuracy_checker.common.config import msCheckerConfig


ResultInfo = namedtuple('ResultInfo', ['full_api_name', 'fwd_success_status', 'bwd_success_status',
                                       'fwd_compare_alg_results', 'bwd_compare_alg_results', 'rank'])


class Comparator:
    # consts for result csv
    COLUMN_API_NAME = "API name"
    COLUMN_FORWARD_SUCCESS = "Forward Test Success"
    COLUMN_BACKWARD_SUCCESS = "Backward Test Success"
    COLUMN_STACK_INFO = "Traceback callstack info"

    def __init__(self, result_csv_path, details_csv_path, is_continue_run_ut, stack_info_json_path=None):
        self.save_path_str = result_csv_path
        self.detail_save_path_str = details_csv_path
        self.save_path_list = [result_csv_path]
        self.detail_save_path_list = [details_csv_path]
        if msCheckerConfig.is_online:
            self.save_path_str = result_csv_path.replace(".csv", "_rank{}.csv")
            self.detail_save_path_str = details_csv_path.replace(".csv", "_rank{}.csv")
            self.save_path_list = [self.save_path_str.format(rank) for rank in msCheckerConfig.rank_list]
            self.detail_save_path_list = [self.detail_save_path_str.format(rank) for rank in msCheckerConfig.rank_list]

        if not is_continue_run_ut:
            self.write_csv_title()
        if stack_info_json_path:
            self.stack_info = get_json_contents(stack_info_json_path)
        else:
            self.stack_info = None

    @staticmethod
    def get_path_from_rank(rank, path_list, path_pattern):
        return path_list[-1] if len(path_list) == 1 else path_pattern.format(rank)

    @staticmethod
    def print_pretest_result():
        print_info_log("Successfully completed run_ut/multi_run_ut.")

    def write_csv_title(self):
        summary_test_rows = [[self.COLUMN_API_NAME, self.COLUMN_FORWARD_SUCCESS, 
                              self.COLUMN_BACKWARD_SUCCESS, "Message"]]
        for save_path, detail_save_path in zip(self.save_path_list, self.detail_save_path_list):
            if not os.path.exists(save_path):
                write_csv(summary_test_rows, save_path)
            if not os.path.exists(detail_save_path):
                write_csv(DETAIL_TEST_ROWS, detail_save_path)

    def write_summary_csv(self, test_result):
        test_rows = []
        if self.stack_info:
            test_rows[0].append(self.COLUMN_STACK_INFO)

        name = test_result[0]
        df_row = list(test_result[:3])
        if test_result[1] == "SKIP":
            df_row.append(test_result[3][0][-1])
        if self.stack_info:
            stack_info = "\n".join(self.stack_info[name])
            df_row.append(stack_info)
        test_rows.append(df_row)
        save_path = self.get_path_from_rank(test_result[-1], self.save_path_list, self.save_path_str)
        write_csv(test_rows, save_path)

    def write_detail_csv(self, test_result):
        test_rows = []

        subject_prefix = test_result[0]
        fwd_result = test_result[3]
        bwd_result = test_result[4]
        if isinstance(fwd_result, list):
            for i, test_subject in enumerate(fwd_result):
                subject = subject_prefix + ".forward.output." + str(i)
                test_subject = ["{:.{}f}".format(item, msCheckerConfig.precision) 
                                if isinstance(item, float) else item for item in test_subject]
                test_rows.append([subject] + list(test_subject))
        if isinstance(bwd_result, list):
            for i, test_subject in enumerate(bwd_result):
                subject = subject_prefix + ".backward.output." + str(i)
                test_subject = ["{:.{}f}".format(item, msCheckerConfig.precision) 
                                if isinstance(item, float) else item for item in test_subject]
                test_rows.append([subject] + list(test_subject))

        detail_save_path = self.get_path_from_rank(test_result[-1],
                                                   self.detail_save_path_list,
                                                   self.detail_save_path_str)
        write_csv(test_rows, detail_save_path)

    def record_results(self, args):
        self.write_summary_csv(args)
        self.write_detail_csv(args)

    def compare_output(self, full_api_name, data_info):
        _, api_name, _ = full_api_name.split(Const.DELIMITER)
        bench_output, device_output = data_info.bench_output, data_info.device_output
        bench_grad, device_grad = data_info.bench_grad, data_info.device_grad
        backward_message = data_info.backward_message
        compare_func = self._compare_dropout if "dropout" in full_api_name else self._compare_core_wrapper
        # forward result compare
        fwd_success_status, fwd_compare_alg_results = compare_func(api_name, bench_output, device_output)
        # backward result compare
        if bench_grad is None or device_grad is None:
            bwd_success_status, bwd_compare_alg_results = (CompareConst.SPACE, [])
        else:
            if "dropout" in full_api_name:
                bwd_success_status, bwd_compare_alg_results = compare_func(api_name, bench_grad[0], device_grad[0])
            else:
                bwd_success_status, bwd_compare_alg_results = compare_func(api_name, bench_grad, device_grad)
        if backward_message:
            backward_column = CompareColumn()
            bwd_compare_alg_results = [backward_column.to_column_value(CompareConst.SKIP, backward_message)]
        else:
            bwd_success_status = bwd_success_status if bwd_compare_alg_results is not None else CompareConst.SPACE

        result_info = ResultInfo(full_api_name,
                                 fwd_success_status,
                                 bwd_success_status,
                                 fwd_compare_alg_results,
                                 bwd_compare_alg_results,
                                 data_info.rank)
        self.record_results(result_info)
        return fwd_success_status == CompareConst.PASS, bwd_success_status == CompareConst.PASS \
            or bwd_success_status == CompareConst.SPACE

    def _compare_core_wrapper(self, api_name, bench_output, device_output):
        detailed_result_total = []
        test_final_success = CompareConst.PASS
        if isinstance(bench_output, (list, tuple)):
            status, compare_result, message = [], [], []
            if len(bench_output) > len(device_output):
                status = [CompareConst.ERROR]
                message = ["bench and npu output structure is different."]
            else:
                device_output = device_output[:len(bench_output)]
                for b_out_i, n_out_i in zip(bench_output, device_output):
                    status_i, compare_result_i, message_i = self._compare_core(api_name, b_out_i, n_out_i)
                    status.append(status_i)
                    compare_result.append(compare_result_i)
                    message.append(message_i)
        else:
            status, compare_result, message = self._compare_core(api_name, bench_output, device_output)
        if not isinstance(status, list):
            detailed_result_total.append(compare_result.to_column_value(status, message))
            if status == CompareConst.ERROR:
                test_final_success = CompareConst.ERROR
            elif status == CompareConst.WARNING:
                test_final_success = CompareConst.WARNING
        else:
            for item, item_status in enumerate(status):
                detailed_result_total.append(compare_result[item].to_column_value(item_status, message[item]))
                if item_status == CompareConst.ERROR:
                    test_final_success = CompareConst.ERROR
                elif item_status == CompareConst.WARNING:
                    test_final_success = CompareConst.WARNING
        return test_final_success, detailed_result_total

    def _compare_core(self, api_name, bench_output, device_output):
        compare_column = CompareColumn()
        if not isinstance(bench_output, type(device_output)):
            return CompareConst.ERROR, compare_column, "bench and npu output type is different."
        elif isinstance(bench_output, dict):
            b_keys, n_keys = set(bench_output.keys()), set(device_output.keys())
            if b_keys != n_keys:
                return CompareConst.ERROR, compare_column, "bench and npu output dict keys are different."
            else:
                status, compare_result, message = self._compare_core(api_name, list(bench_output.values()), 
                                                                     list(device_output.values()))
        elif isinstance(bench_output, torch.Tensor):
            copy_bench_out = bench_output.detach().clone()
            copy_device_output = device_output.detach().clone()
            compare_column.bench_type = str(copy_bench_out.dtype)
            compare_column.npu_type = str(copy_device_output.dtype)
            compare_column.shape = tuple(device_output.shape)
            status, compare_result, message = self._compare_torch_tensor(api_name, copy_bench_out, copy_device_output,
                                                                compare_column)
        elif isinstance(bench_output, (bool, int, float, str)):
            compare_column.bench_type = str(type(bench_output))
            compare_column.npu_type = str(type(device_output))
            status, compare_result, message = self._compare_builtin_type(bench_output, device_output, compare_column)
        elif bench_output is None:
            return CompareConst.SKIP, compare_column, "Bench output is None, skip this test."
        else:
            return CompareConst.PASS, compare_column, 
        "Unexpected output type in compare_core: {}".format(type(bench_output))

        return status, compare_result, message

    def _compare_torch_tensor(self, api_name, bench_output, device_output, compare_column):
        cpu_shape = bench_output.shape
        npu_shape = device_output.shape
        npu_dtype = device_output.dtype
        if npu_dtype == torch.bfloat16:
            bench_output = bench_output.to(torch.float32)
            device_output = device_output.to(torch.float32)
        bench_output = bench_output.numpy()
        device_output = device_output.cpu().numpy()
        if cpu_shape != npu_shape:
            return CompareConst.ERROR, compare_column, f"The shape of bench{str(cpu_shape)} " \
                                                    f"and npu{str(npu_shape)} not equal."
        if not check_dtype_comparable(bench_output, device_output):
            return CompareConst.ERROR, compare_column, f"Bench out dtype is {bench_output.dtype} but " \
                                                    f"npu output dtype is {device_output.dtype}, cannot compare."
        message = ""
        if bench_output.dtype in [bool, np.uint8, np.int8, np.int16, np.uint16, np.uint32, np.int32, 
                                  np.int64, np.uint64]:
            message += f"Compare algorithm is not supported for {bench_output.dtype} data. " \
                    f"Only judged by Error Rate."
            err_rate, status, msg = self._compare_bool_tensor(bench_output, device_output)
            message += msg + "\n"
            compare_column.error_rate = err_rate
            return status, compare_column, message
        else:
            status, compare_column, message = self._compare_float_tensor(api_name, bench_output, device_output, 
                                                                         compare_column, npu_dtype)
            return status, compare_column, message
    
    def _compare_float_tensor(self, api_name, bench_output, device_output, compare_column, dtype):
        message = ""
        abs_bench, abs_bench_with_eps = get_abs_bench_with_eps(bench_output, dtype)
        abs_err = get_abs_err(bench_output, device_output)
        rel_err_orign = get_rel_err_origin(abs_err, abs_bench_with_eps)
        if api_name in ThousandthStandardApi:
            thousand_res, thousand_status = get_rel_err_ratio(rel_err_orign, 0.001)
            compare_column.rel_err_thousandth = thousand_res
        if str(dtype) in BENCHMARK_COMPARE_SUPPORT_LIST:
            both_finite_mask, inf_nan_mask = get_finite_and_infinite_mask(bench_output, device_output)
            if api_name in BinaryStandardApi:
                err_rate, _, _ = self._compare_bool_tensor(bench_output, device_output)
                compare_column.error_rate = err_rate
            elif api_name in AbsoluteStandardApi:
                small_value_threshold, small_value_atol, rtol = self._get_absolute_threshold_attribute(
                    api_name, str(dtype))
                rel_err = abs_err / abs_bench_with_eps
                small_value_mask = get_small_value_mask(abs_bench, both_finite_mask, small_value_threshold)
                normal_value_mask = np.logical_and(both_finite_mask, np.logical_not(small_value_mask))
                compare_column.inf_nan_error_ratio = check_inf_nan_value(inf_nan_mask, bench_output, device_output, dtype, rtol)
                compare_column.rel_err_ratio = check_norm_value(normal_value_mask, rel_err, rtol)
                compare_column.abs_err_ratio = check_small_value(abs_err, small_value_mask, small_value_atol)
            elif api_name in ULPStandardApi:
                if bench_output.size == 0:
                    compare_column.max_ulp_error = 0
                    compare_column.mean_ulp_error = 0
                    compare_column.ulp_error_proportion = 0
                else:
                    ulp_err = get_ulp_err(bench_output, device_output, dtype)
                    compare_column.max_ulp_error = np.max(ulp_err)
                    compare_column.mean_ulp_error = np.mean(ulp_err)
                    if dtype == torch.float32:
                        compare_column.ulp_error_proportion = np.sum(ulp_err > 32) / bench_output.size
                    else:
                        compare_column.ulp_error_proportion = np.sum(ulp_err > 1) / bench_output.size
            else:
                dtype_config = precision_configs.get(dtype)    
                small_value_mask = get_small_value_mask(abs_bench, both_finite_mask, dtype_config['small_value'][0])
                abs_err_greater_mask = np.greater(abs_err, dtype_config['small_value_atol'][0])
                compare_column.small_value_err_ratio = get_small_value_err_ratio(small_value_mask, abs_err_greater_mask)
                rel_err = get_rel_err(abs_err, abs_bench_with_eps, small_value_mask, inf_nan_mask)
                compare_column.RMSE = get_rmse(abs_err, np.logical_or(inf_nan_mask, small_value_mask))
                compare_column.EB = get_error_balance(bench_output, device_output)
                if rel_err.size == 0:
                    return CompareConst.ERROR, compare_column, "Relative error result list is empty."
                compare_column.Max_rel_error = get_max_rel_err(rel_err)
                compare_column.Mean_rel_error = get_mean_rel_err(rel_err)

        cos_res, cos_status, msg = cosine_sim(bench_output, device_output)
        compare_column.cosine_sim = cos_res
        message += msg + "\n"
        if not cos_status:
            message += "Cosine similarity is less than 0.99, consider as error, skip other check and set to SPACE.\n"
            return CompareConst.ERROR, compare_column, message

        max_abs_res, max_abs_status = get_max_abs_err(abs_err)
        compare_column.max_abs_err = max_abs_res
        if max_abs_status:
            message += "Max abs error is less than 0.001, consider as pass, skip other check and set to SPACE.\n"
            return CompareConst.PASS, compare_column, message

        if dtype in [torch.float16, torch.bfloat16]:
            hundred_res, hundred_status = get_rel_err_ratio(rel_err_orign, 0.01)
            compare_column.rel_err_hundredth = hundred_res
            if not hundred_status:
                message += "Relative error is greater than 0.01, consider as error, skip other check and set to SPACE.\n"
                return CompareConst.ERROR, compare_column, message
        thousand_res, thousand_status = get_rel_err_ratio(rel_err_orign, 0.001)
        compare_column.rel_err_thousandth = thousand_res
        if dtype in [torch.float16, torch.bfloat16]:
            if thousand_status:
                message += "Relative error is less than 0.001, consider as pass, skip other check and set to SPACE.\n"
                return CompareConst.PASS, compare_column, message
            message += "Relative error is greater than 0.001, consider as warning, skip other check and set to SPACE.\n"
            return CompareConst.WARNING, compare_column, message
        ten_thousand_res, ten_thousand_status = get_rel_err_ratio(rel_err_orign, 0.0001)
        compare_column.rel_err_ten_thousandth = ten_thousand_res
        if dtype in [torch.float32, torch.float64]:
            if not thousand_status:
                message += "Relative error is greater than 0.001, consider as error, skip other check and set to SPACE.\n"
                return CompareConst.ERROR, compare_column, message
            if not ten_thousand_status:
                message += "Relative error is greater than 0.0001, consider as warning, skip other check and set to SPACE.\n"
                return CompareConst.WARNING, compare_column, message
            message += "Relative error is less than 0.0001, consider as pass.\n"
        return CompareConst.PASS, compare_column, message

    @staticmethod
    def _compare_dropout(api_name, bench_output, device_output):
        tensor_num = bench_output.numel()
        if tensor_num >= 100:
            if abs((bench_output == 0).sum() - (device_output == 0).cpu().sum()) / tensor_num < 0.1:
                return CompareConst.PASS, 1
            else:
                return CompareConst.ERROR, 0
        else:
            return CompareConst.PASS, 1

    @staticmethod
    def _compare_builtin_type(bench_output, device_output, compare_column):
        if not isinstance(bench_output, (bool, int, float, str)):
            return CompareConst.PASS, compare_column, ""
        if bench_output != device_output:
            return CompareConst.ERROR, compare_column, ""
        compare_column.error_rate = 0
        return CompareConst.PASS, compare_column, ""


    @staticmethod
    def _compare_bool_tensor(bench_output, device_output):
        error_nums = (bench_output != device_output).sum()
        if bench_output.size == 0:
            return 0, CompareConst.PASS, ""
        error_rate = float(error_nums / bench_output.size)
        result = CompareConst.PASS if error_rate == 0 else CompareConst.ERROR
        return error_rate, result, ""
    
    @staticmethod
    def _get_absolute_threshold_attribute(api_name, dtype):
        small_value_threshold = apis_threshold.get(api_name).get(dtype).get('small_value')
        small_value_atol = apis_threshold.get(api_name).get(dtype).get('small_value_atol')
        rtol = apis_threshold.get(api_name).get(dtype).get('rtol')
        return small_value_threshold, small_value_atol, rtol
