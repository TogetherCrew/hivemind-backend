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
    use_https = bool(os.getenv("QDRANT_USE_HTTPS", False))

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
        "use_https": use_https,
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

        user = os.getenv("MONGODB_USER")
        password = os.getenv("MONGODB_PASS")
        host = os.getenv("MONGODB_HOST")
        port = os.getenv("MONGODB_PORT")

        if user is None:
            raise ValueError("`MONGODB_USER` is not set in env credentials!")
        if password is None:
            raise ValueError("`MONGODB_PASS` is not set in env credentials!")
        if host is None:
            raise ValueError("`MONGODB_HOST` is not set in env credentials!")
        if port is None:
            raise ValueError("`MONGODB_PORT` is not set in env credentials!")

        mongo_creds = {"user": user, "password": password, "host": host, "port": port}
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

    def load_qdrant(self) -> dict[str, str]:
        """
        load qdrant credentials from .env

        Returns:
        ---------
        dict[str, str]
            qdrant credentials containing host, port, and api_key
        """
        credentials = load_qdrant_credentials()

        return credentials

    def load_postgres(self) -> dict[str, str]:
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
