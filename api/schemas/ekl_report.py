import datetime
from typing import Optional

import loguru
from pydantic import BaseModel


class ShiftEndInfoSchema(BaseModel):
    oper_code: int
    oper_div: int
    route_code: str
    tape_rn: str
    term: str
    ekl: str
    bkl: Optional[str]
    status: Optional[str]
    date_of: datetime.datetime
    ins_date: datetime.datetime


class ShiftEndInfoResponseSchema(BaseModel):
    info: list[ShiftEndInfoSchema]
