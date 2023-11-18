from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class QueryUserResponse(PromptResponse):
    def __init__(self, query: str):
        super().__init__(PromptStatus.COMPLETED, query)

    def query(self) -> str:
        return self.message


def query_user_callback(task: Task, query: str) -> QueryUserResponse:
    return QueryUserResponse(query)
