from app.models.data_models import *
from utils.db_utils import Base, get_database_url
import os
from sqlalchemy import create_engine


def init_database():
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


def init_test_database() -> create_engine:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_db_path = os.path.join(project_root, "test.db")
    test_database_url = f"sqlite:///{test_db_path}"
    test_engine = create_engine(test_database_url, echo=False)
    Base.metadata.create_all(test_engine)

    return test_engine
