import datetime
from typing import Annotated

import fastapi.requests
import loguru
import requests
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.schemas.ekl_report import ShiftEndInfoResponseSchema
from api.utils import templates
from db.utils import get_session

ekl_router = APIRouter(prefix="/ekl")

DATE_FORMAT = "%Y-%m-%d"
EKL_REQUEST_LINK = "http://192.168.10.12/api_bkl.php?fd={start}&sd={end}"


@ekl_router.get("/")
async def main_ekl(
    request: Request,
):
    # loguru.logger.debug(start_from.strftime("%Y-%m-%d"))
    return templates.TemplateResponse(
        request=request, name="ekl_report.html", context={"reports": []}
    )


@ekl_router.post("/info")
async def get_ekl_info(
    request: Request,
    start_from: Annotated[datetime.date, Form()],
    end_on: Annotated[datetime.date, Form()],
    session: Session = Depends(get_session),
):
    start_from = start_from.strftime(DATE_FORMAT)
    end_on = end_on.strftime(DATE_FORMAT)
    reports = requests.get(
        EKL_REQUEST_LINK.format(start=start_from, end=end_on)
    )
    ekl_data = ShiftEndInfoResponseSchema(info=reports.json())
    loguru.logger.debug(ekl_data)
    return templates.TemplateResponse(
        request=request,
        name="ekl_report.html",
        context={"reports": ekl_data.info},
    )
