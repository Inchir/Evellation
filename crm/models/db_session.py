from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

# from crm.logger import setup_logger

SqlAlchemyBase = orm.declarative_base()

__factory = None

import os


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    # pool_logger = setup_logger("sqlalchemy.pool", "./pool_logger.log", level=logging.INFO)

    db_path = Path(db_file).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo_pool=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
