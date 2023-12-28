from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import DatabaseController
from apis.articles import router as articles_router
from apis.subjects import router as subjects_router
from apis.operations import router as options_router

app = FastAPI()
app.include_router(articles_router, prefix='/api')
app.include_router(subjects_router, prefix='/api')
app.include_router(options_router, prefix='/api')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])


@app.on_event("startup")
async def startup():
    app.db_controller = DatabaseController()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
