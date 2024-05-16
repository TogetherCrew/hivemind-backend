import os

from dotenv import load_dotenv


def load_postgres_credentials() -> dict[str, str]:
    """
    load postgres credentials into a dictionary

    Returns
    ---------
    credentials : dict[str, str]
        a dictionary containing
        `host`, `password`, `user`, `port`, and `db_name` as keys
        and values are the values for the credentials
    """
    load_dotenv()

    credentials: dict[str, str] = {}

    credentials["host"] = os.getenv("POSTGRES_HOST", "")
    credentials["password"] = os.getenv("POSTGRES_PASS", "")
    credentials["user"] = os.getenv("POSTGRES_USER", "")
    credentials["port"] = os.getenv("POSTGRES_PORT", "")
    credentials["db_name"] = os.getenv("POSTGRES_DBNAME", "")

    return credentials


def load_qdrant_credentials() -> dict[str, str]:
    """
    load qdrant database credentials

    Returns:
    ---------
    qdrant_creds : dict[str, Any]
        redis credentials
        a dictionary representive of
            `api_key` : str
            `host` : str
            `port` : int
    """
    load_dotenv()

    qdrant_creds: dict[str, str] = {}

    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")
    api_key = os.getenv("QDRANT_API_KEY")

    if host is None:
        raise ValueError("`QDRANT_HOST` is not set in env credentials!")
    if port is None:
        raise ValueError("`QDRANT_PORT` is not set in env credentials!")
    if api_key is None:
        raise ValueError("`QDRANT_API_KEY` is not set in env credentials!")

    qdrant_creds = {
        "host": host,
        "port": port,
        "api_key": api_key,
    }
    return qdrant_creds
