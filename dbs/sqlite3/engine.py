from sqlalchemy import create_engine

import settings

engine = None


def get_engine(url: str = settings.SQLITE3_DATABASE_URI):
    global engine

    if engine is None:
        engine = create_engine(url, execution_options={"sqlite_raw_colnames": True}, echo=True)

    return engine
