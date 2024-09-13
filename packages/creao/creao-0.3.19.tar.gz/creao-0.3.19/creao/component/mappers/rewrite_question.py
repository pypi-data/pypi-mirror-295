from typing import Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures
from creao.core.Endpoints import CreaoLLM


@component
class RewriteQuestion:
    def __init__(
        self, service: str = "default", pipeline_id: str = "pipeline_id_default"
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="question rewriter assistant",
                bot_content="You are given a question. Your task is to rewrite the question in a conversational manner. Reflective Thinking: Before you generate the final list of questions, pause to examine your assumptions, biases, and the mental models that the question might use. Consider how the question influences the relevance to the passage, and how they prioritize the relevance. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        # print("rewriting question with minimax")
        if len(documents) == 0:
            return {"outputs": []}
        questions = [doc.content for doc in documents]
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]

        def process_question(question):
            if self.service == "default":
                prompt = conversational_re_write_prompt.format(
                    question=question, file_name=file_name, passage=chunk
                )
                json_schema = {"re_written_question": {"type": "string"}}
                response_json = self.llm.invoke(
                    prompt, json_schema, "RewriteQuestion", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"RewriteQuestion json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"re_written_question": ""}
                return raw_answer["re_written_question"]
            else:
                return self.generator.conversational_re_write(
                    question, file_name, chunk
                )["re_written_question"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            outputs = list(executor.map(process_question, questions))
            # filter out question with empty string
            outputs = [question for question in outputs if question]
        docs = []
        for question in outputs:
            doc = Document(
                content=question, meta={"file_name": file_name, "chunk": chunk}
            )
            docs.append(doc)
        # print("rewriting question with minimax done")
        return {"documents": docs}

    def to_dict(self) -> dict:
        return default_to_dict(self, service=self.service, pipeline_id=self.pipeline_id)

    @classmethod
    def from_dict(cls, data: dict) -> "RewriteQuestion":
        return default_from_dict(cls, data)


@component
class PersonaToWritingStyle:
    def __init__(
        self, service: str = "default", pipeline_id: str = "pipeline_id_default"
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="persona to writing style assistant",
                bot_content="You are given a persona. Your task is to generate the writing style of the persona. Reflective Thinking: Before you generate the final list of writing styles, pause to examine your assumptions, biases, and the mental models that the persona might use. Consider how the persona influences the writing style, and how they prioritize the writing style. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.generator = Generator()

    @component.output_types(outputs=List[Dict[str, str]])
    def run(self, personas: List[str]):
        # print("generating writing style with minimax")
        writing_styles = []
        for persona in personas:
            if self.service == "default":
                prompt = extract_writing_style.format(persona=persona)
                json_schema = {"writing_style": {"type": "string"}}
                response_json = self.llm.invoke(
                    prompt, json_schema, "PersonaToWritingStyle", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"PersonaToWritingStyle json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"writing_style": ""}
                style = raw_answer
            else:
                style = json.loads(self.generator.writing_style(persona).strip())
            if style["writing_style"] != "":
                writing_styles.append(
                    {"persona": persona, "style": style["writing_style"]}
                )
        # print("generating writing style with minimax done")
        return {"outputs": writing_styles}

    def to_dict(self) -> dict:
        return default_to_dict(self, service=self.service, pipeline_id=self.pipeline_id)

    @classmethod
    def from_dict(cls, data: dict) -> "PersonaToWritingStyle":
        return default_from_dict(cls, data)


@component
class RewriteQuestionByPersona:
    def __init__(
        self, service: str = "default", pipeline_id: str = "pipeline_id_default"
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="question rewriter assistant",
                bot_content="You are given a question and a persona. Your task is to rewrite the question in the writing style of the persona. Reflective Thinking: Before you generate the final list of questions, pause to examine your assumptions, biases, and the mental models that the question might use. Consider how the question influences the relevance to the passage, and how they prioritize the relevance. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer",
            )
        elif self.service == "openai":
            self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document], writing_styles: List[Dict[str, str]]):
        # print("rewriting question by persona with minimax")
        questions = [doc.content for doc in documents]

        def process_question(question):
            question_variants = []
            for style in writing_styles:
                if self.service == "default":
                    prompt = persona_rewrite_prompt.format(
                        persona=style["style"], question=question
                    )
                    json_schema = {"new_question": {"type": "string"}}
                    response_json = self.llm.invoke(
                        prompt,
                        json_schema,
                        "RewriteQuestionByPersona",
                        self.pipeline_id,
                    )
                    try:
                        raw_answer = json.loads(response_json["reply"])
                    except Exception as e:
                        print(
                            f"RewriteQuestionByPersona json decode error:{e}, with response_json:{response_json}"
                        )
                        raw_answer = {"new_question": ""}
                    re_write = raw_answer["new_question"]
                else:
                    re_write = self.generator.persona_rewrite(style["style"], question)
                if re_write != "":
                    question_variants.append(
                        {
                            "new_question": re_write,
                            "style": style,
                            "original_question": question,
                        }
                    )
            return question_variants

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            re_written_questions = [
                variant
                for result in executor.map(process_question, questions)
                for variant in result
            ]
        docs = []
        for question in re_written_questions:
            doc = Document(
                content=question["new_question"],
                meta={
                    "file_name": documents[0].meta["file_name"],
                    "chunk": documents[0].meta["chunk"],
                    "style": question["style"],
                    "original_question": question["original_question"],
                },
            )
            docs.append(doc)
        # print("rewriting question by persona with minimax done")
        return {"documents": docs}

    def to_dict(self) -> dict:
        return default_to_dict(self, service=self.service, pipeline_id=self.pipeline_id)

    @classmethod
    def from_dict(cls, data: dict) -> "RewriteQuestionByPersona":
        return default_from_dict(cls, data)
