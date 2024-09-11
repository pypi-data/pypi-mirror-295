from typing import List
from haystack import component, Pipeline

import pandas as pd
from datasets import Dataset, concatenate_datasets

from github import Github, Repository, ContentFile
import requests
import os

from typing import List, Optional
from pathlib import Path

import nltk
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')


def download(c: ContentFile, out: str) -> None:
    r = requests.get(c.download_url)
    output_path = f"{out}/{c.path}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        print(f"downloading {c.path} to {out}")
        f.write(r.content)


def download_folder(repo: Repository, folder: str, out: str, recursive: bool) -> None:
    contents = repo.get_contents(folder)
    for c in contents:
        if c.download_url is None:
            if recursive:
                download_folder(repo, c.path, out, recursive)
            continue
        download(c, out)


def create_chunks(md_files: List[str]) -> dict[str, List[str]]:
    """Create the chunks of text from the markdown files.

    Note:
        We should allow the chunking strategy to take into account the max size delimited
        by the number of tokens.

    Args:
        md_files: List of paths to the markdown files.

    Returns:
        Dictionary from filename to the list of chunks.
    """
    from unstructured.chunking.title import chunk_by_title
    from unstructured.partition.auto import partition

    data = {}
    for file in md_files:
        partitioned_file = partition(filename=file)
        chunks = [str(chunk) for chunk in chunk_by_title(partitioned_file)]

        data[str(file)] = chunks
    return data


def create_dataset(
    data: dict[str, List[str]], repo_name: Optional[str] = None
) -> Dataset:
    """Creates a dataset from the dictionary of chunks.

    Args:
        data: Dictionary from filename to the list of chunks,
            as obtained from `create_chunks`.

    Returns:
        Dataset with `filename` and `chunks` columns.
    """
    df = pd.DataFrame.from_records(
        [(k, v) for k, values in data.items() for v in values],
        columns=["filename", "chunks"],
    )
    if repo_name:
        df["repo_name"] = repo_name
    ds = Dataset.from_pandas(df)
    return ds


@component
class RepoMarkDownCollector:
    """
    A component collecting MarkDown files from a github repo
    """

    @component.output_types(md_file_paths=List[str])
    def run(self, repo_name: str):
        print()
        print("[RepoMarkDownCollector]")
        gh = Github()
        repo = gh.get_repo(repo_name)

        docs_path = Path(repo_name.split("/")[1])  # the default output path

        if docs_path.exists():
            print(f"Folder {docs_path} already exists, skipping download.")
        else:
            print("Downloading the files...")
            download_folder(
                repo, "docs", str(docs_path), True
            )  # docs could be exposable

        print("Start collecting MarkDown files...")
        md_files = list(docs_path.glob("**/*.md"))  # a list of Path
        md_files = [str(path) for path in md_files]  # a list of str
        print(md_files)
        print(f"{len(md_files)} MarkDown files collected successfully")
        print("[RepoMarkDownCollector]")
        print()
        return {"md_file_paths": md_files}


@component
class ChunkDataGenerator:
    """
    A component generating chunks from a list of files
    """

    @component.output_types(chunk_data=dict[str, List[str]])
    def run(self, source_files: List[str]):
        # Loop to iterate over the files and generate chunks from the text pieces
        print()
        print("[ChunkDataGenerator]")
        print("Generating the chunks from the markdown files...")
        output = create_chunks(source_files)
        print("Completed.")
        print("[ChunkDataGenerator]")
        print()
        return {"chunk_data": output}


@component
class DatasetCreator:
    """
    A component generating Dataset with filename and chunks columns and repo name
    """

    @component.output_types(dataset=Dataset)
    def run(self, chuck_data: dict[str, List[str]], repo_name: Optional[str] = None):
        print()
        print("[DatasetCreator]")
        print("Creating dataset...")
        output = create_dataset(chuck_data, repo_name=repo_name)
        print("Completed.")
        print("[DatasetCreator]")
        print()
        return {"dataset": output}


data_pipeline = Pipeline()
data_pipeline.add_component(name="markdown_collector", instance=RepoMarkDownCollector())
data_pipeline.add_component(name="chunk_data_generator", instance=ChunkDataGenerator())
data_pipeline.add_component(name="dataset_creator", instance=DatasetCreator())

data_pipeline.connect(
    sender="markdown_collector.md_file_paths",
    receiver="chunk_data_generator.source_files",
)
data_pipeline.connect(
    sender="chunk_data_generator.chunk_data", receiver="dataset_creator.chuck_data"
)

result = data_pipeline.run(
    {"markdown_collector": {"repo_name": "argilla-io/argilla-python"}}
)

print(result["dataset_creator"]["dataset"])
