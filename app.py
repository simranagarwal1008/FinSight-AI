import pandas as pd
import plotly.express as px
import streamlit as st

from database import (
    init_db,
    load_data,
    update_database,
    get_uploaded_files,
    delete_file_data,
    clear_all_data,
)
from processor import process_uploaded_file
from ai_engine import ask_ai_about_finances, execute_read_only_sql

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ============================================================
# PROFESSIONAL BLUE UI
# ============================================================
st.markdown(
    """
    <style>
    /* App background */
    .stApp { background: #f5f7fb; }
    .main .block-container {
        max-width: 1450px;
        padding: 2rem 2.5rem 3rem 2.5rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1f3a 0%, #102f56 100%);
        min-width: 260px;
    }
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0b1f3a 0%, #102f56 100%);
    }
    section[data-testid="stSidebar"] * { color: #eef5ff; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.14); }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #9fb4cf !important;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .08em;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] { gap: 7px; }
    section[data-testid="stSidebar"] [role="radio"] {
        border-radius: 10px;
        padding: 10px 12px;
        margin: 1px 0;
        border: 1px solid transparent;
        transition: all .15s ease;
    }
    section[data-testid="stSidebar"] [role="radio"]:hover {
        background: rgba(255,255,255,.09);
        border-color: rgba(255,255,255,.10);
    }
    section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
        background: #1e6ee7;
        border-color: #4b91f2;
        box-shadow: 0 7px 20px rgba(0,0,0,.18);
    }
    section[data-testid="stSidebar"] [role="radio"] > div:first-child { display: none; }
    .sidebar-brand { font-size: 1.45rem; font-weight: 800; letter-spacing: -.03em; }
    .sidebar-sub { color: #9fb4cf !important; font-size: .78rem; margin-top: -4px; }
    .sidebar-bottom {
        color: #7f9abb !important;
        font-size: .72rem;
        line-height: 1.5;
        margin-top: 18px;
    }

    /* Page header */
    .page-title {
        font-size: 2.25rem;
        font-weight: 800;
        color: #10233f;
        letter-spacing: -.04em;
        margin: 0;
    }
    .page-subtitle { color: #64748b; margin-top: .25rem; font-size: .98rem; }
    .top-badge {
        display: inline-block;
        background: #e8f1ff;
        color: #1769d2;
        border: 1px solid #cfe2ff;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: .76rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0f4c9b 0%, #1f78e0 65%, #318cf0 100%);
        border-radius: 18px;
        padding: 28px 30px;
        color: white;
        box-shadow: 0 12px 30px rgba(25, 92, 173, .18);
        margin-bottom: 22px;
    }
    .hero h2 { margin: 0; font-size: 1.75rem; letter-spacing: -.025em; }
    .hero p { margin: 8px 0 0; color: #dcecff; font-size: .95rem; }

    /* Cards */
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 17px 18px;
        box-shadow: 0 4px 14px rgba(15, 35, 63, .05);
        min-height: 112px;
    }
    .metric-label { color: #64748b; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
    .metric-value { color: #10233f; font-size: 1.55rem; font-weight: 800; margin-top: 7px; }
    .metric-blue { border-top: 4px solid #1f78e0; }
    .metric-green { border-top: 4px solid #159570; }
    .metric-red { border-top: 4px solid #e05252; }
    .metric-purple { border-top: 4px solid #7357d9; }

    /* Section headings */
    .section-head { margin: 28px 0 12px; color: #10233f; font-size: 1.15rem; font-weight: 800; }
    .section-note { color: #718096; font-size: .88rem; margin-top: -5px; margin-bottom: 12px; }

    /* Streamlit containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e2e8f0 !important;
        border-radius: 15px !important;
        background: white;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 40px;
        border: 1px solid #cbd5e1;
        background: white;
    }
    .stButton > button[kind="primary"] {
        background: #1e6ee7;
        border-color: #1e6ee7;
        color: white;
    }
    .stButton > button[kind="primary"]:hover {
        background: #155fc9;
        border-color: #155fc9;
    }

    /* Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
        border-radius: 9px;
    }
    
    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">💳 FinSight AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Personal Finance Intelligence</div>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "💳  Transactions",
            "📊  Analytics",
            "🤖  AI Analyst",
            "⚙️  Data Manager",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown(
        '<div class="sidebar-bottom">Built with<br>Python · Streamlit · SQLite<br>Pandas · Plotly · Gemini AI</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# DATA
# ============================================================
try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load database: {exc}")
    st.stop()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")


def money(value):
    return f"₹{value:,.0f}"


def calculate_metrics(data):
    income = data.loc[data["amount"] > 0, "amount"].sum()
    expenses = abs(data.loc[data["amount"] < 0, "amount"].sum())
    return income, expenses, income - expenses, len(data)


def metric_cards(data):
    income, expenses, net, count = calculate_metrics(data)
    cards = [
        ("TOTAL INCOME", money(income), "metric-green"),
        ("TOTAL EXPENSES", money(expenses), "metric-red"),
        ("NET CASH FLOW", money(net), "metric-blue"),
        ("TRANSACTIONS", f"{count:,}", "metric-purple"),
    ]
    cols = st.columns(4)
    for col, (label, value, cls) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="metric-card {cls}"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
                unsafe_allow_html=True,
            )


def expense_data(data):
    expenses = data[data["amount"] < 0].copy()
    expenses["spend"] = expenses["amount"].abs()
    return expenses


# ============================================================
# DASHBOARD
# ============================================================
if page.startswith("🏠"):
    st.markdown('<div class="top-badge">FINANCIAL COMMAND CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Good to see you 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Understand where your money goes and make better spending decisions.</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown(
        '<div class="hero"><h2>Take control of your finances.</h2><p>Upload your bank statement, explore your spending patterns, and ask FinSight AI questions about your financial data.</p></div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="section-head" style="margin-top:0">📁 Upload Bank Statement</div>', unsafe_allow_html=True)
        st.caption("CSV should contain Date, Description and Amount columns.")
        upload_col, button_col = st.columns([4, 1])
        with upload_col:
            uploaded_file = st.file_uploader(
                "Choose CSV file",
                type=["csv"],
                label_visibility="collapsed",
            )
        with button_col:
            process_clicked = st.button("Process & Analyze", type="primary", use_container_width=True)

        if uploaded_file is not None and process_clicked:
            try:
                with st.spinner("Processing transactions..."):
                    new_count, dup_count = process_uploaded_file(uploaded_file)
                st.success(f"Added {new_count} new transactions • Ignored {dup_count} duplicates")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    if df.empty:
        st.info("No transactions yet. Upload a CSV bank statement above to start using FinSight AI.")
    else:
        st.markdown('<div class="section-head">Financial Overview</div>', unsafe_allow_html=True)
        metric_cards(df)

        expenses = expense_data(df)
        st.markdown('<div class="section-head">Spending Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">A quick view of your spending distribution and daily activity.</div>', unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.markdown("**Spending by Category**")
                if expenses.empty:
                    st.info("No expenses available.")
                else:
                    cat = expenses.groupby("category", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
                    fig = px.pie(cat, values="spend", names="category", hole=0.55)
                    fig.update_layout(
                        height=360,
                        margin=dict(t=15, b=10, l=10, r=10),
                        legend=dict(orientation="v"),
                        font=dict(color="#334155"),
                    )
                    st.plotly_chart(fig, use_container_width=True)

        with right:
            with st.container(border=True):
                st.markdown("**Daily Spending Trend**")
                if expenses.empty:
                    st.info("No expenses available.")
                else:
                    trend = expenses.groupby("date", as_index=False)["spend"].sum()
                    fig = px.area(trend, x="date", y="spend")
                    fig.update_layout(
                        height=360,
                        margin=dict(t=15, b=10, l=10, r=10),
                        xaxis_title=None,
                        yaxis_title="Spend (₹)",
                    )
                    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TRANSACTIONS
# ============================================================
elif page.startswith("💳"):
    st.markdown('<div class="top-badge">TRANSACTION LEDGER</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Search and filter every transaction stored in your local database.</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No transactions available. Upload a CSV from Dashboard.")
    else:
        st.write("")
        f1, f2, f3 = st.columns([2, 1.3, 1.2])
        with f1:
            search = st.text_input("Search description", placeholder="e.g. Amazon, Uber, salary...")
        with f2:
            categories = sorted(df["category"].dropna().unique().tolist())
            selected_categories = st.multiselect("Category", categories)
        with f3:
            transaction_type = st.selectbox("Type", ["All", "Income", "Expense"])

        filtered = df.copy()
        if search:
            filtered = filtered[filtered["description"].str.contains(search, case=False, na=False)]
        if selected_categories:
            filtered = filtered[filtered["category"].isin(selected_categories)]
        if transaction_type == "Income":
            filtered = filtered[filtered["amount"] > 0]
        elif transaction_type == "Expense":
            filtered = filtered[filtered["amount"] < 0]

        st.caption(f"Showing {len(filtered):,} of {len(df):,} transactions")
        display_df = filtered.copy()
        display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)

# ============================================================
# ANALYTICS
# ============================================================
elif page.startswith("📊"):
    st.markdown('<div class="top-badge">SMART FINANCIAL ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Turn raw transactions into useful financial insights.</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("Upload transactions to unlock analytics.")
    else:
        st.write("")
        metric_cards(df)
        expenses = expense_data(df)

        if not expenses.empty:
            category_spend = (
                expenses.groupby("category", as_index=False)["spend"]
                .sum()
                .sort_values("spend", ascending=False)
            )
            category_spend["% of expenses"] = (
                category_spend["spend"] / category_spend["spend"].sum() * 100
            ).round(1)

            st.markdown('<div class="section-head">Top Spending Categories</div>', unsafe_allow_html=True)
            c1, c2 = st.columns([1.25, .75])
            with c1:
                fig = px.bar(
                    category_spend.head(8).sort_values("spend"),
                    x="spend",
                    y="category",
                    orientation="h",
                )
                fig.update_layout(height=360, margin=dict(t=15, b=15, l=10, r=10), xaxis_title="Spend (₹)", yaxis_title=None)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.dataframe(
                    category_spend.rename(columns={"spend": "Spend (₹)"}),
                    use_container_width=True,
                    hide_index=True,
                    height=360,
                )

            st.markdown('<div class="section-head">Monthly Income vs Expense</div>', unsafe_allow_html=True)
            monthly = df.copy()
            monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
            monthly["income"] = monthly["amount"].where(monthly["amount"] > 0, 0)
            monthly["expense"] = monthly["amount"].where(monthly["amount"] < 0, 0).abs()
            monthly = monthly.groupby("month", as_index=False)[["income", "expense"]].sum()
            monthly_long = monthly.melt("month", var_name="type", value_name="amount")
            fig = px.bar(monthly_long, x="month", y="amount", color="type", barmode="group")
            fig.update_layout(height=380, margin=dict(t=15, b=15, l=10, r=10), xaxis_title=None, yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="section-head">Highest Individual Expenses</div>', unsafe_allow_html=True)
            top_expenses = expenses.sort_values("spend", ascending=False).head(10).copy()
            top_expenses["date"] = top_expenses["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(
                top_expenses[["date", "description", "category", "spend"]].rename(columns={"spend": "Amount (₹)"}),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown('<div class="section-head">Quick Insights</div>', unsafe_allow_html=True)
            avg_daily = expenses.groupby("date")["spend"].sum().mean()
            top_category = category_spend.iloc[0]
            largest = top_expenses.iloc[0]
            q1, q2, q3 = st.columns(3)
            q1.metric("Average Daily Spend", money(avg_daily))
            q2.metric("Top Category", str(top_category["category"]))
            q3.metric("Largest Expense", money(largest["spend"]))

# ============================================================
# AI ANALYST
# ============================================================
elif page.startswith("🤖"):
    st.markdown('<div class="top-badge">GEMINI-POWERED ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">AI Financial Analyst</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ask questions about your transactions in plain English.</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("Upload transactions first so FinSight AI has data to analyze.")
    else:
        st.write("")
        with st.container(border=True):
            st.markdown("**💬 Ask FinSight AI**")
            st.caption("Gemini converts your question into a read-only SQLite query and returns the result from your local database.")
            examples = [
                "What is my total spending?",
                "Which category did I spend the most on?",
                "Show my top 5 expenses.",
                "How much did I spend on Food & Drink?",
                "What is my total income?",
            ]
            st.markdown("**Try asking:** " + "  •  ".join(examples[:3]))
            user_query = st.text_input(
                "Question",
                placeholder="e.g. Which category has the highest spending?",
                label_visibility="collapsed",
            )
            ask_clicked = st.button("✨ Analyze with AI", type="primary")

        if ask_clicked:
            if not user_query.strip():
                st.warning("Please enter a question first.")
            else:
                schema = "id INTEGER, date TEXT, description TEXT, amount REAL, category TEXT, source_file TEXT"
                try:
                    with st.spinner("FinSight AI is analyzing your data..."):
                        generated_sql = ask_ai_about_finances(user_query, schema)
                        result = execute_read_only_sql(generated_sql)

                    if isinstance(result, pd.DataFrame):
                        st.success("Analysis complete")
                        st.markdown('<div class="section-head">Result</div>', unsafe_allow_html=True)
                        st.dataframe(result, use_container_width=True, hide_index=True)
                        with st.expander("View technical details"):
                            st.caption("This is the read-only SQL generated by Gemini.")
                            st.code(generated_sql, language="sql")
                    else:
                        st.error(result)
                except Exception as exc:
                    st.error(f"AI analysis failed: {exc}")
                    st.caption("Check that GEMINI_API_KEY is present in your .env file.")

# ============================================================
# DATA MANAGER
# ============================================================
else:
    st.markdown('<div class="top-badge">DATABASE MANAGEMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Data Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage uploaded files and manually correct transaction records.</div>', unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="section-head" style="margin-top:0">📂 Uploaded Files</div>', unsafe_allow_html=True)
        files_list = get_uploaded_files()
        if files_list:
            for filename in files_list:
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.write(f"📄 **{filename}**")
                with c2:
                    if st.button("Delete", key=f"delete_{filename}", use_container_width=True):
                        delete_file_data(filename)
                        st.success(f"Deleted transactions from {filename}.")
                        st.rerun()
        else:
            st.caption("No uploaded files found.")

    st.markdown('<div class="section-head">✏️ Interactive Ledger</div>', unsafe_allow_html=True)
    if not df.empty:
        editable = df.copy()
        editable["date"] = editable["date"].dt.strftime("%Y-%m-%d")
        edited_df = st.data_editor(
            editable,
            use_container_width=True,
            hide_index=True,
            disabled=["id", "source_file"],
            num_rows="fixed",
        )
        if st.button("Save Manual Edits", type="primary"):
            try:
                update_database(edited_df)
                st.success("Ledger updated successfully.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save edits: {exc}")
    else:
        st.info("Your ledger is empty.")

    st.markdown('<div class="section-head">⚠️ Danger Zone</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.caption("This permanently removes all transactions from the local SQLite database.")
        if st.button("Delete All Transactions"):
            clear_all_data()
            st.success("All transaction data deleted.")
            st.rerun()
