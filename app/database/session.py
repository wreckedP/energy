from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncScalarResult,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker, scoped_session


from app.settings.configuration import configuration

Base = declarative_base()

session_factory = sessionmaker(autoflush=False, bind=create_engine(configuration.db_driver + configuration.db_url + configuration.db_name))
session = session_factory()

async_engine = create_async_engine(
    configuration.db_async_driver + configuration.db_url + configuration.db_name,
    echo=True,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


def pg_session():
    try:
        return session
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.commit()
        session.close()


async def async_pg_session():
    session = async_sessionmaker(async_engine, expire_on_commit=False)
    try:
        return session()
    except Exception as err:
        raise err
    finally:
        await async_engine.dispose()
