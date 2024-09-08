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

from component.evaluator import prepare_matryoshka_evaluator


def load_split_dataset_to_local(
    dataset_path: str,
    select_columns: List[str],
    test_ratio: float,
    train_local_json_path: str,
    test_local_json_path: str,
) -> dict[str, str]:
    """Load dataset, split and save to local.

    Args:
        xxx

    Returns:
        Two local Json file paths organized in a dict, representing the split train and test.
    """
    # dataset_path = "plaguss/argilla_sdk_docs_queries"
    # select_columns = ["anchor", "positive", "negative"]

    # Load dataset from the hub
    dataset = load_dataset(dataset_path, split="train")
    dataset = (
        load_dataset(dataset_path, split="train")
        .select_columns(select_columns)  # Select the relevant columns
        .add_column("id", range(len(dataset)))  # Add an id column to the dataset
        .train_test_split(
            test_size=test_ratio
        )  # split dataset by specifying test set rate
    )

    # save datasets to disk
    dataset["train"].to_json(train_local_json_path, orient="records")
    dataset["test"].to_json(test_local_json_path, orient="records")
    return {"train": train_local_json_path, "test": test_local_json_path}


@component
class HuggfingFaceDatasetLoadSplitPersistence:
    """
    A component loading, spliting, saving datasets
    """

    @component.output_types(dict_train_test_paths=dict[str, str])
    def run(
        self,
        dataset_path: str,
        select_columns: List[str],
        test_ratio: float,
        train_local_json_path: str,
        test_local_json_path: str,
    ):
        print()
        output_dict = load_split_dataset_to_local(
            dataset_path,
            select_columns,
            test_ratio,
            train_local_json_path,
            test_local_json_path,
        )
        print()
        return {"dict_train_test_paths": output_dict}


"""
test = HuggfingFaceDatasetLoadSplitPersistence()
result = test.run(dataset_path="plaguss/argilla_sdk_docs_queries", select_columns=["anchor", "positive", "negative"], test_ratio=0.1, 
         train_local_json_path="train_dataset.json", test_local_json_path="test_dataset.json")
print(result["dict_train_test_paths"])
"""


finetuner_config_example = {
    "train_data_path": "train_dataset.json",
    "test_data_path": "test_dataset.json",
    "select_columns": ["anchor", "positive", "negative"],
    "model_id": "BAAI/bge-base-en-v1.5",
    "matryoshka_dimensions": [768, 512, 256, 128, 64],
    # "device": "mps",
    "output_dir": "bge-base-argilla-sdk-matryoshka",
    "num_train_epochs": 8,  # number of epochs
    "per_device_train_batch_size": 16,  # train batch size
    "gradient_accumulation_steps": 8,  # for a global batch size of 512
    "per_device_eval_batch_size": 4,  # evaluation batch size
    "warmup_ratio": 0.1,  # warmup ratio
    "learning_rate": 2e-7,  # learning rate, 2e-5 is a good value
    "lr_scheduler_type": "cosine",  # use constant learning rate scheduler
    # optim="adamw_torch_fused",                  # use fused adamw optimizer
    # tf32=True,                                  # use tf32 precision
    # bf16=True,                                  # use bf16 precision
    # batch_sampler=BatchSamplers.NO_DUPLICATES,  # MultipleNegativesRankingLoss benefits from no duplicate samples in a batch
    "eval_strategy": "epoch",  # evaluate after each epoch
    "save_strategy": "epoch",  # save after each epoch
    "logging_steps": 5,  # log every 10 steps
    "save_total_limit": 1,  # save only the last 3 models
    "load_best_model_at_end": True,  # load the best model when training ends
    "metric_for_best_model": "eval_dim_512_cosine_ndcg@10",  # Optimizing for the best ndcg@10 score for the 512 dimension
}


