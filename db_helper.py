import mysql.connector                       # Imports MySQL Connector, which allows the script to connect to a MySQL database.
from contextlib import contextmanager        # Imports contextmanager from contextlib to manage database connections safely.
from logging_setup import setup_logger       # Imports a custom logging setup to keep track of database operations
                                             # The logging module in Python is used for tracking events in your application.
logger = setup_logger('db_helper')           # Initializes the logger named db_helper to record database operations.

@contextmanager                              # Defines a context manager to safely handle database connections.
def get_db_cursor(commit=False):             # Function to get a database cursor for executing SQL queries.
    connection = mysql.connector.connect(    # Establishes a connection to the MySQL database using credentials.
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)  # Creates a cursor that returns results as dictionaries (column names as keys).
    yield cursor                                 # Returns the cursor to execute queries within a with block.
    if commit:                                   # Checks if the commit flag is True (used for INSERT, DELETE, or UPDATE queries).
        connection.commit()                      # Commits the transaction to save changes to the database.
    cursor.close()                               # Closes the cursor connection after execution.
    connection.close()                           #Closes the database connection after execution.


def fetch_expenses_for_date(expense_date):                              # Function to retrieve all expenses for a given date.
    logger.info(f"fetch_expenses_for_date called with {expense_date}")  # Logs the function call for debugging purposes.
    with get_db_cursor() as cursor:                                     # Opens a database connection using the context manager.
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))    # SQL query to retrieve all expenses for a specific date.
        expenses = cursor.fetchall()                                    # Fetches all matching records from the database.
        return expenses                                                 # Returns the list of expenses to the calling function.


def delete_expenses_for_date(expense_date):                             # Function to delete expenses for a given date.
    logger.info(f"delete_expenses_for_date called with {expense_date}") # Logs the delete operation.
    with get_db_cursor(commit=True) as cursor:                          # Opens a database connection with commit enabled.
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))    # Executes a SQL DELETE query to remove all expenses for that date.


def insert_expense(expense_date, amount, category, notes):              # Function to insert a new expense record into MySQL.
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")    # Logs the expense insertion details.
    with get_db_cursor(commit=True) as cursor:                          # Opens a database connection with commit enabled.
        cursor.execute(                                                 # Executes a SQL INSERT query to store the expense details.
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def fetch_expense_summary(start_date, end_date):                       # Function to compute total expenses grouped by category.
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")  # Logs the analytics request.
    with get_db_cursor() as cursor:                                    # Opens a database connection.
        cursor.execute(                                                # SQL query to group expenses by category and calculate totals.
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()                                       # Fetches the aggregated summary from MySQL.
        return data                                                    # Returns expense breakdown to the calling function.


if __name__ == "__main__":                                             # Checks if the script is run directly (not imported as a module).
    expenses = fetch_expenses_for_date("2024-09-30")                   # Fetches expenses for the given date and prints them.
    print(expenses)                                                    # Displays the fetched expense records.
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")  # Fetches expense summary between two dates.
    for record in summary:                                             # Loops through the summary results.
        print(record)                                                  # Prints the expense breakdown per category.
