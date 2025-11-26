from fastapi import FastAPI
from .utils import models
from .utils.database import engine
from .users import router

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(router.router)