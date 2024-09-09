from typing import Dict, List, Union
from creao.core.component.util import creao_component

@creao_component  # This decorator registers the class as a component in a pipeline framework
class FilterComponent:
    """
    FilterComponent is responsible for filtering data based on a specific condition applied to a designated column.
    The component can perform two types of filtering:
    1. Exact match filtering for strings or direct equality comparison.
    2. Numeric condition filtering for values that need to meet a specified numeric condition (e.g., >, <, >=).

    Attributes:
    - filtered_column (str): The name of the column on which the filter is applied.
    - condition_type (str): The type of filtering condition. It can be either "exact_match" or "numeric_condition".
    - condition_value (Union[str, int, float]): The value or condition used for filtering. It can be a string (for exact match)
      or a numeric condition (e.g., "> 5", "== 10").
    - pipeline_id (str): Identifier for the pipeline this component belongs to. Defaults to "pipeline_id_default".
    - component_name (str): Name of the component, default is "FilterComponent".
    - **kwargs: Additional arguments that can be passed for customization.

    Methods:
    - run(chained_input: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      This method performs the filtering on the input data (a list of dictionaries). It processes each dictionary (or row)
      and filters it based on the specified conditions. It returns the filtered data as a list of dictionaries.

      - chained_input: The input data, which is expected to be a list of dictionaries where each dictionary represents a row or record.
      - filtered_output: The filtered data after applying the conditions.

      The method supports:
      - "exact_match" condition: Filters based on string equality or direct comparison to a specific value.
      - "numeric_condition" condition: Filters based on a numerical comparison using operators like >, <, >=, etc.

      Example usage:
      - If the condition_type is "exact_match" and condition_value is "apple", it will filter and return only the rows where
        the specified column has the value "apple".
      - If the condition_type is "numeric_condition" and condition_value is "> 5", it will filter and return rows where the
        numeric value in the specified column is greater than 5.

      If the column value cannot be found in the row or cannot be converted to a number for numeric conditions, the row is skipped.

    Example:
    component = FilterComponent(filtered_column="price", condition_type="numeric_condition", condition_value="> 50")
    filtered_data = component.run(input_data)
    """

    def __init__(
        self,
        filtered_column: str,
        condition_type: str = "exact_match",  # or "numeric_condition"
        condition_value: Union[str, int, float] = None,
        pipeline_id: str = "pipeline_id_default",
        component_name: str = "FilterComponent",
        **kwargs,
    ):
        self.filtered_column = filtered_column  # Column to apply the filter on
        self.condition_type = condition_type  # Type of condition, either "exact_match" or "numeric_condition"
        self.condition_value = condition_value  # Value or condition to filter against
        self.pipeline_id = pipeline_id  # ID of the pipeline this component belongs to
        self.component_name = component_name  # Name of the component

    def run(
        self, chained_input: List[Dict[str, List[str]]]
    ) -> List[Dict[str, List[str]]]:
        for single_chained_input in chained_input:
            assert (
                self.filtered_column in single_chained_input
            ), f"Column '{self.filtered_column}' not found in the input data."
            filtered_output = []
            column_values = single_chained_input.get(
                self.filtered_column
            )  # Retrieve the value from the specified column
            # Handle different condition types
            for column_value in column_values:
                if self.condition_type == "exact_match":
                    if column_value == self.condition_value:  # Check for exact match
                        filtered_output.append(
                            column_value
                        )  # Add the row to the output if it matches

                elif self.condition_type == "numeric_condition":
                    try:
                        numeric_value = float(
                            column_value
                        )  # Convert the column value to a numeric value
                        if eval(
                            f"{numeric_value} {self.condition_value}"
                        ):  # Evaluate the numeric condition
                            filtered_output.append(
                                column_value
                            )  # Add the row to the output if it meets the condition
                    except ValueError:
                        continue  # Skip if the value can't be converted to a number
            single_chained_input[self.filtered_column] = filtered_output
        return chained_input  # Return the filtered data