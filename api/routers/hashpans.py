import asyncio
from typing import Annotated

import loguru
import requests
from fastapi import Form, APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import HTMLResponse

from api.const import (
    BLACKLISTED_PANS_URL,
    MAX_PAGE_SIZE,
    HASHPAN_INFO_URL,
    TOTAL_PAGES_KEY,
    ALL_OBJECTS_KEY,
    HASHPAN_FIELD_KEY,
    CARD_MASK_VALUE,
)
from api.schemas.hashpans import CardDataResponseModel
from api.utils import templates, get_async

HASHPAN_PREFIX = "/hashpan"

hashpan_router = APIRouter(prefix=HASHPAN_PREFIX)


@hashpan_router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


@hashpan_router.get("/form")
async def hashpan_view(request: Request):
    return templates.TemplateResponse(request=request, name="card_orders.html")


async def request_all_hashpans():
    hashpans = []
    zero_page_dict, zero_page_values = await get_zero_page_hashpans()
    hashpans.extend(zero_page_values)

    pages_to_request = [
        BLACKLISTED_PANS_URL.format(max_size=MAX_PAGE_SIZE, page_num=i)
        for i in range(1, zero_page_dict[TOTAL_PAGES_KEY])
    ]
    coros = map(get_async, pages_to_request)
    pans = await asyncio.gather(*coros)
    loguru.logger.debug(f"{pans=}")

    for pan_page in pans:
        page_dict = pan_page.json()
        values = [obj[HASHPAN_FIELD_KEY] for obj in page_dict[ALL_OBJECTS_KEY]]
        hashpans.extend(values)

    loguru.logger.debug(f"{len(hashpans)=}")
    return set(hashpans)


async def get_zero_page_hashpans():
    zero_page = await get_async(
        BLACKLISTED_PANS_URL.format(max_size=MAX_PAGE_SIZE, page_num=0),
    )
    zero_page_dict = zero_page.json()
    zero_page_values = [obj["a"] for obj in zero_page_dict["listValues"]]
    return zero_page_dict, zero_page_values


@hashpan_router.post("/find")
async def find_blacklisted_hashpans(
    request: Request,
    first_six_numbers: Annotated[str, Form()],
    last_four_numbers: Annotated[str, Form()],
    hashpans: Annotated[list, Depends(request_all_hashpans)],
):
    assert len(first_six_numbers) == 6
    assert len(last_four_numbers) == 4
    card_mask = first_six_numbers + CARD_MASK_VALUE + last_four_numbers
    card_info = requests.get(
        HASHPAN_INFO_URL.format(card_mask=card_mask), verify=False
    )
    try:
        card_data = CardDataResponseModel(cards=card_info.json())
        loguru.logger.debug(f"{card_data=}")
    except ValidationError as e:
        loguru.logger.exception(e)
        raise HTTPException(status_code=400)
    return templates.TemplateResponse(
        request,
        name="card_orders.html",
        context={"payments": card_data.annotate_cards(hashpans)},
    )
