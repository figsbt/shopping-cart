from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import (
    Column, 
    ForeignKey, 
    String, 
    Integer, 
    text, 
    TIMESTAMP, 
    Float,
    Boolean,
    LargeBinary,
    UniqueConstraint,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship, Session, sessionmaker, declarative_base


Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	"""Database session generator"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
		


def reset_db_on_startup(table_names):
	with engine.connect() as con:
		"""
            for table_name in table_names:
                con.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            con.execute(
                text("CREATE TABLE users (id SERIAL PRIMARY KEY, email_id VARCHAR(255) NOT NULL, pwd_hash VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, is_active BOOLEAN DEFAULT TRUE, is_admin BOOLEAN DEFAULT FALSE, UNIQUE(email_id));")
            )
            con.execute(
                text("CREATE TABLE items (id SERIAL PRIMARY KEY, item_name VARCHAR(255) NOT NULL, item_details VARCHAR(255) NOT NULL, stock INT NOT NULL, cost FLOAT);")
            )
		"""
