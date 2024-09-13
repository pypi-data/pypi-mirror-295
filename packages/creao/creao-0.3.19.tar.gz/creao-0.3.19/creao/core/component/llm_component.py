import json
from typing import Dict, List, Tuple

from jinja2 import Template
from creao.core.Endpoints import CreaoLLM, OpenAILLM
from creao.core.component.util import (
    extract_jinja2_variables,
    creao_component,
    generate_combinations_from_dict_list,
    extract_json_schema,
)


@creao_component
class LLMComponent:
    def __init__(
        self,
        prompt_template: str = None,
        class_instance=None,
        service: str = "default",
        pipeline_id: str = "pipeline_id_default",
        component_name: str = "default",
        **kwargs,
    ):
        """
        Initializes the LLMComponent with necessary configurations.

        Args:
            prompt_template (str): Template string for generating prompts using Jinja2.
            class_instance: An instance of a class used to extract a JSON schema (optional).
            service (str): Specifies the LLM service to use, default is "default".
            pipeline_id (str): Identifier for the pipeline, default is "pipeline_id_default".
            component_name (str): Name of the component, default is "default".
            **kwargs: Additional keyword arguments, such as `json_schema` and `type`.
        """
        self.prompt_template = (
            prompt_template  # Template to be used for generating prompts
        )
        self.component_name = (
            component_name  # Name of the component for logging/tracking
        )
        self.pipeline_id = (
            pipeline_id  # Identifier for the pipeline this component belongs to
        )
        self.service = service  # The LLM service type (e.g., "default", "openai")

        # Extract JSON schema from the provided class instance or use the one in kwargs
        self.json_schema = self._extract_json_schema(class_instance, kwargs)

        # Initialize the appropriate LLM instance based on the selected service
        self.llm = self._initialize_llm()

    def run(
        self, chained_input: List[Dict[str, List[str]]]
    ) -> List[Dict[str, List[str]]]:
        """
        Processes the input data through the LLM based on the prompt template.

        Args:
            chained_input (List[Dict[str, List[str]]]): List of dictionaries containing input data.

        Returns:
            List[Dict[str, List[str]]]: Processed output after invoking the LLM.
        """
        # Extract variables from the Jinja2 template to be used in rendering the prompt
        extracted_vars = self._extract_jinja2_variables()

        res_list = []  # Initialize a list to store results for each input
        for single_chain_input in chained_input:
            # Prepare Jinja2 inputs by mapping extracted variables to the chain input
            jinja_inputs = self._prepare_jinja_inputs(
                extracted_vars, single_chain_input
            )

            # Generate a list of prompts by rendering the template with Jinja2 inputs
            prompts = self._generate_prompts(jinja_inputs)

            for prompt, input_dict in prompts:
                # Invoke the LLM with the rendered prompt and handle the response
                response_json = self.invoke_llm(prompt)
                print("response_json:", response_json)

                if response_json is None:
                    return None  # Exit early if there's an error invoking the LLM

                # Process the LLM's response and prepare the final output format
                processed_response = self.process_llm_response(
                    response_json, input_dict
                )
                res_list.append(
                    processed_response
                )  # Append the processed response to the result list

        return res_list  # Return the list of processed results

    def _extract_json_schema(self, class_instance, kwargs) -> dict:
        """
        Extracts the JSON schema from the class instance or uses the provided schema.

        Args:
            class_instance: The class instance from which to extract the JSON schema.
            kwargs: Dictionary containing the keyword arguments, including `json_schema`.

        Returns:
            dict: The extracted or provided JSON schema.
        """
        json_schema = kwargs.pop(
            "json_schema", None
        )  # Attempt to get the JSON schema from kwargs
        if json_schema is None and class_instance is not None:
            # If no schema is provided, try to extract it from the class instance
            return extract_json_schema(class_instance)
        return json_schema  # Return the schema from kwargs or None if not found

    def _initialize_llm(self):
        """
        Initializes the LLM based on the selected service.

        Returns:
            The initialized LLM instance.
        """
        # Initialize the LLM based on the service type
        if self.service == "default":
            return CreaoLLM(bot_name="assistant", bot_content="assistant")
        elif self.service == "openai":
            return OpenAILLM()
        return None  # Return None if an unsupported service is selected

    def _extract_jinja2_variables(self) -> List[str]:
        """
        Extracts variables from the Jinja2 template.

        Returns:
            List[str]: A list of variables extracted from the Jinja2 template.
        """
        # Use the Pipeline utility to extract variables from the prompt template
        return extract_jinja2_variables(self.prompt_template)

    def _prepare_jinja_inputs(
        self, extracted_vars: List[str], single_chain_input: Dict[str, List[str]]
    ) -> List[Dict[str, str]]:
        """
        Prepares Jinja2 inputs by mapping extracted variables to the chain input.

        Args:
            extracted_vars (List[str]): List of variables extracted from the template.
            single_chain_input (Dict[str, List[str]]): Single input dictionary from the chained input.

        Returns:
            List[Dict[str, str]]: A list of dictionaries prepared for Jinja2 rendering.
        """
        # Create a list of dictionaries where each variable is mapped to its corresponding value
        jinja_var_list = [{var: single_chain_input[var]} for var in extracted_vars]
        return generate_combinations_from_dict_list(
            jinja_var_list
        )  # Convert the list of dictionaries into the required format

    def _generate_prompts(
        self, jinja_inputs: List[Dict[str, str]]
    ) -> List[Tuple[str, Dict[str, str]]]:
        """
        Generates a list of prompts by rendering the template with Jinja2 inputs.

        Args:
            jinja_inputs (List[Dict[str, str]]): A list of dictionaries prepared for Jinja2 rendering.

        Returns:
            List[Tuple[str, Dict[str, str]]]: A list of tuples containing the rendered prompt and the corresponding input dictionary.
        """
        # Initialize the Jinja2 template with the prompt template string
        prompt_template = Template(self.prompt_template)
        # Render the template with each set of inputs and return the list of prompts with input mappings
        return [(prompt_template.render(item), item) for item in jinja_inputs]

    def invoke_llm(self, prompt: str) -> dict:
        """
        Invokes the appropriate LLM based on the service type.

        Args:
            prompt (str): The prompt to be sent to the LLM.

        Returns:
            dict: The LLM's response as a dictionary, or None if an error occurs.
        """
        try:
            if self.service == "default":
                # Invoke the default LLM with the prompt, schema, component name, and pipeline ID
                response_json = self.llm.invoke(
                    prompt,
                    self.json_schema or "",
                    self.component_name,
                    self.pipeline_id,
                )
                if self.json_schema:
                    # Parse the response as JSON if a schema is provided
                    return json.loads(response_json["reply"])
                return {
                    "reply": response_json["reply"]
                }  # Return the plain reply in a dict with key as reply if no schema is used
            elif self.service == "openai":
                # For OpenAI service, simply parse the response as JSON
                return json.loads(self.llm.invoke(prompt))
        except Exception as e:
            # Log any exceptions that occur during LLM invocation
            print(f"Error invoking LLM: {e}")
            return None  # Return None if an error occurs

    def process_llm_response(self, raw_answer: dict, input_dict: dict) -> dict:
        """
        Processes the LLM's raw response into a consistent list-based dictionary.

        Args:
            raw_answer (dict): The raw response from the LLM.
            input_dict (dict): The original input dictionary.

        Returns:
            dict: Processed response with each value in list format.
        """
        processed_response = {}

        if self.service == "openai":
            # For OpenAI service, wrap the raw answer in a list under the "reply" key
            processed_response["reply"] = [raw_answer]
        else:
            # For the default service, ensure all values in the response are lists
            for key, value in raw_answer.items():
                processed_response[key] = value if isinstance(value, list) else [value]

        # Update the processed response with the original input values, converting them to lists
        input_dict_value_list = {key: [input_dict[key]] for key in input_dict}
        processed_response.update(input_dict_value_list)

        return processed_response  # Return the final processed response
