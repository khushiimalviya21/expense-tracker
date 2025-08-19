from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from .database import metadata
from datetime import datetime

expenses_table = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column("title", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("date", DateTime, default=datetime.now)
)
