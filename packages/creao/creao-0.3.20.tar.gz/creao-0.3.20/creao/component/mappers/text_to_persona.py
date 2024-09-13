from typing import List
from haystack import component, default_from_dict, default_to_dict
from creao.core.Generator import *
from creao.core.Endpoints import CreaoLLM, OpenAILLM
import concurrent.futures


class Personas(BaseModel):
    personas: list[str]


extract_persona = """\
Who is likely to {action} the text?

<text>
{text}
</text>

Answer format - Generate a json with the following fields
- "list_of_persona": [<fill>]

Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches. Show your thinking before giving an answer.
the generated persona should be in detail like
<example>
    Lena is a data scientist with a strong background in natural language processing. She has experience working with large language models and is keen on exploring how LangChain can automate and enhance various text-based workflows. Lena often dives deep into technical details and enjoys experimenting with new tools and techniques to optimize her models' performance.
</example>
"""


@component
class TextToPersona:
    def __init__(
        self, service: str = "default", pipeline_id: str = "pipeline_id_default"
    ):
        self.service = service
        self.pipeline_id = pipeline_id
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="persona generation assistant",
                bot_content="You are given a text. Your task is to generate a persona based on the given text. Reflective Thinking: Before you generate the final persona, pause to examine your assumptions, biases, and the mental models that the text might use. Consider how the text influences the persona, and how they prioritize the persona. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.llm = OpenAILLM()

    @component.output_types(personas=List[str])
    def run(self, text: str):
        actions = ["read", "write", "like", "dislike"]

        def process_text(action):
            if self.service == "default":
                prompt = extract_persona.format(action=action, text=text)
                json_schema = {
                    "personas": {"type": "array", "items": {"type": "string"}}
                }
                response_json = self.llm.invoke(
                    prompt, json_schema, "TextToPersona", self.pipeline_id
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"TextToPersona json decode error:{e}, with response_json:{response_json}"
                    )
                    raw_answer = {"personas": []}
                return raw_answer["personas"]
            elif self.service == "openai":
                return json.loads(self.llm.invoke(prompt, Personas))["personas"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            raw_personas = [
                persona
                for result in executor.map(process_text, actions)
                for persona in result
            ]
        personas = []
        for item in raw_personas:
            if item != []:
                personas.append(item)
        return {"personas": personas}

    def to_dict(self) -> dict:
        return default_to_dict(self, service=self.service, pipeline_id=self.pipeline_id)

    @classmethod
    def from_dict(cls, data: dict) -> "TextToPersona":
        return default_from_dict(cls, data)
