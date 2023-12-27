from unittest import TestCase

from tc_hivemind_backend.db.pg_db_utils import setup_db
from tc_hivemind_backend.db.postgresql import PostgresSingleton
from tc_hivemind_backend.db.utils.delete_data import delete_data


class TestDeletePGData(TestCase):
    def setUp(self):
        self.dbname = "test_db"
        setup_db(
            community_id="community123",
            dbname=self.dbname,
            latest_date_query="SELECT 1;",
        )

    def test_delete_no_data(self):
        """
        running a dummy query
        """
        delete_data(deletion_query="SELECT 1;", dbname=self.dbname)

    def test_delete_some_data(self):
        postgres = PostgresSingleton(dbname=self.dbname)
        connection = postgres.get_connection()
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DROP TABLE IF EXISTS temp_table;
                """
            )
            cursor.execute(
                """
                CREATE TABLE temp_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    age INT
                );
            """
            )

            cursor.execute(
                """
                INSERT INTO temp_table (name, age) VALUES
                    ('John Doe', 25),
                    ('Jane Smith', 30),
                    ('Bob Johnson', 22);
            """
            )
        postgres.close_connection()

        delete_data(deletion_query="DELETE FROM temp_table;", dbname=self.dbname)

        postgres = PostgresSingleton(dbname=self.dbname)
        connection = postgres.get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM temp_table;")
            res = cursor.fetchone()

        postgres.close_connection()
        self.assertEqual(res, None)
