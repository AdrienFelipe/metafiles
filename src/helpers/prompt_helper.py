from typing import Optional

from agent.agents.fake_agent import FakeAgent
from prompt.prompt import Prompt
from prompt.prompt_result import PromptCallbackResponse


def prompt_function_to_callback_arguments(func: dict, specials: Optional[dict] = None) -> dict:
    test_values_map = {
        "string": "test_string",
        "number": 123,
        "boolean": True,
        "array": [],
        "object": {},
    }

    test_values = {}

    for param_name, details in func["parameters"]["properties"].items():
        param_type = details["type"]

        if specials is not None and param_name in specials:
            test_value = specials[param_name]
        elif "enum" in details:
            test_value = details["enum"][0]
        elif "description" in details and "json" in details["description"].lower():
            test_value = '{"key": "value"}'
        else:
            test_value = test_values_map.get(param_type, "UnknownType")

        test_values[param_name] = test_value

    return test_values


def get_callback_response(
    prompt: Prompt, function_name: str, specials: Optional[dict] = None
) -> PromptCallbackResponse:
    functions = prompt.functions()

    if functions is not None:
        for function in functions:
            if function["name"] == function_name:
                arguments = prompt_function_to_callback_arguments(function, specials)
                return PromptCallbackResponse(function_name, arguments)

    raise ValueError(f"No function definition found for {function_name}")


def assert_prompt_callbacks_are_valid(
    agent: FakeAgent, prompt: Prompt, specials: Optional[dict] = None
) -> None:
    functions = prompt.functions()
    if functions is None:
        return

    for function in functions:
        callback = function["name"]
        assert isinstance(callback, str), "function name should be a string"
        arguments = prompt_function_to_callback_arguments(function, specials)
        agent.add_responses([PromptCallbackResponse(callback, arguments)])

        response = agent.ask(prompt)
        message = f"callback {callback} failed with arguments {arguments}: {response.message}"
        assert response.is_successful(), message
