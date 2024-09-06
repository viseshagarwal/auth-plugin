from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymongo
from pymongo import MongoClient

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    created_at = Column(DateTime)


class DatabaseManager:
    def __init__(self, db_type, db_url):
        self.db_type = db_type
        self.db_url = db_url
        if db_type == "sqlite" or db_type == "postgresql":
            self.engine = create_engine(db_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        elif db_type == "mongodb":
            self.client = MongoClient(db_url)
            self.db = self.client.get_database()

    def add_user(self, username, email):
        if self.db_type in ["sqlite", "postgresql"]:
            session = self.Session()
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
            session.close()
        elif self.db_type == "mongodb":
            self.db.users.insert_one({"username": username, "email": email})

    def get_user(self, user_id):
        if self.db_type in ["sqlite", "postgresql"]:
            session = self.Session()
            user = session.query(User).filter(User.id == user_id).first()
            session.close()
            return user
        elif self.db_type == "mongodb":
            return self.db.users.find_one({"_id": user_id})

    def delete_user(self, user_id):
        if self.db_type in ["sqlite", "postgresql"]:
            session = self.Session()
            user = session.query(User).filter(User.id == user_id).first()
            session.delete(user)
            session.commit()
            session.close()
        elif self.db_type == "mongodb":
            self.db.users.delete_one({"_id": user_id})
