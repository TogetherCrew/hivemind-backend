from unittest import TestCase

from llama_index.core import MockEmbedding
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from tc_hivemind_backend.qdrant_vector_access import QDrantVectorAccess


class TestQdrantVectorAccess(TestCase):
    def test_init(self):
        expected_collection_name = "sample_collection"
        qdrant_vector_access = QDrantVectorAccess(
            collection_name=expected_collection_name,
            testing=True,
        )

        self.assertEqual(qdrant_vector_access.collection_name, expected_collection_name)
        self.assertIsInstance(qdrant_vector_access.embed_model, MockEmbedding)

    def test_setup_index(self):
        qdrant_vector_access = QDrantVectorAccess(
            collection_name="sample_collection",
            testing=True,
        )
        vector_store = qdrant_vector_access.setup_qdrant_vector_store()
        self.assertIsInstance(vector_store, QdrantVectorStore)

    def test_load_index(self):
        qdrant_vector_access = QDrantVectorAccess(
            collection_name="sample_collection",
            testing=True,
        )
        index = qdrant_vector_access.load_index()
        self.assertIsInstance(index, VectorStoreIndex)
