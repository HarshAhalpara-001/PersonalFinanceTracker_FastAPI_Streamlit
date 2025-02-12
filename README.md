﻿# PersonalFinanceTracker_FastAPI_Streamlit
# Personal Finance Tracker

A simple and efficient personal finance tracker built using **FastAPI**, **SQLite**, and **Streamlit**. This application allows users to track their income and expenses, get detailed breakdowns, view monthly trends, and keep an eye on their financial health.

## Features

- **Income and Expense Summary**: Get a quick overview of your total income, expenses, and net balance.
- **Category-Wise Breakdown**: View your expenses categorized by type (e.g., Food, Utilities, Transportation, etc.).
- **Monthly Trends**: Track your income and expense trends on a monthly basis.
- **Top Transactions**: See a list of your highest transactions with detailed information.

## Technologies Used

- **FastAPI**: For building the backend API.
- **SQLite**: For storing financial data.
- **Streamlit**: For creating interactive web-based data visualizations and interfaces.
  
## Setup and Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- SQLite (SQLite comes pre-installed with Python)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/PersonalFinanceTracker.git
   cd PersonalFinanceTracker
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI backend server:

   ```bash
   uvicorn main:app --reload
   ```

5. In a separate terminal, run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

6. Visit `http://localhost:8501` to use the finance tracker web app.

## Usage

- The app allows users to add, update, and delete transactions.
- The **Income vs Expense Summary** gives you a snapshot of your finances.
- Use the **Category-Wise Breakdown** to see how much you're spending in different categories.
- View your financial **trends** over time with the **Monthly Trends** chart.
- Keep track of your highest transactions under **Top Transactions**.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
