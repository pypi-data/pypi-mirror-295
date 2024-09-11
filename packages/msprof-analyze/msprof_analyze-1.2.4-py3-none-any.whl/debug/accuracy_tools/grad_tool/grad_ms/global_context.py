import os
import threading
from typing import Dict, List, Union

from grad_tool.common.utils import print_warn_log
from grad_tool.common.constant import GradConst
from grad_tool.common.utils import path_valid_check, create_directory, check_str


class GlobalContext:

    _instance = None
    _instance_lock = threading.Lock()
    _setting = {
        GradConst.LEVEL: None,
        GradConst.PARAM_LIST: None,
        GradConst.STEP: None,
        GradConst.RANK: None,
        GradConst.CURRENT_STEP: 0,
        GradConst.BOUNDS: [-10, -1, -0.1, -0.01, -0.001, 0, 0.001, 0.01, 0.1, 1, 10],
        GradConst.OUTPUT_PATH: None
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance_lock.acquire()
            cls._instance = object.__new__(cls)
            cls._instance_lock.release()
        return cls._instance

    def init_context(self, config_dict: Dict):
        level = config_dict.get(GradConst.LEVEL)
        check_str(level, variable_name = "level in yaml")
        if level in GradConst.SUPPORTED_LEVEL:
            self._setting[GradConst.LEVEL] = config_dict.get(GradConst.LEVEL)
        else:
            raise ValueError("Invalid level set in config yaml file, level option: L0, L1, L2")

        self._set_input_list(config_dict, GradConst.PARAM_LIST, str)
        self._set_input_list(config_dict, GradConst.BOUNDS, float)
        self._set_input_list(config_dict, GradConst.STEP, int)
        self._set_input_list(config_dict, GradConst.RANK, int)

        output_path = config_dict.get(GradConst.OUTPUT_PATH)
        check_str(output_path, variable_name = "output_path in yaml")
        try:
            path_valid_check(output_path)
        except RuntimeError as err:
            raise ValueError(f"Invalid output_path: {output_path}. The error message is {err}.") from err
        self._setting[GradConst.OUTPUT_PATH] = output_path
        if not os.path.isdir(self._setting.get(GradConst.OUTPUT_PATH)):
            create_directory(self._setting.get(GradConst.OUTPUT_PATH))
        else:
            print_warn_log("The output_path exists, the data will be covered.")

    def get_context(self, key: str):
        if key not in self._setting:
            print_warn_log(f"Unrecognized {key}.")
        return self._setting.get(key)

    def update_step(self):
        self._setting[GradConst.CURRENT_STEP] += 1

    def step_need_dump(self, step):
        dump_step_list = self.get_context(GradConst.STEP)
        return (not dump_step_list) or (step in dump_step_list)

    def rank_need_dump(self, rank):
        dump_rank_list = self.get_context(GradConst.RANK)
        return (not dump_rank_list) or (rank in dump_rank_list)

    def _set_input_list(self, config_dict: Dict, name: str, dtype: Union[int, str, float]):
        value = config_dict.get(name)
        if dtype == int:
            type_str = "integer"
        elif dtype == float:
            type_str = "float"
        else:
            type_str = "string"
        if value and isinstance(value, list):
            for val in value:
                if not isinstance(val, dtype):
                    print_warn_log(f"Invalid {name} which must be None or list of {type_str}")
                    return
            self._setting[name] = value
        else:
            print_warn_log(f"{name} is None or not a list with valid items, use default value.")

grad_context = GlobalContext()
