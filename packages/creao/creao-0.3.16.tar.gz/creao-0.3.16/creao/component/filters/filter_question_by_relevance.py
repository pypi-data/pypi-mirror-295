from typing import List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures
from creao.core.Endpoints import CreaoLLM


@component
class RelevanceFilter:
    def __init__(
        self,
        flag: str = "not useful",
        service="default",
        pipeline_id: str = "pipeline_id_default",
    ):
        self.flag = flag
        self.pipeline_id = pipeline_id
        self.service = service
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="question relevance filter assistant",
                bot_content="You are given a question and a passage. Your task is to determine the relevance of the question to the passage. Reflective Thinking: Before you generate the final decision, pause to examine your assumptions, biases, and the mental models that the question might use. Consider how the question influences the relevance to the passage, and how they prioritize the relevance. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.relevance_filter = Relevance_Filter()

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        # print("filtering relevance with minimax")
        if len(documents) == 0:
            return {"documents": []}
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        questions = [doc.content for doc in documents]
        filter_flags = []

        def process_question(question):
            if self.service == "default":
                prompt = filter_relevance_prompt.format(
                    question=question,
                    file_name=file_name,
                    passage=chunk,
                )
                json_schema = {
                    "Reasoning": {"type": "string"},
                    "Your_Decision": {"type": "string"},
                }
                response_json = self.llm.invoke(
                    prompt, json_schema, "RelevanceFilter", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"RelevanceFilter json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"Your_Decision": "not useful"}
                flag = raw_answer
            elif self.service == "openai":
                flag = self.relevance_filter.execute(question, file_name, chunk)
            return {"question": question, "flag": flag}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_question, questions))

        filter_flags.extend(results)

        # Step 7: Keep only the relevant questions
        relevant_questions = [
            item["question"]
            for item in filter_flags
            if item["flag"]["Your_Decision"].lower() != "not useful"
        ]
        docs = []
        for question in relevant_questions:
            doc = Document(
                content=question, meta={"file_name": file_name, "chunk": chunk}
            )
            docs.append(doc)
        # print("filtering relevance with minimax done")
        return {"documents": docs}

    def to_dict(self) -> dict:
        return default_to_dict(
            self, flag=self.flag, service=self.service, pipeline_id=self.pipeline_id
        )

    @classmethod
    def from_dict(cls, data: dict) -> "RelevanceFilter":
        return default_from_dict(cls, data)
