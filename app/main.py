from fastapi import FastAPI
from .utils import models
from .utils.database import engine
from .users import router as user_router
from .category import router as category_router
from .budgetrule import router as budget_router

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(budget_router.router)
