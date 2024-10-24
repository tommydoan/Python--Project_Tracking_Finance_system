from datetime import datetime
import streamlit as st
from holoviews.operation import collapse
import requests


url ='http://localhost:8000'

def get_update_tab():
    select_date = st.date_input('Enter date', datetime(2024, 8, 2), label_visibility="collapsed")
    response = requests.get(f"{url}/expenses/{select_date}")
    # select_date_str = select_date.strftime('%m/%d/%Y')
    if response.status_code == 200:
        data = response.json()
    else:
        st.error("failed to retrieved expense data")
        data = []

    # Declare category to get list  collapsed
    categories = ['Rent', 'Food', 'Shopping', 'Entertainment', 'Other']
    with st.form(key="expense_form"):
        # Add header
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        # add number of row in table
        expenses = []
        for i in range(5):
            # Check if customer choose date will not over than the last date
            if i < len(data):
                amount = data[i]['amount']
                category = data[i]['category']
                notes = data[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            # Create full table
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input,
                # 'expense_date': select_date_str,
            })
        # Should have submit button to finish table
        submit_button = st.form_submit_button()
        if submit_button:
            filter_expense = [expense for expense in expenses if expense['amount'] > 0]
            response = requests.post(f"{url}/expenses/{select_date}", json=filter_expense)
            if response.status_code == 200:
                st.success("update expense successful")
            else:
                st.error("failed to update expense data")