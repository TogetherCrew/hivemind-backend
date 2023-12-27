import logging

import psycopg2
from tc_hivemind_backend.db.postgresql import PostgresSingleton


def delete_data(deletion_query: str, dbname) -> None:
    """
    a wrapper function to add the deletion feature

    Parameters
    -----------
    deletion_query : str
        the query to delete or modify the database
    """
    connection: psycopg2.extensions.connection
    try:
        # first connecting to no database to check the database availability
        postgres = PostgresSingleton(dbname=dbname)
        connection = postgres.get_connection()
        connection.autocommit = True
        with connection.cursor() as cursor:
            logging.info("Deleting data from postgresql!")
            cursor.execute(deletion_query)
    except Exception as exp:
        logging.error(f"Database deletion error: {exp}")
    finally:
        postgres.close_connection()