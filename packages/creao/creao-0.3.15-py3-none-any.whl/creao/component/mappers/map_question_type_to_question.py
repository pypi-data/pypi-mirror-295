from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures
from creao.core.Endpoints import CreaoLLM


@component
class MapQuestionTypeToQuestion:
    """
    A component mapping question type to question
    """

    def __init__(
        self,
        type_of_questions: Dict[str, str],
        service: str = "default",
        pipeline_id: str = "pipeline_id_default",
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        self.type_of_questions = type_of_questions
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="question generation assistant",
                bot_content="You are given a list of interests and a passage. Your task is to generate questions that align with the interests and the passage. Reflective Thinking: Before you generate the final list of questions, pause to examine your assumptions, biases, and the mental models that the interests might use. Consider how the interests influence what they find interesting, and how they prioritize topics. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, question_mapping: List[Dict[str, str]], chunk: str, file_name: str):
        """
        Map question type to question
        :param question_type: The question type to map
        :return: The question
        """

        # print("generating question with minimax")
        def process_question_type(item):
            interest_questions = []
            for q_type in item["q_type"]:
                if q_type.lower() in self.type_of_questions:
                    if self.service == "default":
                        prompt = extract_questions_prompt.format(
                            interest=item["interest"],
                            types=self.type_of_questions[q_type.lower()],
                            file_name=file_name,
                            passage=chunk,
                        )
                        json_schema = {
                            "generated_questions": {
                                "type": "array",
                                "items": {"type": "string"},
                            }
                        }
                        response_json = self.llm.invoke(
                            prompt,
                            json_schema,
                            "MapQuestionTypeToQuestion",
                            self.pipeline_id,
                        )

                        try:
                            raw_answer = json.loads(response_json["reply"])
                        except Exception as e:
                            print(
                                f"MapQuestionTypeToQuestion json decode error:{e}, with response_json:{response_json}"
                            )
                            raw_answer = {"generated_questions": []}
                        if "generated_questions" in raw_answer:
                            questions = raw_answer["generated_questions"]
                        else:
                            questions = []
                    elif self.service == "openai":
                        questions = self.generator.generate_questions(
                            file_name,
                            chunk,
                            item["interest"],
                            self.type_of_questions[q_type.lower()],
                        )
                    interest_questions.extend(questions)
            return interest_questions

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            raw_questions = [
                question
                for result in executor.map(process_question_type, question_mapping)
                for question in result
            ]
            questions = [item for item in raw_questions if item != []]
        documents = []
        for question in questions:
            doc = Document(
                content=question, meta={"file_name": file_name, "chunk": chunk}
            )
            documents.append(doc)
        # print("generating question with minimax done")
        return {"documents": documents}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(
            self,
            type_of_questions=self.type_of_questions,
            service=self.service,
            pipeline_id=self.pipeline_id,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MapQuestionTypeToQuestion":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)
