import os

class Config:
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_URL = os.getenv("DB_URL", "sqlite:///./test.db")

config = Config()
