from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures
from creao.core.Endpoints import CreaoLLM


@component
class MapInterestToQuestionType:
    """
    A component mapping interest to question type
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
                bot_name="question type extraction assistant",
                bot_content="You are given a list of interests and a list of types of questions. Your task is to identify the types of questions that can be asked based on the given interests. Reflective Thinking: Before you generate the final list of types of questions, pause to examine your assumptions, biases, and the mental models that the interests might use. Consider how the interests influence the types of questions that can be asked, and how they prioritize the types of questions. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.generator = Generator()

    @component.output_types(question_mapping=List[Dict[str, str]])
    def run(self, documents: List[Document]):
        """
        Map interest to question type
        :param interest: The interest to map
        :return: The question type
        """
        # print("mapping interest to question type with minimax")
        if len(documents) == 0:
            return {"question_mapping": []}
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        interests = [doc.content for doc in documents]

        def process_interest(interest):
            if self.service == "default":
                prompt = extract_compatible_question_type_prompt.format(
                    interest=interest,
                    types="\n".join(list(self.type_of_questions.values())),
                    file_name=file_name,
                    passage=chunk,
                )
                json_schema = {
                    "reasoning": {"type": "string"},
                    "list_of_extractable_types_of_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                }
                response_json = self.llm.invoke(
                    prompt, json_schema, "MapInterestToQuestionType", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"MapInterestToQuestionType json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"list_of_extractable_types_of_questions": []}
                if "list_of_extractable_types_of_questions" in raw_answer:
                    mapping = raw_answer["list_of_extractable_types_of_questions"]
                else:
                    mapping = []
            elif self.service == "openai":
                mapping = self.generator.extract_compatible_question_type(
                    interest, list(self.type_of_questions.values()), file_name, chunk
                )["list_of_extractable_types_of_questions"]
            return {"interest": interest, "q_type": [m.lower() for m in mapping]}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            question_mapping = list(executor.map(process_interest, interests))
        # print("mapping interest to question type with minimax done")
        return {"question_mapping": question_mapping}

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
    def from_dict(cls, data: Dict[str, Any]) -> "MapInterestToQuestionType":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)
