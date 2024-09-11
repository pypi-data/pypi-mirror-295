import os

import torch

from grad_tool.common.base_comparator import BaseComparator
from grad_tool.common.utils import check_file_or_directory_path


class PtGradComparator(BaseComparator):

    @classmethod
    def _load_grad_files(cls, grad_file1: str, grad_file2: str):
        check_file_or_directory_path(grad_file1)
        check_file_or_directory_path(grad_file2)
        try:
            tensor1 = torch.load(grad_file1, map_location=torch.device("cpu"))
            tensor2 = torch.load(grad_file2, map_location=torch.device("cpu"))
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e} when loading tensor.") from e

        if tensor1.shape != tensor2.shape:
            raise RuntimeError(f"tensor shape is not equal: {grad_file1}, {grad_file2}")
        if tensor1.dtype != torch.bool:
            raise TypeError(f"tensor type is not bool: {grad_file1}")
        if tensor2.dtype != torch.bool:
            raise TypeError(f"tensor type is not bool: {grad_file2}")
        return tensor1.numpy(), tensor2.numpy()
