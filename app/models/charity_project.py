from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LENGHT
from app.core.db import BaseModelCharityDonattion


class CharityProject(BaseModelCharityDonattion):
    name = Column(String(MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
