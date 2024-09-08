from typing import Dict
from creao.component.generators.creaogenerator import CreaoGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
import gradio as gr


class RAG(object):
    def __init__(
        self,
        chunk: list[str],
        embedding_model_id: str = "BAAI/bge-base-en-v1.5",
        service="default",
    ) -> None:
        """
        :param chunk: The chunk to be stored in the vector database.
        """
        docs = [
            Document(content=item, meta={"file_path": "document.md"}) for item in chunk
        ]
        text_embedder = SentenceTransformersTextEmbedder(model=embedding_model_id)
        text_embedder.warm_up()
        doc_embedder = SentenceTransformersDocumentEmbedder(model=embedding_model_id)
        doc_embedder.warm_up()
        # store all chunk in a vector database
        document_store = InMemoryDocumentStore()
        docs_with_embeddings = doc_embedder.run(docs)
        document_store.write_documents(docs_with_embeddings["documents"])
        # create a retriever from the vector database
        retriever = InMemoryEmbeddingRetriever(document_store)
        # build the retriever pipeline with haystack
        template = """
        Given the following information, answer the question.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer:
        """
        prompt_builder = PromptBuilder(template=template)
        if service == "default":
            llm = CreaoGenerator()
        elif service == "openai":
            llm = OpenAIGenerator(model="gpt-4o-mini")
        basic_rag_pipeline = Pipeline()
        # Add components to your pipeline
        basic_rag_pipeline.add_component("text_embedder", text_embedder)
        basic_rag_pipeline.add_component("retriever", retriever)
        basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
        basic_rag_pipeline.add_component("llm", llm)
        # Now, connect the components to each other
        basic_rag_pipeline.connect(
            "text_embedder.embedding", "retriever.query_embedding"
        )
        basic_rag_pipeline.connect("retriever", "prompt_builder.documents")
        basic_rag_pipeline.connect("prompt_builder", "llm")
        self.basic_rag_pipeline = basic_rag_pipeline

    def query_response(self, question: str) -> str:
        response = self.basic_rag_pipeline.run(
            {
                "text_embedder": {"text": question},
                "prompt_builder": {"question": question},
            },
            include_outputs_from={"retriever"},
        )
        return response

    def generate_gradio_interface(self, demo_examples: list[str] = []):
        def yes_man(message, history):
            response = self.basic_rag_pipeline.run(
                {
                    "text_embedder": {"text": message},
                    "prompt_builder": {"question": message},
                }
            )
            return response["llm"]["replies"][0]

        gr.ChatInterface(
            yes_man,
            chatbot=gr.Chatbot(height=300),
            textbox=gr.Textbox(placeholder="Ask me question", container=False, scale=7),
            title="Copilot for building Creao Component & Pipeline",
            description="Ask me question",
            theme="soft",
            examples=demo_examples,
            cache_examples=True,
            retry_btn=None,
            undo_btn="Delete Previous",
            clear_btn="Clear",
        ).launch(share=True)
