from fastapi import FastAPI
import routes
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from fastapi.staticfiles import StaticFiles

# FastAPI stuff

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)
