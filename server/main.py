from db import read_db
from fastapi import FastAPI
from typing import Union


# Initialize the FastAPI instance
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/daily")
def read_item():
    return read_db()
