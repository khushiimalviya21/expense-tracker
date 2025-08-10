from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

# In-memory list of expenses
expenses = []

# Pydantic model for Expense with date
class Expense(BaseModel):
    id: int
    title: str
    amount: float
    date: Optional[datetime] = datetime.now()  # Auto-filled if not provided

# Jinja2 Templates directory
templates = Jinja2Templates(directory="templates")

# Serve the HTML form
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Add a new expense
@app.post("/expenses")
def add_expense(expense: Expense):
    expenses.append(expense)
    return {"message": "Expense added"}

# Get all expenses
@app.get("/expenses")
def get_expenses():
    return expenses

# Delete an expense by ID
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    global expenses
    expenses = [e for e in expenses if e.id != expense_id]
    return {"message": "Expense deleted"}

# Get monthly total for a given user ID
@app.get("/expenses/summary/{user_id}")
def get_monthly_total(user_id: int):
    now = datetime.now()
    total = 0.0

    for e in expenses:
        if e.id == user_id and e.date.month == now.month and e.date.year == now.year:
            total += e.amount

    return {
        "user_id": user_id,
        "month": now.month,
        "year": now.year,
        "total": total
    }
