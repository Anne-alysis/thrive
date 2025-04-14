import os

from sqlalchemy import create_engine


def get_engine():
    db_url = os.environ.get("LOCAL_DB_URL")
    if db_url is None:
        raise ValueError("Cannot get url! ")

    return create_engine(db_url)
