from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .database import database, engine, metadata
from .models import expenses_table

# Create tables
metadata.create_all(engine)

app = FastAPI()

# Mount static folder for JS/CSS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="app/templates")

# Pydantic model for Expense
class Expense(BaseModel):
    user_id: int
    title: str
    amount: float
    date: Optional[datetime] = None

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
async def add_expense(expense: Expense):
    if not expense.date:
        expense.date = datetime.now()
    query = expenses_table.insert().values(
        user_id=expense.user_id,
        title=expense.title,
        amount=expense.amount,
        date=expense.date
    )
    await database.execute(query)
    return {"message": "Expense added"}

# Get all expenses
@app.get("/expenses")
async def get_expenses():
    query = expenses_table.select()
    all_expenses = await database.fetch_all(query)
    # Convert datetime to string for frontend JSON
    return [
        {**dict(exp), "date": exp["date"].isoformat()} for exp in all_expenses
    ]

# Delete an expense by ID
@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    query = expenses_table.delete().where(expenses_table.c.id == expense_id)
    await database.execute(query)
    return {"message": "Expense deleted"}

# Update an expense by ID
@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, expense: Expense):
    query = expenses_table.update().where(expenses_table.c.id == expense_id).values(
        user_id=expense.user_id,
        title=expense.title,
        amount=expense.amount,
        date=expense.date if expense.date else datetime.now()
    )
    await database.execute(query)
    return {"message": "Expense updated"}

# Get monthly total for a user
@app.get("/expenses/summary/{user_id}")
async def get_monthly_total(user_id: int, month: Optional[int] = None, year: Optional[int] = None):
    query = expenses_table.select().where(expenses_table.c.user_id == user_id)
    user_expenses = await database.fetch_all(query)
    total = 0.0

    for e in user_expenses:
        e_date = e['date']
        e_month = e_date.month
        e_year = e_date.year
        if (month is None or month == e_month) and (year is None or year == e_year):
            total += e['amount']

    return {
        "user_id": user_id,
        "month": month if month else "all",
        "year": year if year else "all",
        "total": total
    }
