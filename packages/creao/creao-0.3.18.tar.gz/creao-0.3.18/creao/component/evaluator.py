from typing import List
from haystack import component, Pipeline

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import (
    InformationRetrievalEvaluator,
    SequentialEvaluator,
)
from sentence_transformers.util import cos_sim

from datasets import Dataset
from sentence_transformers import SentenceTransformerModelCardData, SentenceTransformer
import time
from datetime import datetime
from sentence_transformers.losses import MatryoshkaLoss, TripletLoss

from sentence_transformers import SentenceTransformerTrainingArguments
from sentence_transformers.training_args import BatchSamplers

from sentence_transformers import SentenceTransformerTrainer
from datasets import load_dataset, concatenate_datasets


def prepare_matryoshka_evaluator(
    train_data_path: str, test_data_path: str, matryoshka_dimensions: List[int]
) -> SequentialEvaluator:
    test_dataset = load_dataset("json", data_files="test_dataset.json", split="train")
    train_dataset = load_dataset("json", data_files="train_dataset.json", split="train")
    return prepare_matryoshka_evaluator(
        train_dataset, test_dataset, matryoshka_dimensions
    )


def prepare_matryoshka_evaluator(
    train_dataset: Dataset, test_dataset: Dataset, matryoshka_dimensions: List[int]
) -> SequentialEvaluator:
    # test_dataset = load_dataset("json", data_files="test_dataset.json", split="train")
    # train_dataset = load_dataset("json", data_files="train_dataset.json", split="train")
    corpus_dataset = concatenate_datasets(
        [train_dataset, test_dataset]
    )  # only needed for evaluation
    # Convert the datasets to dictionaries
    corpus = dict(
        zip(corpus_dataset["id"], corpus_dataset["positive"])
    )  # Our corpus (cid => document)
    queries = dict(
        zip(test_dataset["id"], test_dataset["anchor"])
    )  # Our queries (qid => question)

    # Create a mapping of relevant document (1 in our case) for each query
    relevant_docs = {}  # Query ID to relevant documents (qid => set([relevant_cids])
    for q_id in queries:
        relevant_docs[q_id] = [q_id]  # [corpus[q_id]]

    matryoshka_evaluators = []
    # Iterate over the different dimensions
    for dim in matryoshka_dimensions:
        ir_evaluator = InformationRetrievalEvaluator(
            queries=queries,
            corpus=corpus,
            relevant_docs=relevant_docs,
            name=f"dim_{dim}",
            truncate_dim=dim,  # Truncate the embeddings to a certain dimension
            score_functions={"cosine": cos_sim},
        )
        matryoshka_evaluators.append(ir_evaluator)

    # Create a sequential evaluator
    evaluator = SequentialEvaluator(matryoshka_evaluators)
    return evaluator


def doMatryoshkaEval(
    evaluator: SequentialEvaluator, model: SentenceTransformer
) -> None:
    results = evaluator(model)
    print(results)


@component
class EmbeddingModelMatryoshkaTripletEvaluator:
    """
    A component performing Matryoshka evaluation against the given embedding model.
    """

    @component.output_types()
    def run(self, evaluator: SequentialEvaluator, model: SentenceTransformer):
        print("[EmbeddingModelMatryoshkaTripletEvaluator]")
        print("started")
        doMatryoshkaEval(evaluator, model)
        print("completed")
        print("[EmbeddingModelMatryoshkaTripletEvaluator]")
        # return {"model_output_path": model_output_path}


# test
matryoshka_dimensions = [768, 512, 256, 128, 64]
train_dataset = load_dataset("json", data_files="train_dataset.json", split="train")
test_dataset = load_dataset("json", data_files="test_dataset.json", split="train")
evaluator = prepare_matryoshka_evaluator(
    train_dataset, test_dataset, matryoshka_dimensions
)

model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5",
    # model_kwargs={"attn_implementation": "sdpa"},  # sdpa will be used by default if available
    model_card_data=SentenceTransformerModelCardData(
        language="en",
        license="apache-2.0",
        model_name="BGE base ArgillaSDK Matryoshka",
    ),
)

evaluatortest = EmbeddingModelMatryoshkaTripletEvaluator()
evaluatortest.run(evaluator, model)
