from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loaded!")
    yield
    print("Unloaded!")

app = FastAPI(lifespan=lifespan)
