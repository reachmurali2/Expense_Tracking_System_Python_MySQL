import streamlit as st                              # Imports Streamlit, which is used for creating the web interface.
from add_update_ui import add_update_tab            # Imports the add_update_tab() function, which handles the expense entry UI.
from analytics_ui import analytics_tab              # Imports the analytics_tab() function, which handles the analytics dashboard UI.

st.title("Expense Tracking System")                 # Sets the title of the Streamlit app (displayed at the top of the page).

tab1, tab2 = st.tabs(["Add/Update", "Analytics"])   # Creates two tabs: one for adding/updating expenses, and another for viewing analytics.

with tab1:                                          # Selects the first tab ("Add/Update") for expense entry.
    add_update_tab()                                # Calls the function from add_update_ui.py, which contains the form for entering expenses.

with tab2:                                          # Selects the second tab ("Analytics") for data visualization.
    analytics_tab()                                 # Calls the function from analytics_ui.py, which generates charts and statistics for expenses.
