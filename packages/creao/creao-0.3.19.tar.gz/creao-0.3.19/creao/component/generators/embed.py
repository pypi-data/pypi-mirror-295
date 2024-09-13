from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict
from openai import OpenAI
from haystack.utils import (
    Secret,
    deserialize_callable,
    deserialize_secrets_inplace,
    serialize_callable,
)


@component
class Embed:
    """
    Embed text using a pre-trained model from NVIDIA.

    ### Usage example
    ```python
        from component.generators.embed import Embed
        embed = Embed(service="NVIDIA")
        response = embed.run("how are you")
    ```
    """

    def __init__(
        self,
        service: str,
        encoding_format: str = "float",
    ):
        """
        Initialize the component.
        :param service: The service to use for embedding. Currently only "NVIDIA" is supported.
        :param encoding_format: The encoding format to use. Currently only "float" is supported.

        """
        api_key = ""
        base_url = ""
        self.encoding_format = encoding_format
        self.service = service
        if service == "NVIDIA":
            api_key = Secret.from_env_var("BUILD_NVIDIA_API_KEY")
            base_url = "https://ai.api.nvidia.com/v1/retrieval/nvidia"
            self.model = "NV-Embed-QA"
        else:
            raise ValueError(f"Unsupported service '{service}'")
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key.resolve_value(),
        )

    @component.output_types(embeddings=List[float])
    def run(self, text: str):
        embeddings = (
            self.client.embeddings.create(
                input=[text],
                model=self.model,
                encoding_format=self.encoding_format,
                extra_body={"input_type": "query", "truncate": "NONE"},
            )
            .data[0]
            .embedding
        )
        return {"embeddings": embeddings}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(
            self,
            service=self.service,
            encoding_format=self.encoding_format,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Embed":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)
