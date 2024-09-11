import os
import requests
import networkx as nx
from itertools import product
from networkx.algorithms.dag import topological_sort
import yaml
import json
from creao.core.Endpoints import CreaoLLM, OpenAILLM
from creao.core.component.dedupe_component import Dedup, DedupeComponent
from creao.core.component.llm_component import LLMComponent
from creao.core.component.filter_component import FilterComponent
from creao.core.component.data_component import CSVDataComponent
from creao.core.component.util import class_registry, extract_json_schema, extract_jinja2_variables
from typing import List, Any, Dict
from pydantic import BaseModel, create_model

class Pipeline:
    def __init__(self):
        # Initialize an empty directed graph for the pipeline
        self.graph = nx.DiGraph()
        # Counter to assign unique IDs to each node
        self.node_id_counter = 0
        # Maps node names to node IDs for easy reference
        self.node_name_to_id = {}
        # Global variables shared across pipeline nodes
        self.global_variables = {}

    def add(self, name: str, class_instance):
        """
        Adds a node (component) to the pipeline.

        Args:
            name (str): The name of the node.
            class_instance: The instance of the class to be added as a node.
        """
        self.node_id_counter += 1
        # Add the node to the graph with a unique ID and store class instance
        self.graph.add_node(self.node_id_counter, name=name, data=class_instance)
        # Map the name to the node's ID for easy reference later
        self.node_name_to_id[name] = self.node_id_counter

    def connect(self, from_name: str, to_name: str):
        """
        Connects two nodes in the pipeline, forming an edge between them.

        Args:
            from_name (str): The name of the source node.
            to_name (str): The name of the target node.
        """
        from_node_id = self.node_name_to_id.get(from_name)
        to_node_id = self.node_name_to_id.get(to_name)
        if from_node_id is None or to_node_id is None:
            raise ValueError("One or both of the node names provided do not exist.")
        # Add a directed edge between two nodes in the graph
        self.graph.add_edge(from_node_id, to_node_id)

    def publish_pipeline_output(self, input_config, single_output):
        """
        Publishes the final pipeline output to a remote API.

        Args:
            input_config (dict): The input configuration used for the pipeline.
            single_output (dict): The final output to be published.
        """
        # API Gateway URL and necessary headers for publishing the output
        url = "https://drk3mkqa6b.execute-api.us-west-2.amazonaws.com/default/minimaxserver"
        api_key = os.environ["CREAO_API_KEY"]
        headers = {"Content-Type": "application/json", "x-api-key": api_key}

        # Prepare payload with pipeline and output data
        payload = {
            "single_output": single_output,
            "input_config": input_config,
            "pipeline_id": self.pipeline_id,
            "action": "pipeline_final_output",
        }

        # Send the request and handle the response
        response = requests.post(url, headers=headers, json=payload)
        print("publish_pipeline_output response:", response.content)

        # Attempt to return the response as JSON, handle any errors
        try:
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def run(self):
        """
        Runs the entire pipeline by executing the nodes in topological order.

        For each input from the data node, the output is passed to the next nodes
        in the pipeline. The final output is published via the publish function.
        """
        # Get the initial input data from the data node
        if len(self.single_run_input)>0:
            dict_list = self.single_run_input
        else:    
            dict_list = self.run_datanode()
        all_output = []
        for item in dict_list:
            print("input config:", item)
            # Run the pipeline for the current input
            output = self.run_single(item)
            all_output.append(output)
            print("single_output:", output)
            # Publish the output after the run
            self.publish_pipeline_output(item, output)
        return all_output

    def run_datanode(self):
        """
        Executes the first node in the pipeline (data node), and ensures all output values are lists.

        Returns:
            List[Dict[str, List[str]]]: The initial output from the data node.
        """
        # Ensure that the graph is a directed acyclic graph (DAG)
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("The graph is not a directed acyclic graph (DAG).")

        # Get the nodes in topological order
        execution_order = list(topological_sort(self.graph))

        # Run the first node (data node) to get the initial input
        for node_id in execution_order:
            class_instance = self.graph.nodes[node_id]["data"]
            node_name = self.graph.nodes[node_id]["name"]
            # Execute the class instance to get the output list
            output_list = class_instance.run([], instance_name=node_name, validate_schema=False)

            # Ensure all values in the output are lists
            output_list_force_list_value = []
            for item in output_list:
                for key in item:
                    value = item[key]
                    if not isinstance(value, list):
                        item[key] = [value]
                output_list_force_list_value.append(item)
            break

        return output_list_force_list_value

    def run_single(self, input_dict: dict):
        """
        Executes the entire pipeline for a given input dictionary.

        Args:
            input_dict (Dict[str, List[str]]): The input configuration for the pipeline.

        Returns:
            dict: The final output after all nodes have processed the input.
        """
        output_store = {}

        # Ensure the graph is a directed acyclic graph (DAG)
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("The graph is not a directed acyclic graph (DAG).")

        # Run nodes in topological order starting from the second node
        execution_order = list(topological_sort(self.graph))[1:]

        for node_id in execution_order:
            class_instance = self.graph.nodes[node_id]["data"]
            node_name = self.graph.nodes[node_id]["name"]
            # Get predecessors of the current node
            predecessors = list(self.graph.predecessors(node_id))

            # Collect the output from predecessor nodes
            predecessors_list = [output_store[self.graph.nodes[item]["data"]] for item in predecessors if self.graph.nodes[item]["data"] in output_store]


            # If any predecessor output is None, return an empty list
            if None in predecessors_list:
                return []

            # Generate all possible input combinations
            combinations = list(product(*predecessors_list))
            chained_input = [{k: v for d in item for k, v in d.items()} for item in combinations]

            if not chained_input:
                chained_input = [input_dict]

            # Run the class instance with the combined input
            combined_global_variables = self.global_variables.copy()
            combined_global_variables.update(input_dict)
            output = class_instance.run(chained_input, global_variables=combined_global_variables, instance_name=node_name, validate_schema=False)

            # Store the output for downstream nodes
            output_store[class_instance] = output

        return output

    def to_dict(self):
        """
        Converts the pipeline structure into a dictionary format for serialization.

        Returns:
            dict: The pipeline represented as a dictionary.
        """
        pipeline_dict = {"nodes": [], "connections": []}

        # Add nodes and their configurations to the dictionary
        for node_id, node_data in self.graph.nodes(data=True):
            class_instance = node_data["data"]
            class_dict = class_instance.__dict__.copy()

            # Remove sensitive data like LLM instance from serialization
            class_dict.pop("llm", None)

            node_dict = {
                "name": node_data["name"],
                "class": class_instance.__class__.__name__,
                "params": class_dict,
            }
            pipeline_dict["nodes"].append(node_dict)

        # Add connections between nodes to the dictionary
        for from_node, to_node in self.graph.edges():
            from_name = self.graph.nodes[from_node]["name"]
            to_name = self.graph.nodes[to_node]["name"]
            pipeline_dict["connections"].append({"from": from_name, "to": to_name})

        return pipeline_dict

    def save_to_yaml(self, file_path):
        """
        Saves the pipeline structure to a YAML file.

        Args:
            file_path (str): The path to save the YAML file.
        """
        pipeline_dict = self.to_dict()
        with open(file_path, "w") as yaml_file:
            yaml.dump(pipeline_dict, yaml_file)

    @staticmethod
    def from_dict(pipeline_dict, dataset_children_map, global_variables):
        """
        Reconstructs a Pipeline instance from a dictionary representation.

        Args:
            pipeline_dict (dict): The dictionary representation of the pipeline.
            dataset_children_map (dict): A map of dataset relationships.
            global_variables (dict): Global variables to be used in the pipeline.

        Returns:
            Pipeline: The reconstructed pipeline instance.
        """
        pipeline = Pipeline()
        pipeline.pipeline_id = pipeline_dict.get("pipeline_id", "pipeline_id_default")
        pipeline.single_run_input = pipeline_dict.get("single_run_inpt", [])
        pipeline.global_variables = global_variables
        pipeline.dataset_children_map = dataset_children_map

        # Reconstruct nodes
        for node in pipeline_dict["nodes"]:
            class_name = node["class"]
            class_instance = class_registry[class_name](**node["params"])
            if class_name == "CSVDataComponent":
                class_instance.global_dataset_map = pipeline_dict.get("global_dataset_map", {})
            pipeline.add(node["name"], class_instance)

        # Reconstruct connections
        for connection in pipeline_dict["connections"]:
            pipeline.connect(connection["from"], connection["to"])

        # Reinitialize necessary components for certain classes
        for node_id in pipeline.graph.nodes:
            class_instance = pipeline.graph.nodes[node_id]["data"]
            if isinstance(class_instance, DedupeComponent):
                class_instance.llm = Dedup()
            elif isinstance(class_instance, LLMComponent):
                if class_instance.service == "default":
                    class_instance.llm = CreaoLLM(bot_name="assistant", bot_content="assistant")
                elif class_instance.service == "openai":
                    class_instance.llm = OpenAILLM()

        return pipeline

    @staticmethod
    def create_pydantic_model(fields: List[Dict[str, Any]]) -> BaseModel:
        """
        Create a Pydantic model dynamically from a list of dictionaries representing fields.

        Args:
        - fields (List[Dict[str, Any]]): A list where each dict contains 'name' and 'type' keys.

        Returns:
        - A dynamically created Pydantic model class.
        """
        new_json_list = []
        for item in fields:
            if item["type"] == "list[str]":
                item["type"] = List[str]
            elif item["type"] == "str":
                item["type"] = str
            new_json_list.append(item)
        fields = new_json_list
        field_definitions = {field['name']: (field['type'], ...) for field in fields}
        return create_model('JsonBase', **field_definitions)
    

    @staticmethod
    def load_from_rf_json(file_path, rf_dict=None, global_variables=None):
        """
        Loads a pipeline from a JSON file created in a specific format.

        Args:
            file_path (str): The path to the JSON file.
            rf_dict (dict): The dictionary representation of the pipeline (optional).
            global_variables (dict): Global variables for the pipeline (optional).

        Returns:
            Pipeline: The reconstructed pipeline.
        """
        if rf_dict is None:
            with open(file_path, "r") as rf_file:
                rf_dict = json.load(rf_file)

        nodes = []
        id_to_name_dict = {}

        # Reconstruct nodes from the JSON file
        for node in rf_dict["nodes"]:
            id = node["id"]
            temp_dict = {}
            params = {}
            node_data = node["data"]
            output_schema = node_data.get("output_schema", [])

            temp_dict["name"] = node_data["label"]

            # Assign class based on the node type
            if "type" not in node or node["type"] == "llmNode":
                temp_dict["class"] = "LLMComponent"
                json_schema = extract_json_schema(Pipeline.create_pydantic_model(output_schema))
                params["json_schema"] = json_schema
            elif node["type"] == "dataNode":
                temp_dict["class"] = "CSVDataComponent"
            elif node["type"] == "filterNode":
                temp_dict["class"] = "FilterComponent"
            elif node["type"] == "dedupeNode":
                temp_dict["class"] = "DedupeComponent"

            # Add additional parameters to the node
            for key in node_data:
                if key not in ("output_schema", "label"):
                    params[key] = node_data[key]

            params["component_name"] = node_data["label"]
            temp_dict["params"] = params

            prompt_template = node_data.get("prompt_template", "")
            id_to_name_dict[id] = {
                "label": node_data["label"],
                "class": temp_dict["class"],
                "prompt_template": prompt_template,
            }
            print("temp_dict:",temp_dict)
            nodes.append(temp_dict)

        # Reconstruct connections and dataset children map
        connections = []
        dataset_children_map = {}
        for edge in rf_dict["edges"]:
            from_node = id_to_name_dict[edge["source"]]
            to_node = id_to_name_dict[edge["target"]]

            # Handle special case for CSVDataComponent nodes
            if from_node["class"] == "CSVDataComponent":
                dataset_children_map.setdefault(from_node["label"], {})[to_node["label"]] = extract_jinja2_variables(to_node["prompt_template"])

            connections.append({"from": from_node["label"], "to": to_node["label"]})
        single_run_input = rf_dict.get("single_run_inpt", [])
        # Final JSON to be processed back into a pipeline
        final_json = {
            "nodes": nodes,
            "connections": connections,
            "pipeline_id": rf_dict["pipeline_id"],
            "global_dataset_map": rf_dict["global_dataset_map"],
            "single_run_inpt":single_run_input
        }
        print("final_json:", final_json)
        return Pipeline.from_dict(final_json, dataset_children_map, global_variables)

