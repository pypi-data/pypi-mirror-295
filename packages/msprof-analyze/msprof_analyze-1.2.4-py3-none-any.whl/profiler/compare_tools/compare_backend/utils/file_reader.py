import csv
import json
import os

from common_func.path_manager import PathManager
from compare_backend.utils.constant import Constant


class FileReader:
    @classmethod
    def read_trace_file(cls, file_path: str) -> any:
        PathManager.check_path_readable(file_path)
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not exists.")
        file_size = os.path.getsize(file_path)
        if file_size <= 0:
            return []
        if file_size > Constant.MAX_FILE_SIZE:
            check_msg = input(
                f"The file({file_path}) size exceeds the preset max value. Continue reading the file? [y/n]")
            if check_msg.lower() != "y":
                print(f"[WARNING] The user choose not to read the file: {file_path}")
                return []
        try:
            with open(file_path, "rt") as file:
                json_data = json.loads(file.read())
        except Exception as e:
            msg = f"Can't read file: {file_path}"
            raise RuntimeError(msg) from e
        return json_data

    @classmethod
    def read_csv_file(cls, file_path: str, bean_class: any = None) -> any:
        PathManager.check_path_readable(file_path)
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not exists.")
        file_size = os.path.getsize(file_path)
        if file_size <= 0:
            return []
        if file_size > Constant.MAX_FILE_SIZE:
            check_msg = input(
                f"The file({file_path}) size exceeds the preset max value. Continue reading the file? [y/n]")
            if check_msg.lower() != "y":
                print(f"[WARNING] The user choose not to read the file: {file_path}")
                return []
        result_data = []
        try:
            with open(file_path, newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    row_data = bean_class(row) if bean_class else row
                    result_data.append(row_data)
        except Exception as e:
            msg = f"Failed to read the file: {file_path}"
            raise RuntimeError(msg) from e
        return result_data

    @classmethod
    def check_json_type(cls, file_path: str) -> str:
        json_data = cls.read_trace_file(file_path)
        if isinstance(json_data, dict):
            return Constant.GPU
        return Constant.NPU
