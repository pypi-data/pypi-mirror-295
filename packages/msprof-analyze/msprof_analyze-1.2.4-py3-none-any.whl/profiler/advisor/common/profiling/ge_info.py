"""
DB
"""
import logging
import os
from typing import Any, List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from profiler.advisor.dataset.profiling.db_manager import ConnectionManager
from profiler.advisor.dataset.profiling.profiling_parser import ProfilingParser
from profiler.advisor.utils.utils import check_path_valid

logger = logging.getLogger()


class GeInfo(ProfilingParser):
    """
    ge info file
    """
    FILE_PATTERN_MSG = "ge_info.db"
    FILE_INFO = "ge info"
    STATIC_OP_STATE = "0"
    DYNAMIC_OP_STATE = "1"

    file_pattern_list = [r"ge_info.db"]

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.op_state_info_list = None

    def parse_from_file(self, profiling_db_file):
        """
        ge info
        """
        db_path, db_file = os.path.split(profiling_db_file)
        check_path_valid(db_path)
        if not ConnectionManager.check_db_exists(db_path, [db_file]):
            return False
        try:
            conn = ConnectionManager(db_path, db_file)
        except SQLAlchemyError as e:
            logger.error("Database error: %s", e)
            return False
        if conn.check_table_exists(['TaskInfo']):
            with conn().connect() as sql_conn:
                self.op_state_info_list = sql_conn.execute(text("select op_name, op_state from TaskInfo")).fetchall()
        return True

    def get_static_shape_operators(self) -> List[Any]:
        return [op for op, state in self.op_state_info_list if state == self.STATIC_OP_STATE]

    def get_dynamic_shape_operators(self) -> List[Any]:
        return [op for op, state in self.op_state_info_list if state == self.DYNAMIC_OP_STATE]
