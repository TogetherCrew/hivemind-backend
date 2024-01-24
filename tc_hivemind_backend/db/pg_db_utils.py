import logging
from datetime import datetime

import psycopg2
from tc_hivemind_backend.db.postgresql import PostgresSingleton


def setup_db(
    community_id: str, dbname: str, latest_date_query: str | None = None
) -> datetime | None:
    """
    setup the database.
    create a database if not available, else get the latest message saved

    Parameters
    ------------
    community_id : str
        the community id for the case of logging
    dbname : str
        the database name to create or access its database
    guild_id : str
        the guild id to create a database for
    latest_date_query : str | None
        the query to get latest date of a message
        if `None`, then no need to check for latest_message date
        the return would be also `None` if this field was `None`

    Returns
    ---------
    from_date : datetime | None
        in case of no data available it would be None
    """
    msg = f"COMMUNITYID: {community_id} "
    from_date: datetime | None = None
    connection: psycopg2.extensions.connection
    try:
        postgres = PostgresSingleton(dbname=dbname)
        if postgres is not None:
            logging.info(f"{msg}Database {dbname} is already available!")
            postgres.close_connection()
            if latest_date_query is not None:
                logging.info(f"{msg}Checking the latest saved message!")
                from_date = get_latest_msg(community_id, dbname, latest_date_query)
        else:
            logging.warning(
                f"{msg}Database {dbname} is Not available! Creating one instead!"
            )
            # Connecting to default db passed in `.env`
            postgres_default_db = PostgresSingleton(dbname=None)
            connection = postgres_default_db.get_connection()
            connection.autocommit = True
            cursor = connection.cursor()
            logging.info(f"{msg}Creating database {dbname}")
            cursor.execute(f"CREATE DATABASE {dbname};")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cursor.close()
            connection.close()
    except Exception as exp:
        logging.error(f"{msg}database initialization error: {exp}")

    return from_date


def get_latest_msg(community_id: str, dbname: str, latest_date_query: str):
    from_date: datetime | None = None
    msg = f"COMMUNITYID: {community_id} "

    postgres = PostgresSingleton(dbname=dbname)
    connection = postgres.get_connection()
    connection.autocommit = True
    with connection.cursor() as cursor:
        try:
            # If we had some data previously saved
            # fetch the latest date we wanted to work on it
            logging.info(f"{msg}Loading the latest date from previous data")
            cursor.execute(latest_date_query)
            data = cursor.fetchone()
            if data is not None:
                from_date = data[0]
                logging.info(f"{msg}Latest processed message: {from_date}")
            else:
                logging.info(f"{msg}No processed message, starting from the first!")
        except psycopg2.errors.UndefinedTable:
            logging.warning(f"{msg}No data to get the latest date")

    postgres.close_connection()
    return from_date


def convert_tuple_str(data: list[str]) -> str:
    """
    convert a list of inputs to a string tuple that
    can be queried within database

    Parameters
    ------------
    data : list[str]
        list of string items

    Returns
    ---------
    data_str : str
        the data converted to string tuple
    """
    data_str: str
    if len(data) == 1:
        data_str = f"('{data[0]}')"
    else:
        data_str = str(tuple(data))

    return data_str
