from action.action import Action, ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task import Task
from task_execute import execute_task


class DivideTask(Action):
    description = "Subdivide the task into smaller tasks"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        agent_proxy = AgentProxy(agent)

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
        # TODO: should it be able to update the whole plan?

        # Apply sub-tasks
        for sub_goal in task.plan:
            sub_requirements = agent_proxy.ask_to_filter_requirements(task, sub_goal)
            sub_task = Task(sub_goal, sub_requirements, task)
            sub_result = execute_task(agent, sub_task)
            # TODO: check sub result and advise what to do next <---------

        # TODO: this should check the sub results
        return ActionResult(ActionResultStatus.SUCCESS, "Task was divided")


action_registry.register_action(ActionName.DIVIDE_TASK, DivideTask)