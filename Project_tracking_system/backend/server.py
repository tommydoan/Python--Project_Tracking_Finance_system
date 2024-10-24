from distributed.utils_comm import retry
from fastapi import FastAPI, HTTPException
from datetime import date
from future.backports.datetime import datetime

import db_helper
from typing import List
from pydantic import BaseModel

class List_expense(BaseModel):
    amount:float
    category : str
    notes : str

class Date_expense(BaseModel):
    start_date: date
    end_date: date

class Month_range(BaseModel):
    start_date: date
    end_date: date
app = FastAPI()

@app.get('/expenses/{expense_date}', response_model=List[List_expense])
def get_expense(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    return expenses

@app.post('/expenses/{expense_date}')
def add_or_update_expense(expense_date: date, expenses : List[List_expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return "Successfully added or updated expense"

@app.post('/analytics/')
def get_analytics_expense(date_range: Date_expense):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total_amount =  sum([ row['total'] for row in data])

    breakdown = {}
    for row in data :
        percentage = (row['total']/total_amount)*100 if total_amount != 0 else 0
        breakdown[row['category']]  = {
            'total': row['total'],
            'percentage': percentage}
    return breakdown

@app.post('/analytics-month/')
def get_analytics_month(month_range: Month_range):
    data=db_helper.fetch_expense_by_month(month_range.start_date, month_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense by month from the database.")

    holder = []
    for row in data:
        holder.append({
            'month': row['month'],
            'total': row['total'],
        })
    return holder