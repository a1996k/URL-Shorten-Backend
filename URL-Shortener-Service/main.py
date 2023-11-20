from fastapi import FastAPI
from models.user import Base
from config.database import engine
from routes.user_routes import user
from routes.urls_routes import url
app = FastAPI()

@app.on_event("startup")
def create_tables():
    from sqlalchemy import MetaData

    metadata = MetaData()
    Base.metadata.create_all(engine)


app.include_router(user)
app.include_router(url)