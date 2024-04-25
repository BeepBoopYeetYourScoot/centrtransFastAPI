import datetime
from typing import Optional

import loguru
from pydantic import BaseModel


class CardDataRequestModel(BaseModel):
    num: int
    order_num: Optional[str]
    oper_code: int
    route: str
    term_code: int
    smena: int
    ticket_number: str
    card_mask: str
    hashpan: str
    amount: float
    date_of: datetime.datetime
    date_payment: Optional[datetime.datetime]
    state: Optional[str]
    comment: Optional[str]
    approval: Optional[str]


class CardDataResponseModel(BaseModel):
    cards: list[CardDataRequestModel]

    def annotate_cards(self, hashpans):
        cards = self.dict()["cards"]
        assert isinstance(cards, list)
        for card in cards:
            card["is_blocked"] = card["hashpan"] in hashpans
        return cards
