from fastapi import FastAPI, HTTPException     # Imports FastAPI, a framework for building APIs, and HTTPException, which is used to return error responses.
from datetime import date                      # Imports the date module, which allows tracking expenses based on specific dates.
import db_helper                               # Imports the database helper functions for executing SQL queries.
from typing import List                        # Allows defining lists in request models (e.g., multiple expenses at once).
from pydantic import BaseModel                 # Pydantic ensures data validation, making sure API inputs follow the defined schema.

app = FastAPI()                                # Initializes a FastAPI application instance that will handle incoming HTTP requests.

class Expense(BaseModel):                      # Defines a Pydantic model for handling expense data input.
    amount: float                              # The expense amount, required to be a floating-point number. / Expense amount (numerical value).
    category: str                              # The category of the expense (e.g., "Food", "Rent"), required to be a string./Expense category (e.g., Rent, Food).
    notes: str                                 # Optional field to add descriptions or additional information./ Optional field for additional notes.

class DateRange(BaseModel):                    # Defines a Pydantic model to handle analytics requests for a date range.
    start_date: date                           # The start date for retrieving expense summary.
    end_date: date                             # The end date for retrieving expense summary.

# @app.get("/hello")
# def wish():
#     return "Hi"

@app.get("/expenses/{expense_date}", response_model=List[Expense])    # Defines a GET request to retrieve expenses for a specific date. /API endpoint to fetch expenses for a given date.
def get_expenses(expense_date: date):                                      # Function that processes the request and fetches expenses from the database.
    expenses = db_helper.fetch_expenses_for_date(expense_date)             # Calls fetch_expenses_for_date() from db_helper.py to query the database.
    if expenses is None:                                                   # Checks if no expenses were found for the given date.
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")   # Returns a 500 Internal Server Error if retrieval fails.
    return expenses                                                        # Returns the list of expenses as JSON.


@app.post("/expenses/{expense_date}")                                      # Defines a POST request to insert or update expenses./API endpoint to insert/update expenses.
def add_or_update_expense(expense_date: date, expenses:List[Expense]):     # Function to insert/update multiple expenses on a given date.
    db_helper.delete_expenses_for_date(expense_date)                       # Deletes old expenses for the given date before inserting new records.
    for expense in expenses:                                               # Inserts each expense into the database using insert_expense().
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated successfully"}                    # Returns a success response to the client.


@app.post("/analytics/")                                                   # Defines a POST request to compute expense analytics./API endpoint to fetch expense breakdown based on date range.
def get_analytics(date_range: DateRange):                                  # Function to fetch analytics for a date range.
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)   # Calls fetch_expense_summary() to get aggregated expense data.
    if data is None:                                                       # Checks if no data was found for the given period.
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")   # Returns an error response if data retrieval fails.
    total = sum([row['total'] for row in data])                            # Calculates the total expenses for the given period.

    breakdown = {}                                                         # Creates an empty dictionary to store expense category breakdown.

    for row in data:                                                       # Loops through each expense category returned by the database.
        percentage = (row['total']/total)*100 if total != 0 else 0         # Calculates the percentage of total expenses per category.
        breakdown[row['category']] = {                                     # Stores category-wise total and percentage in the dictionary.
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown                                                       # Returns the expense breakdown in JSON format.
