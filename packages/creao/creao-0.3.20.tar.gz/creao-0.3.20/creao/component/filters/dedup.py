from typing import Any, Dict, List
from creao.core.pipeline import creao_component
from creao.core.Dedup import Dedup


@creao_component
class Deduplication:
    input_schema = {"contents": List[str]}
    output_schema = {"contents": List[str]}

    def __init__(self):
        pass

    def warm_up(self):
        """
        Initializes the component.
        """
        if not hasattr(self, "dedup"):
            self.dedup = Dedup()

    def run(self, chained_input):
        if not hasattr(self, "dedup"):
            raise RuntimeError(
                "The embedding model has not been loaded. Please call warm_up() before running."
            )
        res = self.dedup.execute(input_texts)
        dedup_list = []
        for item in res:
            dedup_list.append(item)
        return {"dedup_list": dedup_list}
