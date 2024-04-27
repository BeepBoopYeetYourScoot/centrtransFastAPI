from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DB_NAME = "postgres"
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/{db_name}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL.format(db_name=DB_NAME), echo=True
)  # , connect_args={"check_same_thread": False} for sqlite
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
