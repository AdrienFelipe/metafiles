from typing import Dict, Optional

from core.logger.logger_interface import IExecutionLogger


class NoLogger(IExecutionLogger):
    def log(self, _: str, __: Optional[Dict] = None) -> None:
        return
