import os

from dotenv import load_dotenv


def load_mongo_credentials() -> dict[str, str]:
    """
    load mongo db credentials from .env

    Returns:
    ---------
    mongo_creds : dict[str, Any]
        mongodb credentials
        a dictionary representive of
            `user`: str
            `password` : str
            `host` : str
            `port` : int
    """
    load_dotenv()

    mongo_creds = {}

    mongo_creds["user"] = os.getenv("MONGODB_USER", "")
    mongo_creds["password"] = os.getenv("MONGODB_PASS", "")
    mongo_creds["host"] = os.getenv("MONGODB_HOST", "")
    mongo_creds["port"] = os.getenv("MONGODB_PORT", "")

    return mongo_creds


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
