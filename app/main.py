from fastapi import FastAPI
from routers import auth, article

app = FastAPI()

app.include_router(auth.router)
app.include_router(article.router)