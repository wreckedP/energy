from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


from app.settings.configuration import configuration

Base = declarative_base()

session_factory = sessionmaker(autoflush=False, bind=create_engine(configuration.db_driver + configuration.db_url + configuration.db_name))
session = session_factory()


def pg_session():
    try:
        return session
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.commit()
        session.close()
