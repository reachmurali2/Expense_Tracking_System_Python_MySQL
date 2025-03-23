import streamlit as st                                     # Imports Streamlit, which is used for building the interactive web app UI.
from datetime import datetime                              # Imports datetime, which is used to handle date selections.
import requests                                            # Imports the requests module, which enables HTTP requests to the FastAPI backend.

API_URL = "http://localhost:8000"                          # Defines the FastAPI backend URL that Streamlit will send and receive data from.


def add_update_tab():                                      # Defines a function that generates the expense input form UI.
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed") # Creates a date picker widget for selecting the expense date. - Default value: August 1, 2024.
    response = requests.get(f"{API_URL}/expenses/{selected_date}")    #  # Sends a GET request to FastAPI to fetch stored expenses for the selected date.
    if response.status_code == 200:                        #  Checks if the API request was successful (status code 200 OK).
        existing_expenses = response.json()                # Extracts the expense data from the API response.
        # st.write(existing_expenses)
    else:                                                  # Handles the case when the request fails.
        st.error("Failed to retrieve expenses")            # Displays an error message if data retrieval fails.
        existing_expenses = []                             # Initializes an empty list if no expenses are found.

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]   # Defines a list of categories for expense classification.

    with st.form(key="expense_form"):                      # Creates a form container for entering expenses.
        col1, col2, col3 = st.columns(3)                   # Creates three columns to organize the form layout.
        with col1:                                         # Displays "Amount" as a label in the first column.
            st.text("Amount")
        with col2:                                         # Displays "Category" as a label in the second column.
            st.text("Category")
        with col3:                                         # Displays "Notes" as a label in the third column.
            st.text("Notes")

        expenses = []                                      # Initializes an empty list to store expense inputs.
        for i in range(5):                                 # Creates input fields for up to 5 expenses.
            if i < len(existing_expenses):                 # Checks if existing expenses are available for pre-filling the fields.
                amount = existing_expenses[i]["amount"]    # Extracts the stored amount from API response (⚠ Fix Needed: amount should be a string key).
                category = existing_expenses[i]["category"] # Extracts the stored category from API response.
                notes = existing_expenses[i]["notes"]      # Extracts the stored notes from API response.
            else:                                          # If no stored data is available, assign default values.
                amount = 0.0                               # Default values for empty fields.
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)               # Creates three columns to structure the form.
            with col1:                                     # Places amount input field in the first column.
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")     # Creates a numeric input field for the amount.
            with col2:                                     # Places category dropdown in the second column.
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}", label_visibility="collapsed") # Creates a dropdown menu to select a category.
            with col3:                                     # Places notes input field in the third column
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")
                                                           # Creates a text input field for optional notes.
            expenses.append({                              # Stores user inputs in a list.
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()             # Creates a submit button to save expenses.
        if submit_button:                                   # Executes this block when the user clicks Submit.
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]   # Removes empty expense entries where amount = 0.

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)   # Sends a POST request to FastAPI with the new expense data.
            if response.status_code == 200:                 # Checks if the request was successful (status code 200 OK).
                st.success("Expenses updated successfully!") # Displays a success message if the data is saved successfully.
            else:                                            # Handles failed requests.
                st.error("Failed to update expenses.")       # Displays an error message if the request fails.
