from typing import Dict, List
from creao.core.Endpoints import OpenAILLM, CreaoLLM
import json
from pydantic import BaseModel
from creao.core.pipeline import creao_component
from jinja2 import Template

extract_poi_prompt_str = """\
You are given a Persona and a Passage. Your task is to immitate the persona and create a list interesting topics from the given passage.

<Persona>
{{persona}}
</Persona>

<Passage>
The following information is from a file with the title "{{file_name}}".

{{passage}}
</Passage>

Answer format - Generate a json with the following fields
- "list_of_interest": [<fill with 1-5 word desription>]

Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches. Show your thinking before giving an answer.
"""


class POISchema(BaseModel):
    list_of_interest: list[str]


@creao_component
class ExtractPOI:
    def __init__(
        self,
        custom_prompt: str = None,
        service: str = "default",
        pipeline_id: str = "pipeline_id_default",
    ):
        self.custom_prompt = custom_prompt
        self.pipeline_id = pipeline_id
        self.service = service
        if self.service == "default":
            self.llm = CreaoLLM(
                bot_name="point of interests extraction assistant",
                bot_content="You are given a Persona and a Passage. Your task is to adopt the given Persona and reflect deeply on the content of the Passage. Then, create a list of interesting topics from the Passage that align with the Persona's unique perspective and thinking style.Reflective Thinking: Before you generate the final list of topics, pause to examine your assumptions, biases, and the mental models that the Persona might use. Consider how the Persona's perspective influences what they find interesting, and how they prioritize topics. Be open to learning from previous similar tasks and improving the outcome. Explicitly share your reflective thought process before giving the final answer.",
            )
        elif self.service == "openai":
            self.llm = OpenAILLM()

    def run(self, chained_input: List[Dict[str, str]]) -> List[Dict[str, str]]:
        prompt_template = Template(extract_poi_prompt_str)
        # print("extracting points of interest with minimax")
        prompt_list = [prompt_template.render(item) for item in chained_input]
        res_list = []
        for prompt in prompt_list:
            if self.service == "default":
                response_json = self.llm.invoke(
                    prompt,
                    {
                        "list_of_interest": {
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                    "ExtractPOI",
                    self.pipeline_id,
                )
                try:
                    raw_answer = json.loads(response_json["reply"])
                except Exception as e:
                    print(
                        f"ExtractPOI json decode error:{e}, response_json:{response_json}"
                    )
                    raw_answer = {"list_of_interest": []}
            elif self.service == "openai":
                try:
                    raw_answer = json.loads(self.llm.invoke(prompt, POISchema))
                except Exception as e:
                    print(f"ExtractPOI json decode error:{e}")
                    raw_answer = {"list_of_interest": []}
            list_of_interest = raw_answer["list_of_interest"]
            for interest in list_of_interest:
                res_list.append({"interest": interest})
        return res_list


# extract_poi = ExtractPOI()
# res = extract_poi.run({"personas":["I am a student", "I am a teacher"], "file_name":"file1", "chunk":"chunk1"})
# print(res)
