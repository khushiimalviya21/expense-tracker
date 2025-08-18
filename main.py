from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import database, engine, metadata
from models import expenses_table

# Create tables
metadata.create_all(engine)

app = FastAPI()

# Pydantic model for Expense
class Expense(BaseModel):
    user_id: int
    title: str
    amount: float
    date: Optional[datetime] = None  

# Templates directory
templates = Jinja2Templates(directory="templates")

# Connect/disconnect database
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Serve HTML
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Add new expense
@app.post("/expenses")
def add_expense(expense: Expense):
    expenses.append(expense)
    return {"message": "Expense added"}

# Get all expenses
@app.get("/expenses")
async def get_expenses():
    query = expenses_table.select()
    all_expenses = await database.fetch_all(query)
    return all_expenses

# Delete an expense by DB-generated ID
@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    query = expenses_table.delete().where(expenses_table.c.id == expense_id)
    await database.execute(query)
    return {"message": "Expense deleted"}

# Get monthly total for a user
@app.get("/expenses/summary/{user_id}")
def get_monthly_total(user_id: int):
    now = datetime.now()
    total = 0.0

    for e in expenses:
        if e.id == user_id and e.date.month == now.month and e.date.year == now.year:
            total += e.amount

    return {
        "user_id": user_id,
        "month": month if month else "all",
        "year": year if year else "all",
        "total": total
    }
