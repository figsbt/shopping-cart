import os
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
    PrimaryKeyConstraint,
	ARRAY,
	JSON
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


def reset_db_on_startup():
	with engine.connect() as con:
		os.system("PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -U postgres -q -f init.sql")
