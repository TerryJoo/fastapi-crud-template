from typing import Generator

from sqlalchemy.orm import sessionmaker

from dbs.sqlite3.engine import get_engine

generate_session = sessionmaker(bind=get_engine())


def get_session() -> Generator:
    session = generate_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
