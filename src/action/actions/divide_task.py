from action.action import Action
from action.action_name import ActionName
from action.action_result import ActionResult
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task.task import Task


class DivideTask(Action):
    action_name = ActionName.DIVIDE_TASK
    description = (
        "Break down the task into smaller, manageable parts. Use this for complex tasks "
        "that benefit from being broken down to ensure clarity and completeness."
    )

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        agent_proxy = AgentProxy(self._container, agent)

        # Prompt which roles and skills the agent should have
        roles = agent_proxy.ask_for_agent_roles(task).get_roles()
        # TODO: what happens if roles is empty?
        task.plan = agent_proxy.ask_to_create_plan(task, roles, reason).get_plan()

        # TODO: Validate the answer is what was expected
        # TODO: should it be able to update the whole plan?

        # Apply sub-tasks
        for step in task.plan:
            sub_task = Task.from_plan_step(step, task)
            self._task_handler.execute(agent, sub_task)
            # TODO: check sub result and advise what to do next <---------

        # TODO: this should check the sub results
        # TODO: update prompt and rest of code as division result comes from last task
        return sub_task.result
