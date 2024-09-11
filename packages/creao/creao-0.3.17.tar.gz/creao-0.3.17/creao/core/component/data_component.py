from abc import ABC, abstractmethod
import csv
from typing import Dict, List
from datasets import load_dataset
from creao.core.component.util import creao_component
from io import StringIO
import boto3
from urllib.parse import urlparse



class BaseDataComponent(ABC):
    def __init__(self, **kwargs):
        """
        Initialize the base data component, possibly with additional keyword arguments
        for future extensions.
        
        Args:
            **kwargs: Additional keyword arguments for future use.
        """
        self.global_dataset_map = kwargs.get('global_dataset_map', {})

    @abstractmethod
    def load_data(self) -> List[Dict[str, str]]:
        """
        Abstract method for loading data that must be implemented by subclasses.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded data.
        """
        pass

    def _remap_keys(self, dataset: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Apply the global dataset mapping to remap keys in the dataset.

        Args:
            dataset (List[Dict[str, str]]): The dataset to process.

        Returns:
            List[Dict[str, str]]: The dataset with keys remapped according to global_dataset_map.
        """
        remapped_data = []

        for item in dataset:
            # Create a copy of the item so that the original is not modified
            remapped_item = item.copy()
            # Iterate over each key in the global dataset map and remap it
            for key in self.global_dataset_map:
                if key in remapped_item:
                    value = remapped_item.pop(key)
                    mapped_key = self.global_dataset_map[key]
                    remapped_item[mapped_key] = value

            remapped_data.append(remapped_item)

        return remapped_data

    def run(self, chained_input: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """
        Load the data, apply global mappings, and return the processed data.

        Args:
            chained_input (List[Dict[str, str]], optional): Input data passed from the previous 
                                                            component in the pipeline.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the processed dataset 
                                  with keys remapped according to the global dataset map.
        """
        # Load the data using the subclass-specific method
        dataset = self.load_data()

        # Apply global dataset mapping to the loaded data
        return self._remap_keys(dataset)
    

@creao_component
class HFDataComponent(BaseDataComponent):
    def __init__(self, hf_dataset_path: str, **kwargs):
        """
        Initialize the HFDataComponent by setting the path to the Hugging Face dataset.
        
        Args:
            hf_dataset_path (str): Path to the Hugging Face dataset (e.g., 'imdb').
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.hf_path = hf_dataset_path

    def load_data(self) -> List[Dict[str, str]]:
        """
        Load data from the specified Hugging Face dataset and convert it to a list of dictionaries.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded dataset.
        """
        # Log the beginning of the dataset download process
        print(f"Downloading dataset from {self.hf_path}...")

        # Load the dataset split (defaulting to 'train')
        dataset = load_dataset(self.hf_path, split="train")
        
        # Convert the dataset to a list of dictionaries with string values
        return [{key: str(value) for key, value in example.items()} for example in dataset]


@creao_component
class CSVDataComponent(BaseDataComponent):
    def __init__(self, file_path: str, **kwargs):
        """
        Initialize the CSVDataComponent by setting the path to the S3 CSV file.

        Args:
            file_path (str): S3 path to the CSV file (e.g., 's3://bucket-name/path/to/file.csv').
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.file_path = file_path

    def load_data(self) -> List[Dict[str, str]]:
        """
        Load data from the specified S3 CSV file and convert it to a list of dictionaries.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded CSV data.
        """
        s3_client = boto3.client('s3')
        s3_path = self.file_path
        # Parse the S3 bucket name and key from the S3 path
        bucket_name, key = self._parse_s3_url(s3_path)

        # Download the CSV file from S3
        print(f"Downloading CSV data from S3: {s3_path}...")
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        csv_content = response['Body'].read().decode('utf-8')

        # Read the CSV file and convert it to a list of dictionaries
        data_list = []
        reader = csv.DictReader(StringIO(csv_content))
        for row in reader:
            item = {key: str(value) for key, value in row.items()}
            data_list.append(item)

        return data_list

    def _parse_s3_url(self, url: str) -> (str, str): # type: ignore
        """
        Parse the S3 URL to extract the bucket name and key.

        Args:
            url (str): The S3 URL (e.g., 'https://bucket-name.s3.region.amazonaws.com/key/to/file.csv').

        Returns:
            tuple: A tuple containing the bucket name and key.
        """
        parsed_url = urlparse(url)
        
        # Extract bucket name from the netloc (e.g., 'creaodev.s3.us-west-2.amazonaws.com')
        domain_parts = parsed_url.netloc.split('.')
        bucket_name = domain_parts[0]  # This assumes the bucket name is the first part
        
        # Extract key from the path (e.g., '/key/to/file.csv')
        key = parsed_url.path.lstrip('/')  # Strip leading slash from the path
        
        return bucket_name, key