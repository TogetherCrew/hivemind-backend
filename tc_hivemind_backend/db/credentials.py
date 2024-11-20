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

    Note: Depricated. Use `Credentials` class instead.
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
        qdrant credentials
        a dictionary representive of
            `api_key` : str
            `host` : str
            `port` : int

    Note: Depricated. Use `Credentials` class instead.
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


class Credentials:
    def __init__(self) -> None:
        load_dotenv()

    def load_mongo(self) -> dict[str, str]:
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
        mongo_creds = {}

        mongo_creds["user"] = os.getenv("MONGODB_USER", "root")
        mongo_creds["password"] = os.getenv("MONGODB_PASS", "pass")
        mongo_creds["host"] = os.getenv("MONGODB_HOST", "mongo")
        mongo_creds["port"] = os.getenv("MONGODB_PORT", 27017)

        return mongo_creds

    def load_redis(self) -> dict[str, str]:
        """
        load redis db credentials from .env

        Returns:
        ---------
        redis_creds : dict[str, Any]
            redis credentials
            a dictionary representive of
                `password` : str
                `host` : str
                `port` : int
        """
        host = os.getenv("REDIS_HOST")
        port = os.getenv("REDIS_PORT")
        password = os.getenv("REDIS_PASSWORD")

        if host is None:
            raise ValueError("`REDIS_HOST` is not set in env credentials!")
        if port is None:
            raise ValueError("`REDIS_PORT` is not set in env credentials!")
        if password is None:
            raise ValueError("`REDIS_PASSWORD` is not set in env credentials!")

        redis_creds: dict[str, str] = {
            "host": host,
            "port": port,
            "password": password,
        }
        return redis_creds

    def load_qdrant(self):
        credentials = load_qdrant_credentials()

        return credentials

    def load_postgres(self):
        """
        load postgres credentials into a dictionary

        Returns
        ---------
        credentials : dict[str, str]
            a dictionary containing
            `host`, `password`, `user`, `port`, and `db_name` as keys
            and values are the values for the credentials
        """
        credentials = load_postgres_credentials()

        return credentials
