from action import Action
from action_result import ActionResult
from agent_proxy import AgentProxy
from openai_chat import OpenAIChat
from registry import action_registry
from task import Task


class DivideTask(Action):
    description = "Subdivide the task into smaller tasks"

    def execute(self, task: Task, reason: str) -> ActionResult:
        agent_proxy = AgentProxy(OpenAIChat())

        # Prompt which agents would best know about the task to know what to do
        roles = agent_proxy.ask_for_agent_roles(task)

        # For each agent role
        while True:
            initial_plan = task.plan
            for role in roles:
                # Prompt acting like agent to list first level of sub tasks to divide or refine it
                plan = agent_proxy.ask_to_create_plan(task, role)
                # validate plan is valid
                task.plan = plan

            if task.plan == initial_plan:
                break
        # Validate the answer is what was expected
        # Update task with plan


action_registry.register_action("divide_task", DivideTask)
