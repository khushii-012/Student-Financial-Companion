import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="AI Personal Expense Tracker", layout="wide")

st.title("💰 AI Personal Expense Tracker")
st.markdown("Track your expenses, analyze spending, and get smart insights 📊")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Type", "Category", "Amount", "Note"
    ])

if "budget" not in st.session_state:
    st.session_state.budget = {}

# ----------------------------
# SIDEBAR MENU
# ----------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Transaction", "View Dashboard", "Budget Settings", "AI Insights"]
)

# ----------------------------
# ADD TRANSACTION
# ----------------------------
if menu == "Add Transaction":
    st.subheader("➕ Add Income / Expense")

    t_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category (Food, Travel, Bills, etc.)")
    amount = st.number_input("Amount", min_value=0.0, step=50.0)
    note = st.text_input("Note")
    date = st.date_input("Date", datetime.today())

    if st.button("Add Transaction"):
        new_data = pd.DataFrame([[date, t_type, category, amount, note]],
                                columns=st.session_state.data.columns)
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.success("Transaction Added Successfully ✅")

# ----------------------------
# DASHBOARD
# ----------------------------
elif menu == "View Dashboard":
    st.subheader("📊 Financial Dashboard")

    df = st.session_state.data

    if df.empty:
        st.warning("No data available yet.")
    else:
        col1, col2, col3 = st.columns(3)

        total_income = df[df["Type"] == "Income"]["Amount"].sum()
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expense

        col1.metric("Total Income", f"₹{total_income}")
        col2.metric("Total Expense", f"₹{total_expense}")
        col3.metric("Balance", f"₹{balance}")

        # ---------------- CATEGORY WISE EXPENSE ----------------
        st.markdown("### 📌 Category-wise Expenses")

        exp_df = df[df["Type"] == "Expense"]
        if not exp_df.empty:
            cat_data = exp_df.groupby("Category")["Amount"].sum()

            fig, ax = plt.subplots()
            cat_data.plot(kind="bar", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # ---------------- TRANSACTION TABLE ----------------
        st.markdown("### 📄 Transaction History")
        st.dataframe(df)

# ----------------------------
# BUDGET SETTINGS
# ----------------------------
elif menu == "Budget Settings":
    st.subheader("⚙️ Set Budget Limits")

    category = st.text_input("Category")
    limit = st.number_input("Set Budget Limit", min_value=0.0, step=100.0)

    if st.button("Save Budget"):
        st.session_state.budget[category] = limit
        st.success(f"Budget set for {category} ✔")

    st.markdown("### Current Budgets")
    st.write(st.session_state.budget)

# ----------------------------
# AI INSIGHTS
# ----------------------------
elif menu == "AI Insights":
    st.subheader("🧠 Smart AI Insights")

    df = st.session_state.data

    if df.empty:
        st.warning("No data to analyze yet.")
    else:
        exp_df = df[df["Type"] == "Expense"]

        st.markdown("### 🔍 Spending Analysis")

        total_spent = exp_df["Amount"].sum()
        st.write(f"Total Spending: ₹{total_spent}")

        # Highest spending category
        if not exp_df.empty:
            top_category = exp_df.groupby("Category")["Amount"].sum().idxmax()
            st.success(f"You are spending most on: **{top_category}**")

        # ---------------- AI RULE-BASED INSIGHTS ----------------
        st.markdown("### 🤖 AI Suggestions")

        for cat, limit in st.session_state.budget.items():
            spent = exp_df[exp_df["Category"] == cat]["Amount"].sum()

            if spent > limit:
                st.error(f"⚠ You exceeded budget in {cat} (₹{spent} / ₹{limit})")
            elif spent > 0.8 * limit:
                st.warning(f"⚠ You are close to budget limit in {cat}")
            else:
                st.info(f"✔ Spending is under control in {cat}")

        # General advice
        if total_spent > 10000:
            st.warning("💡 Tip: Your spending is high this month. Try reducing non-essential expenses.")
        else:
            st.success("💡 Good job! Your spending is under control.")