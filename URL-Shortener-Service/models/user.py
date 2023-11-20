from models.index import Base
from sqlalchemy import Column, String, Integer
from passlib.hash import pbkdf2_sha256


class User(Base):
    __tablename__ = "users"
    email = Column(String(255), primary_key=True,unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tier = Column(Integer, nullable=False)
    no_of_requests = Column(Integer, nullable=False)
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
