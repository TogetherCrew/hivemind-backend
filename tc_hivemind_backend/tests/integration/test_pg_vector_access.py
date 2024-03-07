import unittest

import psycopg2
from llama_index.core import Document
from llama_index.core.indices.vector_store import VectorStoreIndex
from tc_hivemind_backend.db.credentials import load_postgres_credentials
from tc_hivemind_backend.db.pg_db_utils import setup_db
from tc_hivemind_backend.pg_vector_access import PGVectorAccess


class TestPGVectorAccess(unittest.TestCase):
    def setUpDB(self, dbname: str, table_name: str):
        creds = load_postgres_credentials()
        self.community_id = "123456789a"
        latest_date_query = f"""
            SELECT (metadata_->> 'date')::timestamp AS latest_date
            FROM data_{table_name}
            ORDER BY (metadata_->>'date')::timestamp DESC
            LIMIT 1;
        """
        setup_db(
            community_id=self.community_id,
            dbname=dbname,
            latest_date_query=latest_date_query,
        )
        self.postgres_conn = psycopg2.connect(
            dbname=dbname,
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            port=creds["port"],
        )

    def _create_and_save_doc(self, table: str, dbname: str):
        documents = [
            Document(
                text="test_message1",
                metadata={
                    "channel": "channel#1",
                    "author_username": "author#1",
                    "author_global_name": "author_global#1",
                    "date": "2023-08-01",
                },
            )
        ]
        self.setUpDB(dbname=dbname, table_name=table)
        cursor = self.postgres_conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS data_{table};")
        self.postgres_conn.commit()
        pg_vector = PGVectorAccess(table_name=table, dbname=dbname, testing=True)

        # Save the documents
        pg_vector.save_documents(self.community_id, documents, verbose=True)
        return documents

    def test_save_documents(self):
        table = "discord"
        guild_id = "1234"
        dbname = f"guild_{guild_id}"

        documents = self._create_and_save_doc(table, dbname)
        cursor = self.postgres_conn.cursor()

        cursor.execute(f"SELECT text, node_id, metadata_ FROM data_{table};")

        data = cursor.fetchall()

        self.assertEqual(len(data), 1)

        # text, node_id, metadata
        text, _, metadata = data[0]

        # nickname was `None`, so it wasn't included in metadata
        self.assertEqual(text, "test_message1")
        self.assertEqual(metadata["channel"], documents[0].metadata["channel"])
        self.assertEqual(
            metadata["author_username"], documents[0].metadata["author_username"]
        )
        self.assertEqual(
            metadata["author_global_name"], documents[0].metadata["author_global_name"]
        )
        self.assertEqual(metadata["date"], documents[0].metadata["date"])
        self.assertNotIn("author_nickname", metadata)

        cursor.close()

    def test_load_index(self):
        table = "discord"
        guild_id = "1234"
        dbname = f"guild_{guild_id}"
        _ = self._create_and_save_doc(table, dbname)

        pg_vector = PGVectorAccess(table_name=table, dbname=dbname, testing=True)
        index = pg_vector.load_index()

        self.assertIsInstance(index, VectorStoreIndex)

        cursor = self.postgres_conn.cursor()
        cursor.close()
