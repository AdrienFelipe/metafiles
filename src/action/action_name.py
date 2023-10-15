from enum import Enum


class ActionName(Enum):
    ASK_AGENT = "ask_agent"
    ASK_USER = "ask_user"
    RUN_CODE = "run_code"
    DIVIDE_TASK = "divide_task"
