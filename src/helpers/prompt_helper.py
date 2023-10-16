def prompt_function_to_callback_arguments(func: dict) -> dict:
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

        if "enum" in details:
            test_value = details["enum"][0]
        else:
            test_value = test_values_map.get(param_type, "UnknownType")

        test_values[param_name] = test_value

    return test_values
