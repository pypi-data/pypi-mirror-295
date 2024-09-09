from itertools import product
from typing import Any, Dict, List

from jinja2 import Environment, meta

# A global registry to store all registered classes
class_registry = {}


def creao_component(cls):
    """
    Registers a class in the global registry and wraps its `run` method
    to handle global variables.

    Args:
        cls (type): The class to be registered and wrapped.

    Returns:
        type: The original class with its `run` method wrapped.
    """
    # Retrieve the original `run` method of the class
    original_run_method = getattr(cls, "run", None)

    # Ensure the class has a `run` method
    if original_run_method is None:
        raise ValueError(f"Class {cls.__name__} must have a 'run' method.")

    def wrapped_run(self, chained_input: List[Dict[str, List[str]]], *args, **kwargs):
        """
        Wrapper for the original `run` method that processes global variables
        and updates the chained input accordingly.

        Args:
            chained_input (List[Dict[str, List[str]]]): The input data that may be processed
                                                        and passed to the `run` method.
            *args: Additional positional arguments for the `run` method.
            **kwargs: Additional keyword arguments for the `run` method,
                      including `global_variables` which are processed separately.

        Returns:
            Any: The output from the original `run` method.
        """
        # Extract and process global variables from kwargs
        global_variables = kwargs.pop("global_variables", {})
        processed_global_variables = {}

        # Convert global variables into a consistent list format
        for key, value in global_variables.items():
            processed_global_variables[key] = (
                value if isinstance(value, list) else [value]
            )

        # Update each item in the chained input with the processed global variables
        for single_chained_input in chained_input:
            single_chained_input.update(processed_global_variables)

        # Call the original `run` method with the modified input
        output = original_run_method(self, chained_input)
        return output

    # Replace the original `run` method of the class with the wrapped version
    setattr(cls, "run", wrapped_run)

    # Register the class in the global class registry
    class_registry[cls.__name__] = cls

    # Return the original class with the wrapped `run` method
    return cls


def generate_combinations_from_dict_list(dict_list):
    """
    Generate a list of dictionaries representing all possible combinations of values
    from a list of dictionaries with identical keys.

    Args:
        dict_list (list of dict): A list of dictionaries where each dictionary has the same keys.

    Returns:
        list of dict: A list of dictionaries, each representing a unique combination of the values
                      from the input dictionaries.
    """
    if len(dict_list) == 0:
        return []

    # Initialize lists to store keys and values from the input dictionaries
    keys = []
    values = []

    # Extract keys and corresponding values from each dictionary in the input list
    for d in dict_list:
        for k, v in d.items():
            keys.append(k)
            values.append(v)

    # Generate the Cartesian product of the lists of values
    combinations = product(*values)

    # Construct a list of dictionaries, each representing a unique combination
    result = [dict(zip(keys, combo)) for combo in combinations]

    return result


def extract_json_schema(class_instance) -> Dict[str, Any]:
    """
    Extract and modify the JSON schema of a given class instance.

    Args:
        class_instance: An instance of a class that has a `.schema()` method which returns a JSON schema.

    Returns:
        Dict[str, Any]: A dictionary representing the modified JSON schema, with 'title' fields removed.
    """
    # Generate the JSON schema for the class instance
    json_schema = class_instance.schema()

    # Extract the 'properties' part of the schema, which contains the details of each field
    output_dict = json_schema["properties"]

    # Iterate over each field in the class instance
    for key in class_instance.__fields__:
        # Remove the 'title' attribute from each field's schema (if present)
        output_dict[key].pop("title")

    # Return the modified schema as a dictionary
    return output_dict


def extract_jinja2_variables(template_str: str) -> List[str]:
    env = Environment()
    # Parse the template
    parsed_content = env.parse(template_str)
    variables = meta.find_undeclared_variables(parsed_content)
    return list(variables)
