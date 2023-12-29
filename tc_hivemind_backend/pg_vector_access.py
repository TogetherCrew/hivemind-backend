import logging
import time

from llama_index import Document, MockEmbedding, ServiceContext, StorageContext
from llama_index.embeddings import BaseEmbedding, OpenAIEmbedding
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import BaseNode
from llama_index.vector_stores import PGVectorStore
from tc_hivemind_backend.db.credentials import load_postgres_credentials
from tc_hivemind_backend.db.utils.delete_data import delete_data
from tc_hivemind_backend.db.utils.model_hyperparams import load_model_hyperparams


class PGVectorAccess:
    def __init__(self, table_name: str, dbname: str, testing: bool = False) -> None:
        """
        the class to access VectorStoreIndex from postgres

        Parameters
        -----------
        table_name : str
            the table name to access in postgres for vectors
        dbname : str
            the database to save the data under
        testing : bool
            work with mock LLM and mock embedding model for testing purposes
        """
        self.table_name = table_name
        self.dbname = dbname
        self.testing = testing

        self.llm: str | None
        self.embed_model: BaseEmbedding
        if not self.testing:
            self.embed_model = OpenAIEmbedding()
            self.llm = "default"
        else:
            self.embed_model = MockEmbedding(embed_dim=1024)
            self.llm = None

    def setup_pgvector_index(self, embed_dim: int = 1024):
        """
        setup postgres vectore index

        Parameters
        -----------
        embed_dim : int
            the embed dimension
            default is 1024 which is the cohere dimension
        """
        postgres_creds = load_postgres_credentials()

        vector_store = PGVectorStore.from_params(
            database=self.dbname,
            host=postgres_creds["host"],
            password=postgres_creds["password"],
            port=postgres_creds["port"],
            user=postgres_creds["user"],
            table_name=self.table_name,
            embed_dim=embed_dim,
        )
        return vector_store

    def save_documents(
        self,
        community_id: str,
        documents: list[Document],
        node_parser: SimpleNodeParser | None = None,
        **kwargs,
    ) -> None:
        """
        save documents in postgres database

        Parameters
        -----------
        community_id : str
            the community id for the case of loggging
        documents : list[llama_index.Document]
            list of llama_idex documents
        node_parser : SimpleNodeParser | None
            get the node_parser
            default is None, meaning it would configure it with default values
        **kwargs :
            max_request_per_minute : int | None
                the maximum possible request count per limit which is the openai limits
                if `None` it wouldn't do a sleep
            embed_dim : int
                to configure the embedding dimension
                default is set to be 1024 which is the cohere embedding dimension
            max_request_per_day : int
                the maximum request count per day
            embed_model : llama_index.embeddings.base.BaseEmbedding
                to pass the embedding model
                default will be the OpenAIEmbedding
            batch_info : str
                the information about the batch number that the loop is within
            deletion_query : str
                the query to delete some documents
        """
        msg = f"COMMUNITYID: {community_id} "

        max_request_per_minute = kwargs.get("max_request_per_minute")
        max_request_per_day = kwargs.get("max_request_per_day")
        embed_dim: int = kwargs.get("embed_dim", 1024)
        self.embed_model = kwargs.get("embed_model", self.embed_model)
        deletion_query = kwargs.get("deletion_query", "")
        batch_info = kwargs.get("batch_info", "")

        node_parser = node_parser or SimpleNodeParser.from_defaults()

        nodes = node_parser.get_nodes_from_documents(documents)

        for idx, node in enumerate(nodes):
            self._process_embedding(
                node,
                idx,
                len(nodes),
                msg=msg,
                max_request_per_day=max_request_per_day,
                max_request_per_minute=max_request_per_minute,
                batch_info=batch_info,
            )

        vector_store = self.setup_pgvector_index(embed_dim)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = self._create_service_context(node_parser)
        self._handle_deletion(deletion_query, msg)
        self._save_embedded_documents(nodes, service_context, storage_context, msg)

    def save_documents_in_batches(
        self,
        community_id: str,
        documents: list[Document],
        batch_size: int = 100,
        **kwargs,
    ):
        """
        save the documents in batches in postgresql database

        Parameters
        -----------
        community_id : str
            the community id for the logging
        documents : list[llama_index.Document]
            list of llama_idex documents
        batch_size : int
            the batch size
        **kwargs :
            node_parser : SimpleNodeParser | None
                get the node_parser
                default is None, meaning it would configure it with default values
            max_request_per_minute : int | None
                the maximum possible request count per limit which is the openai limits
                if `None` it wouldn't do a sleep
            embed_dim : int
                to configure the embedding dimension
                default is set to be 1024 which is open ai embedding dimension
            max_request_per_day : int
                the maximum request count per day
            embed_model : llama_index.embeddings.base.BaseEmbedding
                to pass the embedding model
                default will be the OpenAIEmbedding
            deletion_query : str
                the query to delete some documents
        """
        node_parser = kwargs.get("node_parser")

        msg = f"COMMUNITYID: {community_id} "
        logging.info(f"{msg}Starting embedding and saving batch job")
        for batch_idx, current_batch in enumerate(range(0, len(documents), batch_size)):
            batch_info = (
                f"{msg}Batch {batch_idx + 1}/{(len(documents) // batch_size) + 1}"
            )
            self.save_documents(
                community_id,
                documents[current_batch : current_batch + batch_size],
                node_parser=node_parser,
                batch_info=batch_info,
                **kwargs,
            )

    def load_index(self, **kwargs) -> VectorStoreIndex:
        """
        load the llama_index.VectorStoreIndex

        Parameters
        -----------
        **kwargs :
            embed_dim : int
                to configure the embedding dimension
        """
        _, embedding_dim = load_model_hyperparams()

        embed_dim: int = embedding_dim
        if "embed_dim" in kwargs:
            embed_dim = kwargs["embed_dim"]

        vector_store = self.setup_pgvector_index(embed_dim)
        service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embed_model,
        )
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, service_context=service_context
        )
        return index

    def _process_embedding(
        self, node: BaseNode, idx: int, total_nodes: int, **kwargs
    ) -> None:
        """
        compute embeddings for one node (assigning to variable property)
        """
        msg = kwargs.get("msg", "")
        max_request_per_minute = kwargs.get("max_request_per_minute")
        max_request_per_day = kwargs.get("max_request_per_day")
        batch_info = kwargs.get("batch_info", "")

        logging.info(f"{batch_info} | Doing embedding {idx + 1}/{total_nodes}")
        node.embedding = self.embed_model.get_text_embedding(node.text)

        if max_request_per_day and idx % max_request_per_day:
            logging.info(f"{msg}Sleeping for 24 hours to avoid per day rate limits!")
            time.sleep(24 * 60 * 60 + 1)

        if (
            max_request_per_minute
            and idx % max_request_per_minute
            and idx != 0
            and idx != total_nodes
        ):
            logging.info(f"{msg}Sleeping to avoid per minute rate limits!")
            time.sleep(61)

    def _delete_documents(self, deletion_query: str) -> None:
        """
        delete documents with specific ids

        Parameters
        ------------
        deletion_query : str
            the query to delete the data
        """
        delete_data(deletion_query=deletion_query, dbname=self.dbname)

    def _save_embedded_documents(
        self,
        nodes: list[BaseNode],
        service_context: ServiceContext,
        storage_context: StorageContext,
        msg: str,
    ) -> None:
        logging.info(f"{msg}Saving the embedded documents within the database!")
        _ = VectorStoreIndex(
            nodes, service_context=service_context, storage_context=storage_context
        )

    def _handle_deletion(self, deletion_query: str, msg: str) -> None:
        if deletion_query:
            logging.info(f"{msg}Deleting some previous data in database!")
            self._delete_documents(deletion_query)

    def _create_service_context(self, node_parser: SimpleNodeParser) -> ServiceContext:
        return ServiceContext.from_defaults(
            node_parser=node_parser,
            llm=self.llm,
            embed_model=self.embed_model,
        )
