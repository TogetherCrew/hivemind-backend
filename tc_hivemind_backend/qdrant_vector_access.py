from llama_index.core import MockEmbedding
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from tc_hivemind_backend.db.qdrant import QdrantSingleton
from tc_hivemind_backend.embeddings import CohereEmbedding


class QDrantVectorAccess:
    def __init__(self, collection_name: str, testing: bool = False, **kwargs) -> None:
        """
        the class to access VectorStoreIndex from qdrant vector db

        Paramters
        -----------
        collection_name : str
            the qdrant collection name
        testing : bool
            work with mock LLM and mock embedding model for testing purposes
        **kwargs :
            embed_model : BaseEmbedding
                an embedding model to use for all tasks defined in this class
                default is `CohereEmbedding`
        """
        self.collection_name = collection_name
        self.embed_model: BaseEmbedding = kwargs.get("embed_model", CohereEmbedding())

        if testing:
            self.embed_model = MockEmbedding(embed_dim=1024)

    def setup_qdrant_vector_store(self) -> QdrantVectorStore:
        client = QdrantSingleton.get_instance().client
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=self.collection_name,
        )
        return vector_store

    def load_index(self, **kwargs) -> VectorStoreIndex:
        """
        load the llama_index.VectorStoreIndex

        Parameters
        -----------
        **kwargs :
            embed_model : BaseEmbedding
                the embedding model to use
                default is the one set when initializing the class
        """
        embed_model: BaseEmbedding = kwargs.get("embed_model", self.embed_model)
        vector_store = self.setup_qdrant_vector_store()
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
        )
        return index
