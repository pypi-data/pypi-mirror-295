from collections import defaultdict
from creao.core.component.util import creao_component
import concurrent.futures
from typing import Dict, List
import numpy as np
from creao.core.Endpoints import CreaoLLM
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances


class Dedup:
    def __init__(self):
        self.embedding_model = CreaoLLM()

    def get_embedding_vector(self, text):
        return self.embedding_model.invoke(text, "", component_id="embed")

    def list2vec(self, text_list, num_workers=100):
        def process_text(text):
            vector = self.get_embedding_vector(text)
            return text, vector

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(process_text, text_list))

        texts, embeddings = zip(*results)
        embeddings = np.array(embeddings)

        return list(texts), embeddings

    def clustering(self, embeddings, threshold=0.075):
        cosine_dist_matrix = cosine_distances(embeddings)

        agg_clustering = AgglomerativeClustering(
            n_clusters=None,
            metric="precomputed",
            linkage="complete",
            distance_threshold=threshold,
        )
        labels = agg_clustering.fit_predict(cosine_dist_matrix)

        return labels

    def execute(self, text_list: List[str]) -> List[str]:
        if len(text_list) < 2:
            return text_list
        try:
            texts, embeddings = self.list2vec(text_list)
        except Exception as e:
            print(f"dedupe list2vec with error: {e}")
            return text_list

        labels = self.clustering(embeddings)
        assert len(texts) == len(labels)
        # only keep the first text with duplicated label, and return the list[{text, drop}], where drop is a boolean
        exist_label = set()
        res = []
        for i in range(len(texts)):
            label = labels[i]
            if label in exist_label:
                continue
            else:
                exist_label.add(label)
                res.append(texts[i])
        return res
    
@creao_component
class DedupeComponent:
    def __init__(
        self,
        dedup_column: str,
        pipeline_id: str = "pipeline_id_default",
        component_name: str = "default",
        **kwargs,
    ):
        self.pipeline_id = pipeline_id
        self.dedup_column = dedup_column
        self.component_name = component_name
        self.llm = Dedup()

    def convert_to_dict_of_lists(
        self, data: List[Dict[str, str]]
    ) -> Dict[str, List[str]]:
        result = defaultdict(list)

        for entry in data:
            for key, value in entry.items():
                result[key].append(value)
        return result

    def run(
        self, chained_input: List[Dict[str, List[str]]]
    ) -> List[Dict[str, List[str]]]:
        """
        Deduplicate the input texts.

        Args:
            chained_input (List[Dict[str, str]]): Input from previous component.
        Returns:
            List[Dict[str, str]]: Deduplicated texts.
        """
        for single_chained_input in chained_input:
            assert (
                self.dedup_column in single_chained_input
            ), f"Column '{self.dedup_column}' not found in the input data."
            for key in single_chained_input:
                if key == self.dedup_column:
                    texts = single_chained_input[key]
                    dedupe_res = self.llm.execute(texts)
                    single_chained_input[key] = dedupe_res
        return chained_input
