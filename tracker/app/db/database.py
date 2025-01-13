from sqlmodel import create_engine, SQLModel, Session
from app.core.models.models import Fighter, Fight, User, Pick, Card
from typing import Annotated
from fastapi import Depends
import logging
import os

_ = (Fighter, Fight, User, Pick, Card)

current_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.abspath(os.path.join(current_dir, "../../data/database.db"))
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}  # multithreading
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("database and tables created successfully")
    except Exception as e:
        logging.error(f"error creating database and tables: {e}")

def get_session():
    with Session(engine) as session:
        yield session


# simplifying the dependency injection
SessionDep = Annotated[Session, Depends(get_session)]

"""
when testing, use a temporary in-memory database
def get_test_engine():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
"""
