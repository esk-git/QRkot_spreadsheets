from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import BaseModelCharityDonattion


class Donation(BaseModelCharityDonattion):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
