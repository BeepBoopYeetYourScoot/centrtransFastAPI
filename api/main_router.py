from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from api.routers.hashpans import hashpan_router

app = FastAPI()


@app.get("/root")
def root():
    return {"message": "Hello World"}


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(hashpan_router)
