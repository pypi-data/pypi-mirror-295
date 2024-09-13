from typing import List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures


@component
class IntelligentFilter:
    def __init__(
        self, service: str = "default", pipeline_id: str = "pipeline_id_default"
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="question intelligence filter assistant",
                bot_content="You are given a question. Your task is to determine the intelligence of the question. Reflective Thinking: Before you generate the final decision, pause to examine your assumptions, biases, and the mental models that the question might use. Consider how the question influences the intelligence of the question, and how they prioritize the intelligence. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.intelligent_question_filter = Intelligent_Question_Filter()

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        # print("filtering intelligence with minimax")
        if len(documents) == 0:
            return {"outputs": []}
        inputs = [doc.content for doc in documents]
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]

        def filter_question(question):
            if self.service == "default":
                prompt = intelligent_question_filter_prompt.format(
                    question=question, file_name=file_name, passage=chunk
                )
                json_schema = {"Type_of_question": {"type": "string"}}
                response_json = self.llm.invoke(
                    prompt, json_schema, "IntelligentFilter", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"IntelligentFilter json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"Type_of_question": ""}
                filter_flag = raw_answer
            else:
                filter_flag = self.intelligent_question_filter.execute(
                    question, file_name, chunk
                )
            return question if filter_flag["Type_of_question"] == "Type_A" else None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            filtered_questions = list(executor.map(filter_question, inputs))

        # Filter out any None values from the list of filtered questions
        questions = [q for q in filtered_questions if q is not None]
        docs = []
        for question in questions:
            doc = Document(
                content=question, meta={"file_name": file_name, "chunk": chunk}
            )
            docs.append(doc)
        # print("filtering intelligence with minimax done")
        return {"documents": docs}

    def to_dict(self) -> dict:
        return default_to_dict(self, service=self.service, pipeline_id=self.pipeline_id)

    @classmethod
    def from_dict(cls, data: dict) -> "IntelligentFilter":
        return default_from_dict(cls, data)
