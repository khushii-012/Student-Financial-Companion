import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ----------------------------
# BASIC CONFIG + CUSTOM CSS
# ----------------------------
st.set_page_config(
    page_title="Student Expense Tracker",
    layout="wide",
    page_icon="🎓"
)

custom_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 40%, #111827 100%);
    color: #e5e7eb;
}
.block-container {
    padding-top: 1rem;
}
.card {
    background-color: #020617;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #1f2937;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.5);
}
h1, h2, h3 {
    color: #e5e7eb;
}
[data-testid="stMetricValue"] {
    font-size: 1.4rem;
    font-weight: 700;
}
[data-testid="stSidebar"] {
    background-color: #020617;
}
.stButton > button {
    border-radius: 999px;
    background: linear-gradient(135deg, #6366f1, #22c55e);
    color: white;
    padding: 0.4rem 1rem;
    border: none;
    font-weight: 600;
}
.stButton > button:hover {
    filter: brightness(1.05);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background-color: #020617;
    border-radius: 999px;
    border: 1px solid #4b5563;
    color: #e5e7eb;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.markdown(
    "<h1 style='text-align: center;'>🎓 Student Expense Tracker</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color:#9ca3af;'>Simple multi‑student tracker: just describe what you spent, and the app understands the category.</p>",
    unsafe_allow_html=True,
)
st.write("")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Student", "Date", "Type", "Category", "Amount", "Description", "Note"]
    )

if "budget" not in st.session_state:
    st.session_state.budget = {}

# ----------------------------
# RULE-BASED CATEGORY DETECTION
# ----------------------------
def guess_category_from_text(text: str) -> str:
    if not text:
        return "Others"

    t = text.lower()

    food_keywords = [
        "zomato", "swiggy", "dominos", "pizza", "burger", "mcdonald", "kfc",
        "restaurant", "hotel", "lunch", "dinner", "snacks", "food", "cafeteria",
        "cafe", "mess", "canteen", "khana", "nashta"
    ]
    if any(k in t for k in food_keywords):
        return "Food"

    travel_keywords = [
        "uber", "ola", "auto", "bus", "train", "cab", "taxi", "flight",
        "petrol", "diesel", "fuel", "metro", "rickshaw"
    ]
    if any(k in t for k in travel_keywords):
        return "Travel"

    rent_keywords = ["rent", "pg", "hostel", "room", "flat"]
    if any(k in t for k in rent_keywords):
        return "Rent"

    bills_keywords = ["electricity", "wifi", "internet", "mobile recharge", "recharge", "bill", "dth"]
    if any(k in t for k in bills_keywords):
        return "Bills"

    study_keywords = [
        "book", "books", "notebook", "pen", "pencil", "stationery",
        "coaching", "tuition", "exam fee", "college fee", "course"
    ]
    if any(k in t for k in study_keywords):
        return "Study Materials"

    entertain_keywords = [
        "netflix", "prime", "spotify", "movie", "mall", "shopping",
        "clothes", "shoes", "game", "pubg", "bgmi"
    ]
    if any(k in t for k in entertain_keywords):
        return "Entertainment"

    income_keywords = ["scholarship", "stipend", "salary", "part time", "internship", "pocket money"]
    if any(k in t for k in income_keywords):
        return "Income"

    return "Others"

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("## 📂 Menu")
    menu = st.selectbox(
        "",
        ["Add Expense / Income", "View Dashboard", "Budget Settings", "AI Insights"],
        key="menu_select",
    )
    st.markdown("---")
    st.markdown("#### ℹ️ App Info")
    st.caption("• Focus on expenses, income optional")
    st.caption("• Auto category & multi‑student support")

