from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from api.routers.ekl_report import ekl_router
from api.routers.hashpans import hashpan_router
from api.utils import templates

app = FastAPI()


@app.get("/root")
def root():
    return {"message": "Hello World"}


@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(hashpan_router)
app.include_router(ekl_router)
