import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ----------------------------
# PAGE CONFIG (full-width)
# ----------------------------
st.set_page_config(
    page_title="WalletIQ – Papa ke paise manager",
    layout="wide",
    page_icon="💸"
)

# ----------------------------
# DARK THEME CSS (WALLET IQ)
# ----------------------------
APP_CSS = """
<style>
.stApp {
    background: radial-gradient(circle at top, #020617 0, #020617 40%, #000000 100%);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main container full width */
.block-container {
    padding-top: 0.6rem;
    padding-bottom: 2rem;
    max-width: 1400px; /* wider than before */
}

/* WalletIQ top bar */
.top-bar {
    background: #020617;
    border-bottom: 1px solid #1f2937;
    padding: 0.6rem 0.75rem 0.5rem 0.75rem;
    margin-bottom: 0.6rem;
}
.top-bar-left {
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #e5e7eb;
}
.top-bar-right {
    font-size: 0.8rem;
    color: #9ca3af;
    text-align: right;
}

/* Hero strip */
.hero-strip {
    background: linear-gradient(130deg, #0f172a 0%, #1e293b 40%, #581c87 100%);
    border-radius: 22px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 1.0rem;
    box-shadow: 0 30px 60px rgba(15, 23, 42, 0.9);
}

/* Cards */
.card {
    background: #020617;
    border-radius: 18px;
    padding: 1.1rem 1.3rem;
    border: 1px solid #1f2937;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.85);
    margin-bottom: 0.8rem;
}

/* Section titles */
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e5e7eb;
}

/* Accent bar for navigation */
.nav-accent {
    height: 4px;
    width: 40px;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e, #6366f1);
    margin-bottom: 0.4rem;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e5e7eb;
}

/* Buttons */
.stButton > button {
    border-radius: 999px;
    background: linear-gradient(135deg, #22c55e, #6366f1);
    color: white;
    padding: 0.4rem 1.1rem;
    border: none;
    font-weight: 600;
    font-size: 0.9rem;
}
.stButton > button:hover {
    filter: brightness(1.05);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background-color: #020617;
    border-radius: 999px;
    border: 1px solid #334155;
    color: #e5e7eb;
    font-size: 0.9rem;
}

/* Radio, selectbox */
.stRadio > div {
    gap: 0.5rem;
}
.stSelectbox > div > div {
    border-radius: 999px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    background-color: #020617;
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    border: 1px solid #1f2937;
    color: #e5e7eb;
}

/* DataFrame header */
[data-testid="stDataFrame"] thead tr th {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# ----------------------------
# TOP BAR – WalletIQ
# ----------------------------
st.markdown(
    """
    <div class="top-bar">
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <div class="top-bar-left">
          💸 WALLETIQ
        </div>
        <div class="top-bar-right">
          Your personal assistant for managing papa ne bheje huye paise
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# HERO STRIP – Taglines
# ----------------------------
st.markdown(
    """
    <div class="hero-strip">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div style="max-width:65%;">
          <div style="font-size:1.4rem; font-weight:700;">
            WalletIQ – monthly pocket money, fully under control.
          </div>
          <div style="font-size:0.9rem; margin-top:0.2rem; color:#cbd5f5;">
            Track papa ke paise: rent, food, travel, udhaar with friends – sab ek hi jagah.
          </div>
        </div>
        <div style="text-align:right; font-size:0.8rem; color:#9ca3af;">
          "Papa ne bheja, WalletIQ ne sambhala."<br/>
          "Jitna dikhega, utna bachega."
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# SESSION STATE
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Student", "Date", "Type", "Category", "Amount", "Description", "Note"]
    )

if "lent" not in st.session_state:
    st.session_state.lent = pd.DataFrame(
        columns=["Friend", "Date", "Amount", "Note", "Repaid?"]
    )

if "borrowed" not in st.session_state:
    st.session_state.borrowed = pd.DataFrame(
        columns=["Friend", "Date", "Amount", "Note", "Repaid?"]
    )

if "budget" not in st.session_state:
    st.session_state.budget = {}

if "profile" not in st.session_state:
    st.session_state.profile = "Hosteller"

if "monthly_papa_money" not in st.session_state:
    st.session_state.monthly_papa_money = 0.0

if "saving_goals" not in st.session_state:
    st.session_state.saving_goals = []  # list of dicts: {name, target, saved}

# ----------------------------
# CATEGORY GUESS
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
# HELPER: CURRENT MONTH FILTER
# ----------------------------
def filter_current_month(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    today = pd.Timestamp.today()
    return df[(df["Date"].dt.year == today.year) & (df["Date"].dt.month == today.month)]

# ----------------------------
# MAIN NAV (full width)
# ----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='nav-accent'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📁 WalletIQ sections</div>", unsafe_allow_html=True)
menu = st.radio(
    "",
    [
        "Add Entry",
        "View Dashboard",
        "Expense History",
        "AI Insights",
        "Friends Udhaar",
        "Split Bill",
        "Setup & Goals",
    ],
    horizontal=True,
    key="menu_radio",
)
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# ADD ENTRY + QUICK PRESETS + BUDGETS
# ----------------------------
if menu == "Add Entry":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>✏️ Add today’s story</div>", unsafe_allow_html=True)
    st.caption("Har kharcha note karo – kal papa poochhenge, WalletIQ ke paas jawab hoga.")

    # Profile + presets row
    p_col1, p_col2 = st.columns([2, 3])

    with p_col1:
        st.markdown("##### Student profile")
        profile = st.radio(
            "Profile type",
            ["Hosteller", "Day scholar"],
            index=0 if st.session_state.profile == "Hosteller" else 1,
            key="profile_radio",
            horizontal=True,
        )
        st.session_state.profile = profile

        if st.button("Load preset budgets", key="btn_load_presets"):
            if profile == "Hosteller":
                st.session_state.budget = {
                    "Rent": 4000,
                    "Food": 2500,
                    "Travel": 1500,
                    "Bills": 800,
                    "Shopping": 1000,
                    "Study Materials": 800,
                    "Entertainment": 1200,
                    "Others": 500,
                }
            else:  # Day scholar
                st.session_state.budget = {
                    "Rent": 0,
                    "Food": 2500,
                    "Travel": 2500,
                    "Bills": 600,
                    "Shopping": 1000,
                    "Study Materials": 800,
                    "Entertainment": 1200,
                    "Others": 500,
                }
            st.success(f"Preset budgets loaded for {profile} ✅")

    with p_col2:
        st.markdown("##### Quick add buttons")
        q_col1, q_col2, q_col3 = st.columns(3)
        quick_category = None
        quick_desc = ""

        with q_col1:
            if st.button("🏠 Rent", key="btn_quick_rent"):
                quick_category = "Rent"
                quick_desc = "Monthly room/PG/hostel rent"
        with q_col2:
            if st.button("🍛 Mess", key="btn_quick_mess"):
                quick_category = "Food"
                quick_desc = "Mess / canteen food"
        with q_col3:
            if st.button("🚗 Uber", key="btn_quick_uber"):
                quick_category = "Travel"
                quick_desc = "Uber / Ola / cab ride"

    # Entry form (full-width)
    student_name = st.text_input("Student name", key="student_name_add")

    description_default = quick_desc if quick_desc else ""
    description = st.text_input(
        "What happened? (e.g. 'aaj Zomato pe 500 spend kiye')",
        value=description_default,
        key="description_input_add",
    )

    if quick_category:
        suggested_category = quick_category
    else:
        suggested_category = guess_category_from_text(description)

    if suggested_category == "Income":
        default_type = "Income"
        suggested_for_select = "Others"
    else:
        default_type = "Expense"
        suggested_for_select = suggested_category

    type_display = st.radio(
        "Type",
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
    if suggested_for_select in categories:
        cat_options = [suggested_for_select] + [c for c in categories if c != suggested_for_select]
    else:
        cat_options = categories

    category = st.selectbox(
        f"Category (suggested: {suggested_for_select})",
        cat_options,
        key="category_select_add",
    )

    form_col1, form_col2, form_col3 = st.columns(3)
    with form_col1:
        amount = st.number_input(
            "Amount (₹)", min_value=0.0, step=50.0, key="amount_input_add"
        )
    with form_col2:
        date_value = st.date_input("Date", datetime.today(), key="date_input_add")
    with form_col3:
        note = st.text_input("Note (optional)", key="note_input_add")

    if st.button("Save entry", use_container_width=True, key="btn_add_entry"):
        if student_name.strip() == "":
            st.error("Please enter the student name.")
        elif amount <= 0:
            st.error("Amount should be greater than 0.")
        else:
            new_data = pd.DataFrame(
                [[student_name.strip(), date_value, type_display, category, amount, description, note]],
                columns=st.session_state.data.columns,
            )
            st.session_state.data = pd.concat(
                [st.session_state.data, new_data], ignore_index=True
            )
            st.success(
                f"{type_display} saved for {student_name.strip()} in '{category}' ✅"
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Budgets card (full-width)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ Budgets (per category)</div>", unsafe_allow_html=True)
    st.caption("Papa ne jo bheja hai, uska limit decide karo – WalletIQ yaad dilayega.")

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        budget_categories = [
            "Rent", "Food", "Travel", "Bills",
            "Shopping", "Study Materials", "Entertainment", "Others",
        ]
        b_category = st.selectbox(
            "Category", budget_categories, key="category_select_budget"
        )
    with b_col2:
        b_limit = st.number_input(
            "Monthly limit (₹)",
            min_value=0.0,
            step=100.0,
            key="limit_input_budget",
        )

    if st.button("Save budget", use_container_width=True, key="btn_save_budget"):
        st.session_state.budget[b_category] = b_limit
        st.success(f"Budget set for {b_category}: ₹{b_limit:,.2f} ✔")

    if st.session_state.budget:
        budget_df = pd.DataFrame(
            [
                {"Category": cat, "Limit (₹)": lim}
                for cat, lim in st.session_state.budget.items()
            ]
        )
        st.dataframe(budget_df, use_container_width=True, height=220)
    else:
        st.caption("No budgets set yet. Add one above.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# FRIENDS UDHAR + NET PER FRIEND
# ----------------------------
elif menu == "Friends Udhaar":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🤝 Friends & Udhaar</div>", unsafe_allow_html=True)
    st.caption("Hostel life = udhaar. WalletIQ yaad rakhega kisne kitna liya aur tumne kitna liya.")

    tabs = st.tabs(["You lent (friends ne tumse liya)", "You borrowed (tumne friends se liya)"])

    with tabs[0]:
        st.markdown("#### You lent money")
        l_friend = st.text_input("Friend name", key="lent_friend")
        l_amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, key="lent_amount")
        l_date = st.date_input("Date", datetime.today(), key="lent_date")
        l_note = st.text_input("Note (optional)", key="lent_note")
        l_repaid = st.checkbox("Marked as repaid?", key="lent_repaid")

        if st.button("Save lent record", use_container_width=True, key="btn_lent"):
            if l_friend.strip() == "" or l_amount <= 0:
                st.error("Friend name and amount are required.")
            else:
                new_lent = pd.DataFrame(
                    [[l_friend.strip(), l_date, l_amount, l_note, "Yes" if l_repaid else "No"]],
                    columns=st.session_state.lent.columns,
                )
                st.session_state.lent = pd.concat(
                    [st.session_state.lent, new_lent], ignore_index=True
                )
                st.success("Udhaar (you lent) saved ✅")

        if not st.session_state.lent.empty:
            lent_df = st.session_state.lent.copy()
            total_lent = lent_df[~(lent_df["Repaid?"] == "Yes")]["Amount"].sum()
            st.metric("Total friends still owe you", f"₹{total_lent:,.2f}")
            st.dataframe(lent_df.sort_values("Date", ascending=False), use_container_width=True)
        else:
            st.caption("No records yet. Add when you lend money to a friend.")

    with tabs[1]:
        st.markdown("#### You borrowed money")
        b_friend = st.text_input("Friend name", key="borrow_friend")
        b_amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, key="borrow_amount")
        b_date = st.date_input("Date", datetime.today(), key="borrow_date")
        b_note = st.text_input("Note (optional)", key="borrow_note")
        b_repaid = st.checkbox("Marked as repaid?", key="borrow_repaid")

        if st.button("Save borrowed record", use_container_width=True, key="btn_borrow"):
            if b_friend.strip() == "" or b_amount <= 0:
                st.error("Friend name and amount are required.")
            else:
                new_borrow = pd.DataFrame(
                    [[b_friend.strip(), b_date, b_amount, b_note, "Yes" if b_repaid else "No"]],
                    columns=st.session_state.borrowed.columns,
                )
                st.session_state.borrowed = pd.concat(
                    [st.session_state.borrowed, new_borrow], ignore_index=True
                )
                st.success("Udhaar (you borrowed) saved ✅")

        if not st.session_state.borrowed.empty:
            borrowed_df = st.session_state.borrowed.copy()
            total_owe = borrowed_df[~(borrowed_df["Repaid?"] == "Yes")]["Amount"].sum()
            st.metric("Total you still owe friends", f"₹{total_owe:,.2f}")
            st.dataframe(borrowed_df.sort_values("Date", ascending=False), use_container_width=True)
        else:
            st.caption("No records yet. Add when you borrow money from a friend.")

    # Net position per friend summary
    st.markdown("#### Net position per friend")
    if not st.session_state.lent.empty or not st.session_state.borrowed.empty:
        lent_df = st.session_state.lent.copy()
        borrowed_df = st.session_state.borrowed.copy()

        lent_df["Amount"] = pd.to_numeric(lent_df["Amount"], errors="coerce")
        borrowed_df["Amount"] = pd.to_numeric(borrowed_df["Amount"], errors="coerce")

        lent_open = lent_df[lent_df["Repaid?"] != "Yes"]
        borrowed_open = borrowed_df[borrowed_df["Repaid?"] != "Yes"]

        lent_sum = lent_open.groupby("Friend")["Amount"].sum()
        borrowed_sum = borrowed_open.groupby("Friend")["Amount"].sum()

        friends = sorted(set(lent_sum.index) | set(borrowed_sum.index))
        summary_rows = []
        for friend in friends:
            they_owe = lent_sum.get(friend, 0.0)
            you_owe = borrowed_sum.get(friend, 0.0)
            net = they_owe - you_owe
            if net > 0:
                status = "They owe you"
            elif net < 0:
                status = "You owe them"
            else:
                status = "Settled"
            summary_rows.append(
                {"Friend": friend, "Net (₹)": net, "Status": status}
            )

        net_df = pd.DataFrame(summary_rows)
        st.dataframe(net_df, use_container_width=True)
    else:
        st.caption("No udhaar data yet to calculate net positions.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# SPLIT BILL CALCULATOR
# ----------------------------
elif menu == "Split Bill":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🧮 Split Bill with Friends</div>", unsafe_allow_html=True)
    st.caption("Cafe, Swiggy, trip – WalletIQ se fair split nikalo.")

    total_bill = st.number_input("Total bill amount (₹)", min_value=0.0, step=50.0, key="split_total")
    tax = st.number_input("Tax / service charge (₹)", min_value=0.0, step=10.0, key="split_tax")
    tip = st.number_input("Tip (₹)", min_value=0.0, step=10.0, key="split_tip")

    num_people = st.number_input("Number of people (including you)", min_value=1, step=1, key="split_people")

    names_input = st.text_input(
        "Names (optional, comma separated – e.g. Khushi, Aditi, Rahul)",
        key="split_names",
    )

    if st.button("Calculate split", use_container_width=True, key="btn_split_calc"):
        total = total_bill + tax + tip
        if total <= 0 or num_people <= 0:
            st.error("Bill amount and number of people should be greater than 0.")
        else:
            per_head = total / num_people
            st.success(f"Each person should pay approximately ₹{per_head:,.2f}")

            if names_input.strip():
                names = [n.strip() for n in names_input.split(",") if n.strip()]
                while len(names) < num_people:
                    names.append(f"Friend {len(names)+1}")
                names = names[:num_people]

                split_df = pd.DataFrame(
                    [{"Person": n, "Share (₹)": per_head} for n in names]
                )
                st.dataframe(split_df, use_container_width=True)
            else:
                st.caption("Add names above if you want to see a per‑friend table.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# SETUP & SAVING GOALS
# ----------------------------
elif menu == "Setup & Goals":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ Monthly setup & goals</div>", unsafe_allow_html=True)
    st.caption("Yahan se WalletIQ ko batayo papa kitna bhejte, aur tum kya save karna chahte ho.")

    mp_col1, mp_col2 = st.columns(2)
    with mp_col1:
        monthly_papa = st.number_input(
            "Papa sends per month (₹)",
            min_value=0.0,
            step=100.0,
            value=st.session_state.monthly_papa_money,
            key="monthly_papa_input",
        )
    with mp_col2:
        pocket_day = st.number_input(
            "Day of month when papa usually sends (1–31)",
            min_value=1,
            max_value=31,
            step=1,
            value=1,
            key="papa_day_input",
        )

    if st.button("Save monthly setup", use_container_width=True, key="btn_save_monthly"):
        st.session_state.monthly_papa_money = monthly_papa
        st.success("Monthly papa‑money setup saved ✅")

    st.markdown("### 🎯 Saving goals")
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        goal_name = st.text_input("Goal name (e.g. Fest, Emergency)", key="goal_name_input")
    with g_col2:
        goal_target = st.number_input(
            "Target amount (₹)",
            min_value=0.0,
            step=100.0,
            key="goal_target_input",
        )
    with g_col3:
        goal_saved_now = st.number_input(
            "Already saved (₹)",
            min_value=0.0,
            step=100.0,
            key="goal_saved_input",
        )

    if st.button("Add / update goal", use_container_width=True, key="btn_add_goal"):
        if goal_name.strip() == "" or goal_target <= 0:
            st.error("Goal name and positive target are required.")
        else:
            updated = False
            for g in st.session_state.saving_goals:
                if g["name"] == goal_name.strip():
                    g["target"] = goal_target
                    g["saved"] = goal_saved_now
                    updated = True
                    break
            if not updated:
                st.session_state.saving_goals.append(
                    {"name": goal_name.strip(), "target": goal_target, "saved": goal_saved_now}
                )
            st.success("Saving goal saved ✅")

    if st.session_state.saving_goals:
        goals_df = pd.DataFrame(st.session_state.saving_goals)
        st.dataframe(goals_df, use_container_width=True)
    else:
        st.caption("No saving goals yet. Add one above.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# DASHBOARD (papa-money + daily chart)
# ----------------------------
elif menu == "View Dashboard":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Dashboard</div>", unsafe_allow_html=True)

    df = st.session_state.data.copy()

    if df.empty:
        st.info("No data available yet. Please add some entries.")
    else:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"])

        f1, f2, f3 = st.columns(3)
        with f1:
            students = sorted(df["Student"].unique().tolist())
            selected_student = st.selectbox(
                "Student",
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

        if selected_student != "All Students":
            df = df[df["Student"] == selected_student]
        if selected_year != "All Years":
            df = df[df["Date"].dt.year == selected_year]
        if selected_month_label != "All Months":
            month_num = [k for k, v in month_names.items() if v == selected_month_label][0]
            df = df[df["Date"].dt.month == month_num]

        q1, q2 = st.columns(2)
        with q1:
            only_this_month = st.checkbox("Only this month", key="cb_this_month")
        with q2:
            only_expenses = st.checkbox("Only expenses", key="cb_only_expenses")

        if only_this_month:
            df = filter_current_month(df)
        if only_expenses:
            df = df[df["Type"] == "Expense"]

        if df.empty:
            st.info("No data for the selected filters.")
        else:
            current_month_df = filter_current_month(st.session_state.data.copy())
            current_month_df["Amount"] = pd.to_numeric(current_month_df["Amount"], errors="coerce")

            bheja = current_month_df[current_month_df["Type"] == "Income"]["Amount"].sum()
            uda = current_month_df[current_month_df["Type"] == "Expense"]["Amount"].sum()
            expected_from_papa = st.session_state.monthly_papa_money

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Papa ne kitna bheja (recorded)", f"₹{bheja:,.2f}")
            m2.metric("Papa monthly setup", f"₹{expected_from_papa:,.2f}")
            m3.metric("Kitna uda diya (this month)", f"₹{uda:,.2f}")
            m4.metric("Abhi bacha (bheja − uda)", f"₹{bheja - uda:,.2f}")

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
                st.markdown("#### Expenses by category")
                exp_df = df[df["Type"] == "Expense"]

                if not exp_df.empty:
                    cat_group = exp_df.groupby("Category", as_index=False)["Amount"].sum()
                    fig_cat = px.bar(
                        cat_group,
                        x="Category",
                        y="Amount",
                        title="Expenses by category",
                        color="Category",
                        text_auto=".2f",
                        template="plotly_dark",
                    )
                    fig_cat.update_layout(
                        xaxis_title="Category",
                        yaxis_title="Amount (₹)",
                        plot_bgcolor="#020617",
                        paper_bgcolor="#020617",
                        font_color="#e5e7eb",
                    )
                    st.plotly_chart(fig_cat, use_container_width=True)
                else:
                    st.info("No expense data for this selection.")

                st.markdown("#### Daily spending (simple chart)")
                if not exp_df.empty:
                    daily = exp_df.groupby(exp_df["Date"].dt.date, as_index=False)["Amount"].sum()
                    daily["Date"] = pd.to_datetime(daily["Date"])
                    fig_daily = px.bar(
                        daily,
                        x="Date",
                        y="Amount",
                        title="Daily spending this month",
                        template="plotly_dark",
                    )
                    fig_daily.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Amount (₹)",
                        plot_bgcolor="#020617",
                        paper_bgcolor="#020617",
                        font_color="#e5e7eb",
                    )
                    st.plotly_chart(fig_daily, use_container_width=True)
                else:
                    st.info("No daily expense data for this selection.")

            with tab3:
                st.markdown("#### Transactions")
                st.dataframe(
                    df.sort_values("Date", ascending=False),
                    use_container_width=True,
                    height=350,
                )

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# EXPENSE HISTORY
# ----------------------------
elif menu == "Expense History":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📜 Expense History</div>", unsafe_allow_html=True)
    st.caption("Pure log of papa ke paise: kab, kis cheez pe, kitna kharcha hua.")

    df = st.session_state.data.copy()

    if df.empty:
        st.info("No expenses recorded yet. Add some entries first.")
    else:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"])

        f1, f2, f3 = st.columns(3)
        with f1:
            students = sorted(df["Student"].unique().tolist())
            selected_student = st.selectbox(
                "Student",
                ["All Students"] + students,
                key="hist_student",
            )
        with f2:
            categories = sorted(df["Category"].unique().tolist())
            selected_category = st.selectbox(
                "Category",
                ["All Categories"] + categories,
                key="hist_category",
            )
        with f3:
            types = ["Expense", "Income"]
            selected_type = st.selectbox(
                "Type",
                ["All Types"] + types,
                key="hist_type",
            )

        if selected_student != "All Students":
            df = df[df["Student"] == selected_student]
        if selected_category != "All Categories":
            df = df[df["Category"] == selected_category]
        if selected_type != "All Types":
            df = df[df["Type"] == selected_type]

        if df.empty:
            st.info("No records match these filters.")
        else:
            st.markdown("#### Last 30 records")
            df_sorted = df.sort_values("Date", ascending=False).head(30)
            st.dataframe(df_sorted, use_container_width=True, height=350)

            total_spent = df_sorted[df_sorted["Type"] == "Expense"]["Amount"].sum()
            total_income = df_sorted[df_sorted["Type"] == "Income"]["Amount"].sum()
            st.metric("Total expenses in view", f"₹{total_spent:,.2f}")
            st.metric("Total income in view", f"₹{total_income:,.2f}")

            csv = df_sorted.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download this history as CSV",
                data=csv,
                file_name="walletiq_expense_history.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# AI INSIGHTS (saving goals + month-end summary)
# ----------------------------
elif menu == "AI Insights":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🧠 Smart Insights</div>", unsafe_allow_html=True)

    df = st.session_state.data.copy()

    if df.empty:
        st.warning("No data to analyze yet. Please add some entries.")
    else:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"])

        students = sorted(df["Student"].unique().tolist())
        selected_student = st.selectbox(
            "Student for insights",
            ["All Students"] + students,
            key="student_filter_insights",
        )

        if selected_student != "All Students":
            df = df[df["Student"] == selected_student]

        exp_df = df[df["Type"] == "Expense"]

        st.markdown("### 🔍 Spending analysis (this month)")
        current_month_df = filter_current_month(df)
        total_spent_month = current_month_df[current_month_df["Type"] == "Expense"]["Amount"].sum()
        st.write(f"**Total spending this month:** ₹{total_spent_month:,.2f}")

        if not exp_df.empty:
            top_category = exp_df.groupby("Category")["Amount"].sum().idxmax()
            st.success(f"Highest spending category: **{top_category}**")

        st.markdown("### 🎯 Spending mood")
        if total_spent_month == 0:
            st.info("No expenses yet. Fresh start, perfect time to plan a budget with papa.")
        elif total_spent_month < 2000:
            st.success("Very low spending. You are in **Ultra Saver** mode – papa proud.")
        elif total_spent_month < 7000:
            st.info("Moderate spending. You are in **Balanced** mode.")
        else:
            st.warning("High spending. You are in **YOLO** mode – thoda control karo.")

        st.markdown("### 🤖 Smart nudges")
        if not st.session_state.budget:
            st.info("Set some budgets in the Add Entry panel to get personalized alerts.")
        else:
            for cat, limit in st.session_state.budget.items():
                cat_spent = current_month_df[
                    (current_month_df["Type"] == "Expense") &
                    (current_month_df["Category"] == cat)
                ]["Amount"].sum()

                if cat_spent > limit:
                    st.error(
                        f"⚠ Over budget in {cat} (₹{cat_spent:,.2f} / ₹{limit:,.2f})"
                    )
                elif cat_spent > 0.8 * limit:
                    st.warning(
                        f"⚠ Close to budget in {cat} (₹{cat_spent:,.2f} / ₹{limit:,.2f})"
                    )
                else:
                    st.info(
                        f"✔ Spending OK in {cat} (₹{cat_spent:,.2f} / ₹{limit:,.2f})"
                    )

        st.markdown("### 💰 Saving goals progress")
        if st.session_state.saving_goals:
            for g in st.session_state.saving_goals:
                name = g["name"]
                target = g["target"]
                saved = g["saved"]
                pct = (saved / target * 100) if target > 0 else 0
                st.write(f"- {name}: ₹{saved:,.2f} / ₹{target:,.2f} ({pct:.1f}%)")
                if pct >= 100:
                    st.success(f"Goal **{name}** completed! 🎉")
                elif pct >= 70:
                    st.info(f"Goal **{name}** almost done, bas thoda aur.")
                else:
                    st.caption(f"Slow and steady: keep adding to **{name}**.")
        else:
            st.caption("No saving goals yet. Add them in the Setup & Goals tab.")

        st.markdown("### 📅 Month‑end summary (last month)")
        if not df.empty:
            df["year"] = df["Date"].dt.year
            df["month"] = df["Date"].dt.month
            today = pd.Timestamp.today()
            last_month_year = today.year
            last_month = today.month - 1
            if last_month == 0:
                last_month = 12
                last_month_year -= 1

            last_df = df[(df["year"] == last_month_year) & (df["month"] == last_month)]
            if last_df.empty:
                st.caption("No data for last month yet.")
            else:
                total_income_last = last_df[last_df["Type"] == "Income"]["Amount"].sum()
                total_expense_last = last_df[last_df["Type"] == "Expense"]["Amount"].sum()
                balance_last = total_income_last - total_expense_last

                st.write(
                    f"Last month papa ne bheja (recorded): ₹{total_income_last:,.2f}, "
                    f"tumne uda diya: ₹{total_expense_last:,.2f}, "
                    f"bacha hua: ₹{balance_last:,.2f}."
                )

                if not last_df[last_df["Type"] == "Expense"].empty:
                    top_cat_last = (
                        last_df[last_df["Type"] == "Expense"]
                        .groupby("Category")["Amount"]
                        .sum()
                        .idxmax()
                    )
                    st.write(f"Most spending last month was in **{top_cat_last}**.")

        with st.expander("See detailed tips"):
            st.write("- Track all food and travel expenses for one week.")
            st.write("- Set a strict limit for online food delivery.")
            st.write("- Try a ‘no-spend day’ challenge once a week.")
            st.write("- Use presets (Rent, Mess, Uber) so nothing gets missed.")

    st.markdown("</div>", unsafe_allow_html=True)