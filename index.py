import streamlit as st
import requests
from datetime import date
import pandas as pd

API_URL = "http://127.0.0.1:8000/"

# Function for Login
def login():
    st.title("Login")
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        payload = {
            "username": username,
            "password": password
        }
        try:
            # Send POST request to the backend for login
            response = requests.post(f"{API_URL}token", data=payload)
            if response.status_code == 200:
                token = response.json().get("access_token")
                # Store token in session state for later use
                st.session_state.token = token
                st.success("Login successful!")
                st.rerun()  # Force a page refresh to show the updated state
            else:
                st.error(f"Login failed: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# Function for Sign Up
def sign_up():
    st.title("Sign Up")
    with st.form(key="signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        payload = {
            "username": username,
            "password": password
        }
        try:
            # Send POST request to the backend to create a new user
            response = requests.post(f"{API_URL}users/", json=payload)
            if response.status_code == 200:
                st.success("User created successfully! You can now log in.")
            else:
                st.error(f"Error: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# Function for Logging Out
def log_out():
    if "token" in st.session_state:
        del st.session_state.token
        st.success("Logged out successfully.")
        st.rerun()  # Trigger a page refresh to clear session state

# Function to show the sidebar with login or app options
def show_sidebar():
    if "token" in st.session_state:
        # User is logged in, show app options
        with st.sidebar:
            st.header("Welcome to the Personal Finance Tracker")
            option = st.radio(
                "Choose an option:",
                ("New Transaction", "List Transactions", "Analysis", "Log Out")
            )
        return option
    else:
        # User is not logged in, show login/signup form
        option = st.sidebar.radio(
            "Choose an option:",
            ("Login", "Sign Up")
        )
        return option

# Main Logic
option = show_sidebar()

if option == "Login":
    login()

elif option == "Sign Up":
    sign_up()

elif option == "Log Out":
    log_out()

# Handle the different page options if user is logged in
if "token" in st.session_state:
    # Show New Transaction form
    if option == "New Transaction":
        st.title("New Transaction")

        with st.form(key="transaction_form"):
            amount = st.number_input("Amount", min_value=0.01, format="%.2f", step=0.01)
            type = st.radio("Type", ("Credit", "Debit"), horizontal= True)
            to_from = st.text_input("To/From(name)")
            CATEGORIES = ['Rent', 'Salary', 'Utilities', 'Food', 'Transportation', 'Entertainment', 'Study', 'Groceries','Other']
            category = st.selectbox("Category", CATEGORIES)
            transaction_date = st.date_input("Transaction Date", value=date.today())
            description = st.text_input("Description")
            submit_button = st.form_submit_button("Submit Transaction")

        if submit_button:
            payload = {
                "name": to_from,
                "amount": amount,
                "type": type,
                "category": category,
                "date": str(transaction_date),
                "description" : str(description),
            }

            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                response = requests.post(f"{API_URL}transactions/", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Transaction submitted successfully!")
                    st.write("Transaction Details:")
                    st.write(f"Type: {type}")
                    st.write(f"Amount: ₹{amount:.2f}")
                    st.write(f"Category: {category}")
                    st.write(f"Date: {transaction_date}")
                else:
                    st.error(f"Error: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

    # Show List of Transactions
    elif option == "List Transactions":
        st.title("Transactions List")

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}transactions/", headers=headers)
        if response.status_code == 200:
            transactions = response.json()
            df = pd.DataFrame(transactions)
            st.write(df)
        else:
            st.error(f"Error: {response.status_code}, {response.text}")

    # Show Analysis Content
    elif option == "Analysis":
        st.header("Analysis")
        st.write("Analyze your transactions with the following insights:")

        # Input Form for Date Range
        with st.form(key="transaction_form"):
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start date")
            with col2:
                end_date = st.date_input("End date")
            submit_button = st.form_submit_button("Submit")

        # If dates are submitted
        if submit_button:
            st.write(start_date, end_date)
            payload = {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d')
            }

            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                response = requests.get(f"{API_URL}transactions/summary/", json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # Display the Income vs Expense Summary
                    st.subheader("Income vs Expense Summary")
                    st.metric("Total Income", f"₹{data['total_income']}")
                    st.metric("Total Expense", f"₹{data['total_expense']}")
                    st.metric("Net Balance", f"₹{data['net_balance']}")

                    # Display the Category-Wise Breakdown
                    st.subheader("Category-Wise Expense Breakdown")
                    category_data = data["category_breakdown"]
                    
                    # Convert category_data to a DataFrame for better visualization
                    category_df = pd.DataFrame(category_data)
                    st.write(category_df)
                    
                    # Create a bar chart for Category-Wise Breakdown
                    st.bar_chart(category_df.set_index("category")["amount"])

                    # Display the Monthly Trends
                    st.subheader("Monthly Trends")
                    monthly_data = pd.DataFrame(data["monthly_trends"])

                    # Ensure the 'month' column is a string for better chart display
                    monthly_data["month"] = monthly_data["month"].astype(str)
                    st.line_chart(monthly_data.set_index("month"))

                    # Display the Top Transactions
                    st.subheader("Highest Transactions")
                    top_transactions = pd.DataFrame(data["top_transactions"])
                    st.table(top_transactions)
                else:
                    st.error(f"Error: {response.status_code}, {response.text}")

            except Exception as e:
                    st.error(f"An error occurred: {e}")

