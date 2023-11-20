from sqlalchemy import Column, Integer, TEXT, Date
from models.index import Base

class Url(Base):
    __tablename__ = "urls"
    shorturl = Column(TEXT, primary_key=True)
    longurl = Column(TEXT)
    user_email = Column(TEXT)
    createdDate = Column(Date)
    expiryDate = Column(Date)