# ----------------------------
# ADD EXPENSE / INCOME
# ----------------------------
if menu == "Add Expense / Income":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("➕ Add Student Expense (or Income)")

        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("Student Name", key="student_name_add")

            description = st.text_input(
                "Describe what happened (e.g. 'aaj Zomato pe 500 spend kiye')",
                key="description_input_add",
            )

            # Guess category and type
            suggested_category = guess_category_from_text(description)
            # If description clearly looks like income, type = Income, else Expense
            if suggested_category == "Income":
                default_type = "Income"
                suggested_category_for_select = "Others"
            else:
                default_type = "Expense"
                suggested_category_for_select = suggested_category

            # Type is still there but secondary (for analytics)
            type_display = st.radio(
                "Is this Expense or Income?",
                ["Expense", "Income"],
                index=0 if default_type == "Expense" else 1,
                key="type_radio_add",
                horizontal=True,
            )

            categories = [
                "Rent",
                "Food",
                "Travel",
                "Bills",
                "Shopping",
                "Study Materials",
                "Entertainment",
                "Others",
            ]
            if suggested_category_for_select in categories:
                cat_options = [suggested_category_for_select] + [
                    c for c in categories if c != suggested_category_for_select
                ]
            else:
                cat_options = categories

            category = st.selectbox(
                f"Category (suggested: {suggested_category_for_select})",
                cat_options,
                key="category_select_add",
            )

            amount = st.number_input(
                "Amount (₹)", min_value=0.0, step=50.0, key="amount_input_add"
            )

        with col2:
            date = st.date_input("Date", datetime.today(), key="date_input_add")
            note = st.text_input("Note (optional)", key="note_input_add")

        st.write("")
        if st.button("Save Entry", use_container_width=True, key="btn_add_entry"):
            if student_name.strip() == "":
                st.error("Please enter the student name.")
            elif amount <= 0:
                st.error("Amount should be greater than 0.")
            else:
                with st.spinner("Saving your entry..."):
                    new_data = pd.DataFrame(
                        [[student_name.strip(), date, type_display, category, amount, description, note]],
                        columns=st.session_state.data.columns,
                    )
                    st.session_state.data = pd.concat(
                        [st.session_state.data, new_data], ignore_index=True
                    )
                st.success(
                    f"{type_display} saved for {student_name.strip()} in '{category}' ✅"
                )
                st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# VIEW DASHBOARD
# ----------------------------
elif menu == "View Dashboard":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Student Expense Dashboard")

        df = st.session_state.data.copy()

        if df.empty:
            st.info("No data available yet. Please add some entries.")
        else:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            df["Date"] = pd.to_datetime(df["Date"])

            # Filters
            f1, f2, f3 = st.columns(3)
            with f1:
                students = sorted(df["Student"].unique().tolist())
                selected_student = st.selectbox(
                    "Select Student",
                    ["All Students"] + students,
                    key="student_filter_dashboard",
                )
            with f2:
                years = sorted(df["Date"].dt.year.unique().tolist())
                selected_year = st.selectbox(
                    "Year", ["All Years"] + years, key="year_filter_dashboard"
                )
            with f3:
                months = sorted(df["Date"].dt.month.unique().tolist())
                month_names = {
                    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
                    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
                    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
                }
                month_options = ["All Months"] + [month_names[m] for m in months]
                selected_month_label = st.selectbox(
                    "Month", month_options, key="month_filter_dashboard"
                )

            # Apply filters
            if selected_student != "All Students":
                df = df[df["Student"] == selected_student]
            if selected_year != "All Years":
                df = df[df["Date"].dt.year == selected_year]
            if selected_month_label != "All Months":
                month_num = [k for k, v in month_names.items() if v == selected_month_label][0]
                df = df[df["Date"].dt.month == month_num]

            # Quick filters
            st.markdown("### Quick Filters")
            q1, q2 = st.columns(2)
            with q1:
                only_this_month = st.checkbox("Show only this month", key="cb_this_month")
            with q2:
                only_expenses = st.checkbox("Show only expenses (hide income)", key="cb_only_expenses")

            if only_this_month:
                today = pd.Timestamp.today()
                df = df[(df["Date"].dt.year == today.year) & (df["Date"].dt.month == today.month)]
            if only_expenses:
                df = df[df["Type"] == "Expense"]

            if df.empty:
                st.info("No data for the selected filters.")
            else:
                tab1, tab2, tab3 = st.tabs(["📌 Summary", "📈 Charts", "📄 Table"])

                with tab1:
                    col1, col2, col3 = st.columns(3)
                    total_income = df[df["Type"] == "Income"]["Amount"].sum()
                    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
                    balance = total_income - total_expense

                    col1.metric("Total Income", f"₹{total_income:,.2f}")
                    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
                    col3.metric("Balance (Savings)", f"₹{balance:,.2f}")

                with tab2:
                    st.markdown("#### Category-wise Expenses")
                    exp_df = df[df["Type"] == "Expense"]

                    if not exp_df.empty:
                        cat_group = exp_df.groupby("Category", as_index=False)["Amount"].sum()
                        fig_cat = px.bar(
                            cat_group,
                            x="Category",
                            y="Amount",
                            title="Category-wise Expenses",
                            color="Category",
                            text_auto=".2f",
                            template="plotly_dark",
                        )
                        fig_cat.update_layout(
                            xaxis_title="Category",
                            yaxis_title="Amount (₹)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(15,23,42,1)",
                        )
                        st.plotly_chart(fig_cat, use_container_width=True)
                    else:
                        st.info("No expense data for this selection.")

                with tab3:
                    st.markdown("#### Transactions")
                    st.dataframe(
                        df.sort_values("Date", ascending=False),
                        use_container_width=True,
                    )

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# BUDGET SETTINGS
# ----------------------------
elif menu == "Budget Settings":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("⚙️ Set Budget Limits (per Category)")

        col1, col2 = st.columns(2)
        with col1:
            categories = [
                "Rent", "Food", "Travel", "Bills",
                "Shopping", "Study Materials", "Entertainment", "Others",
            ]
            category = st.selectbox(
                "Category", categories, key="category_select_budget"
            )
        with col2:
            limit = st.number_input(
                "Monthly Budget Limit (₹)",
                min_value=0.0,
                step=100.0,
                key="limit_input_budget",
            )

        if st.button("Save Budget", use_container_width=True, key="btn_save_budget"):
            st.session_state.budget[category] = limit
            st.success(f"Budget set for {category}: ₹{limit:,.2f} ✔")

        st.markdown("### Current Budgets")
        if st.session_state.budget:
            budget_df = pd.DataFrame(
                [
                    {"Category": cat, "Limit (₹)": lim}
                    for cat, lim in st.session_state.budget.items()
                ]
            )
            st.dataframe(budget_df, use_container_width=True)
        else:
            st.info("No budgets set yet. Add one above.")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# AI INSIGHTS
