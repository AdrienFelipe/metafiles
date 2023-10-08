from action import Action
from action_result import ActionResult
from agent_proxy import AgentProxy
from registry import action_registry
from task import Task
from task_execute import execute_task


class DivideTask(Action):
    description = "Subdivide the task into smaller tasks"

    def execute(self, task: Task, agent_proxy: AgentProxy, reason: str) -> ActionResult:
        # Prompt which agents would best know about the task to know what to do
        roles = agent_proxy.ask_for_agent_roles(task)

        # For each agent role
        # TODO: limit the amount of iterations
        while True:
            initial_plan = task.plan
            for role in roles:
                # Prompt acting like agent to list first level of sub tasks to divide or refine it
                plan = agent_proxy.ask_to_create_plan(task, role)
                # TODO: validate plan is valid
                task.plan = plan

            if task.plan == initial_plan:
                break
        # TODO: Validate the answer is what was expected

        # Apply sub-tasks
        for sub_goal in task.plan:
            sub_requirements = agent_proxy.ask_to_filter_requirements(task, sub_goal)
            sub_task = Task(sub_goal, sub_requirements, task)
            execute_task(sub_task, agent_proxy)


action_registry.register_action("divide_task", DivideTask)
