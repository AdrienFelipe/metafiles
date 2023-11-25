from core.logger.logger_interface import IExecutionLogger


class NoLogger(IExecutionLogger):
    def log(self, _: str) -> None:
        return