# ----------------------------
elif menu == "AI Insights":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧠 Smart Insights for Students")

        df = st.session_state.data.copy()

        if df.empty:
            st.warning("No data to analyze yet. Please add some entries.")
        else:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            df["Date"] = pd.to_datetime(df["Date"])

            students = sorted(df["Student"].unique().tolist())
            selected_student = st.selectbox(
                "Select Student for Insights",
                ["All Students"] + students,
                key="student_filter_insights",
            )

            if selected_student != "All Students":
                df = df[df["Student"] == selected_student]

            exp_df = df[df["Type"] == "Expense"]

            st.markdown("### 🔍 Spending Analysis")

            total_spent = exp_df["Amount"].sum()
            st.write(f"**Total Spending:** ₹{total_spent:,.2f}")

            if not exp_df.empty:
                top_category = exp_df.groupby("Category")["Amount"].sum().idxmax()
                st.success(f"Highest spending category: **{top_category}**")

            st.markdown("### 🎯 Spending Mood")
            if total_spent == 0:
                st.info("No expenses yet. Fresh start, perfect time to plan a budget!")
            elif total_spent < 2000:
                st.success("Very low spending. You are in **Ultra Saver** mode.")
            elif total_spent < 7000:
                st.info("Moderate spending. You are in **Balanced** mode.")
            else:
                st.warning("High spending. You are in **YOLO** mode, careful!")

            st.markdown("### 🤖 AI-style Suggestions")

            if not st.session_state.budget:
                st.info("Set some budgets in 'Budget Settings' to get personalized alerts.")
            else:
                for cat, limit in st.session_state.budget.items():
                    spent = exp_df[exp_df["Category"] == cat]["Amount"].sum()

                    if spent > limit:
                        st.error(
                            f"⚠ Over budget in {cat} (₹{spent:,.2f} / ₹{limit:,.2f})"
                        )
                    elif spent > 0.8 * limit:
                        st.warning(
                            f"⚠ Close to budget limit in {cat} (₹{spent:,.2f} / ₹{limit:,.2f})"
                        )
                    else:
                        st.info(
                            f"✔ Spending OK in {cat} (₹{spent:,.2f} / ₹{limit:,.2f})"
                        )

            with st.expander("See detailed tips"):
                st.write("- Track all food and travel expenses for one week.")
                st.write("- Set a strict limit for online food delivery.")
                st.write("- Try a ‘no-spend day’ challenge once a week.")

        st.markdown("</div>", unsafe_allow_html=True)