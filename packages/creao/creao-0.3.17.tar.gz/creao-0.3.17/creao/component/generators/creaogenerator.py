from typing import Any, Dict, List
from creao.core.Endpoints import CreaoLLM
from haystack import component, default_from_dict, default_to_dict
import json


@component
class CreaoGenerator:
    def __init__(self):
        self.llm = CreaoLLM()

    @component.output_types(replies=List[str], meta=List[Dict[str, Any]])
    def run(self, prompt: str):
        response_raw = self.llm.invoke(prompt, "")
        i = 0
        while i < 3:
            if "reply" in response_raw:
                break
            response_raw = self.llm.invoke(prompt, "")
            i += 1
        if "reply" not in response_raw:
            return {"replies": [""], "meta": [{"service": "minimax"}]}
        return {"replies": [response_raw["reply"]], "meta": [{"service": "minimax"}]}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreaoGenerator":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)
