from core.logger.logger_interface import IExecutionLogger


class FileLogger(IExecutionLogger):
    def __init__(self):
        self._filename = "execution.log"

    def log(self, message):
        with open(self._filename, "a") as file:
            file.write(message + "\n")
