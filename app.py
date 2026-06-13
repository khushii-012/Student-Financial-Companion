import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ----------------------------
# DATABASE FUNCTIONS
# ----------------------------

def save_budget(income, rent, food, travel, study, entertainment, misc):
    conn = sqlite3.connect("expense.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO budget
    (
        monthly_income,
        rent_limit,
        food_limit,
        travel_limit,
        study_limit,
        entertainment_limit,
        misc_limit
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        income,
        rent,
        food,
        travel,
        study,
        entertainment,
        misc
    ))

    conn.commit()
    conn.close()


def save_expense(expense_date, amount, category, description):
    conn = sqlite3.connect("expense.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses
    (
        date,
        amount,
        category,
        description
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        expense_date,
        amount,
        category,
        description
    ))

    conn.commit()
    conn.close()


def get_latest_budget():
    conn = sqlite3.connect("expense.db")

    query = """
    SELECT monthly_income
    FROM budget
    ORDER BY id DESC
    LIMIT 1
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if len(df) == 0:
        return 0

    return df.iloc[0]["monthly_income"]


def get_total_expenses():
    conn = sqlite3.connect("expense.db")

    query = """
    SELECT SUM(amount) AS total
    FROM expenses
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if pd.isna(df.iloc[0]["total"]):
        return 0

    return df.iloc[0]["total"]


# ----------------------------
# STREAMLIT UI
# ----------------------------

st.set_page_config(
    page_title="Student Financial Companion",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Student Financial Companion")

st.markdown("""
### Your AI Financial Friend

Track expenses, manage pocket money,
and avoid running out of money before month-end.
""")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Budget Planner",
        "Add Expense",
        "Expense Analytics"
    ]
)

# ----------------------------
# DASHBOARD
# ----------------------------

if menu == "Dashboard":

    budget = get_latest_budget()
    spent = get_total_expenses()
    remaining = budget - spent

    st.header("🏠 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Budget",
            f"₹{budget:,.0f}"
        )

    with col2:
        st.metric(
            "Total Spent",
            f"₹{spent:,.0f}"
        )

    with col3:
        st.metric(
            "Remaining Balance",
            f"₹{remaining:,.0f}"
        )

# ----------------------------
# BUDGET PLANNER
# ----------------------------

elif menu == "Budget Planner":

    st.header("💰 Budget Planner")

    income = st.number_input(
        "Monthly Pocket Money",
        min_value=0
    )

    rent = st.number_input(
        "Rent Budget",
        min_value=0
    )

    food = st.number_input(
        "Food Budget",
        min_value=0
    )

    travel = st.number_input(
        "Travel Budget",
        min_value=0
    )

    study = st.number_input(
        "Study Budget",
        min_value=0
    )

    entertainment = st.number_input(
        "Entertainment Budget",
        min_value=0
    )

    misc = st.number_input(
        "Misc Budget",
        min_value=0
    )

    if st.button("Save Budget"):

        save_budget(
            income,
            rent,
            food,
            travel,
            study,
            entertainment,
            misc
        )

        st.success("✅ Budget Saved Successfully!")

# ----------------------------
# ADD EXPENSE
# ----------------------------

elif menu == "Add Expense":

    st.header("➕ Add Expense")

    amount = st.number_input(
        "Amount",
        min_value=0
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Study",
            "Entertainment",
            "Rent",
            "Misc"
        ]
    )

    description = st.text_input(
        "Description"
    )

    expense_date = str(date.today())

    if st.button("Add Expense"):

        save_expense(
            expense_date,
            amount,
            category,
            description
        )

        st.success("✅ Expense Added Successfully!")

# ----------------------------
# ANALYTICS
# ----------------------------

elif menu == "Expense Analytics":

    st.header("📊 Expense Analytics")

    st.info(
        "Charts and AI insights will be added in the next version."
    )