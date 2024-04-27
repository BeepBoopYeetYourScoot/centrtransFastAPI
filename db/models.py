import loguru
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from db.conf import Base, engine


class ShiftEndInfo(Base):
    __tablename__ = "shift_end_info"

    id = Column(Integer, primary_key=True)
    oper_code = Column(Integer)
    oper_div = Column(Integer)
    route_code = Column(String)
    tape_rn = Column(String)
    term = Column(String)
    ekl = Column(String)
    bkl = Column(String, nullable=True)
    status = Column(Boolean, nullable=True)
    date_of = Column(DateTime)
    ins_date = Column(DateTime)

    def __repr__(self):
        return f"<ShiftEndInfo(id={self.id} route_code={self.route_code} ekl={self.ekl})>"
