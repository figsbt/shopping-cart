import os 


# from pydantic import BaseSettings


# class Settings(BaseSettings):
#     DATABASE_PORT: int
#     POSTGRES_PASSWORD: str
#     POSTGRES_USER: str
#     POSTGRES_DB: str
#     POSTGRES_HOST: str
#     POSTGRES_HOSTNAME: str
    
#     class Config:
#         env_file = './.env'


# settings = Setting()

DATABASE_URL = DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
	host=os.getenv("POSTGRES_HOST"),
	port=os.getenv("POSTGRES_PORT"),
	db_name=os.getenv("POSTGRES_DB"),
	username=os.getenv("POSTGRES_USER"),
	password=os.getenv("POSTGRES_PASSWORD"),
)

TABLES = [
    "users",
    "items"
]

UTF_FORMAT = "utf8"
SECRET_KEY = os.getenv("SECRET_KEY")
