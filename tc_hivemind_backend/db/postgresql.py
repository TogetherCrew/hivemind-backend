import logging

import psycopg2
from tc_hivemind_backend.db.credentials import load_postgres_credentials


class PostgresSingleton:
    _instance = None

    def __new__(cls, dbname: str | None, *args, **kwargs):
        """
        if `db_name` was `None`, connect to default database in .env
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.connect(dbname)
        return cls._instance

    def connect(self, dbname: str | None):
        """
        connect to postgrsql instance
        """
        creds = load_postgres_credentials()
        try:
            self.conn = psycopg2.connect(
                dbname=dbname or creds["db_name"],
                user=creds["user"],
                password=creds["password"],
                host=creds["host"],
                port=creds["port"],
            )
        except psycopg2.OperationalError as exp:
            logging.error(f"Error initializing connection, exp: {exp}")
            self.destroy_instance()

    def get_connection(self):
        """
        get a connection to database
        """
        return self.conn

    def close_connection(self):
        """
        will close the connection and destroy the class
        """
        self.conn.close()
        self.destroy_instance()

    @classmethod
    def destroy_instance(cls):
        cls._instance = None
