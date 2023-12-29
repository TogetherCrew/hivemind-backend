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

    return credentials