def doEmbederMatryoshkaTripletFinetune(finetuner_config: dict) -> str:
    # load dataset back
    test_dataset = load_dataset(
        "json", data_files=finetuner_config["test_data_path"], split="train"
    )
    train_dataset = load_dataset(
        "json", data_files=finetuner_config["train_data_path"], split="train"
    )
    # corpus_dataset = concatenate_datasets([train_dataset, test_dataset]) #only needed for evaluation

    # remove none
    train_dataset_cleaned = (
        train_dataset.select_columns(finetuner_config["select_columns"])
        .to_pandas()
        .dropna()
    )
    test_dataset_cleaned = (
        test_dataset.select_columns(finetuner_config["select_columns"])
        .to_pandas()
        .dropna()
    )

    train_dataset_cleaned = Dataset.from_pandas(
        train_dataset_cleaned, preserve_index=False
    )
    test_dataset_cleaned = Dataset.from_pandas(
        test_dataset_cleaned, preserve_index=False
    )

    model_id = finetuner_config[
        "model_id"
    ]  # "BAAI/bge-base-en-v1.5"  # Hugging Face model ID https://huggingface.co/BAAI/bge-base-en-v1.5
    matryoshka_dimensions = finetuner_config[
        "matryoshka_dimensions"
    ]  # [768, 512, 256, 128, 64]  # Important: large to small

    device = (
        "mps"
        if torch.backends.mps.is_available()
        else "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )
    print("device", device)

    # load model
    start_time = time.time()
    # load model with SDPA for using Flash Attention 2
    model = SentenceTransformer(
        model_id,
        # model_kwargs={"attn_implementation": "sdpa"},  # sdpa will be used by default if available
        model_card_data=SentenceTransformerModelCardData(
            language="en",
            license="apache-2.0",
            model_name="BGE base ArgillaSDK Matryoshka",
        ),
    )

    elapsed_time = time.time() - start_time
    print("model loading time", elapsed_time)

    # Define the loss
    inner_train_loss = TripletLoss(model)
    train_loss = MatryoshkaLoss(
        model, inner_train_loss, matryoshka_dims=matryoshka_dimensions
    )

    # define training arguments
    args = SentenceTransformerTrainingArguments(
        output_dir=finetuner_config[
            "output_dir"
        ],  # "bge-base-argilla-sdk-matryoshka", # output directory and hugging face model ID
        num_train_epochs=finetuner_config["num_train_epochs"],  # 3,  # number of epochs
        per_device_train_batch_size=finetuner_config[
            "per_device_train_batch_size"
        ],  # 8,             # train batch size
        gradient_accumulation_steps=finetuner_config[
            "gradient_accumulation_steps"
        ],  # 4,             # for a global batch size of 512
        per_device_eval_batch_size=finetuner_config[
            "per_device_eval_batch_size"
        ],  # 4,              # evaluation batch size
        warmup_ratio=finetuner_config[
            "warmup_ratio"
        ],  # 0.1,                           # warmup ratio
        learning_rate=finetuner_config[
            "learning_rate"
        ],  # 2e-5,                         # learning rate, 2e-5 is a good value
        lr_scheduler_type=finetuner_config[
            "lr_scheduler_type"
        ],  # "cosine",                 # use constant learning rate scheduler
        # NOTE: In colab we can work with the optimizer at least, but neither tf32 nor bf16
        #    optim="adamw_torch_fused",                  # use fused adamw optimizer
        #    tf32=True,                                  # use tf32 precision
        #    bf16=True,                                  # use bf16 precision
        # batch_sampler=BatchSamplers.NO_DUPLICATES,  # MultipleNegativesRankingLoss benefits from no duplicate samples in a batch
        eval_strategy=finetuner_config[
            "eval_strategy"
        ],  # "epoch",                      # evaluate after each epoch
        save_strategy=finetuner_config[
            "save_strategy"
        ],  # "epoch",                      # save after each epoch
        logging_steps=finetuner_config[
            "logging_steps"
        ],  # 5,                            # log every 10 steps
        save_total_limit=finetuner_config[
            "save_total_limit"
        ],  # 1,                         # save only the last 3 models
        load_best_model_at_end=finetuner_config[
            "load_best_model_at_end"
        ],  # True,                # load the best model when training ends
        metric_for_best_model=finetuner_config[
            "metric_for_best_model"
        ],  # "eval_dim_512_cosine_ndcg@10",  # Optimizing for the best ndcg@10 score for the 512 dimension
    )

    # prepare trainer (requiring evaluator)
    evaluator = prepare_matryoshka_evaluator(
        train_dataset, test_dataset, matryoshka_dimensions
    )
    trainer = SentenceTransformerTrainer(
        model=model,  # bg-base-en-v1
        args=args,  # training arguments
        train_dataset=train_dataset.select_columns(
            finetuner_config["select_columns"]
        ),  # training dataset
        loss=train_loss,
        evaluator=evaluator,
    )

    # start training, the model will be automatically saved to the hub and the output directory
    start_time = time.time()
    trainer.train()
    elapsed_time = time.time() - start_time
    print("model tuning elapsed time", elapsed_time)

    # save the best model
    trainer.save_model(finetuner_config["output_dir"])
    print("best finetuned model saved to:", finetuner_config["output_dir"])

    # push model to hub
    # trainer.model.push_to_hub("bge-base-argilla-sdk-matryoshka")
    return finetuner_config["output_dir"]


"""
print('start')
doEmbederMatryoshkaTripletFinetune(finetuner_config)
print('success')
"""


@component
class EmbeddingModelMatryoshkaTripletFinetuner:
    """
    A component loading data and model, finetuning with MatryoshkaLoss, and saving the best model, and optinally push to huggingface.
    """

    @component.output_types(model_output_path=str)
    def run(self, embed_finetuner_config: dict):
        print("[EmbeddingModelMatryoshkaTripletFinetuner]")
        print("started")
        model_output_path = doEmbederMatryoshkaTripletFinetune(
            finetuner_config=embed_finetuner_config
        )
        print("completed")
        print("[EmbeddingModelMatryoshkaTripletFinetuner]")
        return {"model_output_path": model_output_path}


finetunertest = EmbeddingModelMatryoshkaTripletFinetuner()
result = finetunertest.run(finetuner_config_example)
print(result["model_output_path"])
