from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from database import metadata

# Expenses table: id is auto-increment, user_id can repeat
expenses_table = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),  # DB generates unique ID
    Column("user_id", Integer, nullable=False),
    Column("title", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("date", DateTime, nullable=False)
)
