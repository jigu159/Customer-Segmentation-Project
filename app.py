import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation & Marketing",
    page_icon="👥",
    layout="wide"
)

# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

@st.cache_data
def load_data():
    file_path = (
        "data/customer_segmentation_exact.csv"
        if os.path.exists("data/customer_segmentation_exact.csv")
        else "customer_segmentation_exact.csv"
    )
    return pd.read_csv(file_path)


try:
    df = load_data()

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()
# ============================================================
# CUSTOM SIDEBAR
# ============================================================

# Default page
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# Selected customer
if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = str(
        df["CustomerID"].iloc[0]
    )


# ------------------------------------------------------------
# SIDEBAR STYLE
# ------------------------------------------------------------

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: #172554;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.sidebar-brand {
    text-align: center;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 20px;
}

.sidebar-brand-icon {
    font-size: 38px;
}

.sidebar-brand-title {
    color: white;
    font-size: 21px;
    font-weight: 800;
    line-height: 1.15;
}

.sidebar-brand-subtitle {
    color: #cbd5e1;
    font-size: 13px;
    margin-top: 5px;
}

.sidebar-section-title {
    color: white;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# APP BRANDING
# ------------------------------------------------------------

st.sidebar.markdown("""
<div class="sidebar-brand">

    <div class="sidebar-brand-icon">👥</div>

    <div class="sidebar-brand-title">
        Customer Segmentation<br>
        Platform
    </div>

    <div class="sidebar-brand-subtitle">
        Personalized Marketing Analytics
    </div>

</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# CUSTOMER DETAILS
# ------------------------------------------------------------

st.sidebar.markdown(
    '<div class="sidebar-section-title">'
    'Enter Customer Details'
    '</div>',
    unsafe_allow_html=True
)


customer_input = st.sidebar.text_input(
    "Customer ID",
    value=str(st.session_state.selected_customer_id)
)


# Find customer
typed_customer = df[
    df["CustomerID"].astype(str) == str(customer_input).strip()
]


if not typed_customer.empty:

    sidebar_customer = typed_customer.iloc[0]

    sidebar_age = sidebar_customer["Age"]
    sidebar_income = sidebar_customer["AnnualIncome"]
    sidebar_purchase = sidebar_customer["PurchaseHistory"]
    sidebar_spending = sidebar_customer["SpendingScore"]

else:

    sidebar_age = ""
    sidebar_income = ""
    sidebar_purchase = ""
    sidebar_spending = ""


st.sidebar.number_input(
    "Age",
    value=int(sidebar_age) if sidebar_age != "" else 0,
    disabled=True
)

st.sidebar.number_input(
    "Income (₹)",
    value=float(sidebar_income) if sidebar_income != "" else 0.0,
    disabled=True
)

st.sidebar.number_input(
    "Purchase History",
    value=int(sidebar_purchase) if sidebar_purchase != "" else 0,
    disabled=True
)

st.sidebar.number_input(
    "Spending Score (1 - 100)",
    value=float(sidebar_spending) if sidebar_spending != "" else 0.0,
    disabled=True
)


# ------------------------------------------------------------
# PREDICT / LOAD CUSTOMER BUTTON
# ------------------------------------------------------------

if st.sidebar.button(
    "🔍  Predict Customer",
    use_container_width=True
):

    if not typed_customer.empty:

        st.session_state.selected_customer_id = str(
            customer_input
        )

        st.session_state.page = "🏠 Home"

        st.rerun()

    else:

        st.sidebar.error(
            "Customer ID not found."
        )


# ------------------------------------------------------------
# RESET BUTTON
# ------------------------------------------------------------

if st.sidebar.button(
    "↻  Reset",
    use_container_width=True
):

    st.session_state.selected_customer_id = str(
        df["CustomerID"].iloc[0]
    )

    st.session_state.page = "🏠 Home"

    st.rerun()


st.sidebar.markdown("---")


# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------

if st.sidebar.button(
    "🏠  Home",
    use_container_width=True
):
    st.session_state.page = "🏠 Home"
    st.rerun()


if st.sidebar.button(
    "📊  Dashboard",
    use_container_width=True
):
    st.session_state.page = "📊 Dashboard"
    st.rerun()


if st.sidebar.button(
    "👥  Customer Segments",
    use_container_width=True
):
    st.session_state.page = "👥 Customer Segments"
    st.rerun()


if st.sidebar.button(
    "👤  Customer Analysis",
    use_container_width=True
):
    st.session_state.page = "👤 Customer Analysis"
    st.rerun()


if st.sidebar.button(
    "💡  Marketing Suggestions",
    use_container_width=True
):
    st.session_state.page = "💡 Marketing Suggestions"
    st.rerun()


# Current page
page = st.session_state.page

# ============================================================
# HOME PAGE - MODERN DASHBOARD STYLE
# ============================================================

if page == "🏠 Home":

    # --------------------------------------------------------
    # DESIGN
    # --------------------------------------------------------

    st.markdown("""
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 25px;
    }

    .top-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 4px 14px rgba(15,23,42,0.08);
        min-height: 140px;
    }

    .card-title {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 10px;
    }

    .card-value {
        font-size: 27px;
        font-weight: 800;
        color: #1e293b;
    }

    .section-box {
        padding: 20px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 4px 14px rgba(15,23,42,0.06);
        margin-bottom: 20px;
    }

    .marketing-card {
        padding: 18px;
        border-radius: 14px;
        background: white;
        border: 1px solid #e2e8f0;
        min-height: 150px;
        box-shadow: 0px 3px 10px rgba(15,23,42,0.06);
    }

    .marketing-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .marketing-text {
        font-size: 14px;
        color: #475569;
        line-height: 1.5;
    }

    </style>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # CUSTOMER SELECTION
    # --------------------------------------------------------

    customer_ids = sorted(
        df["CustomerID"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_customer_id = st.sidebar.selectbox(
        "Select Customer ID",
        customer_ids
    )

    customer_data = df[
        df["CustomerID"] == selected_customer_id
    ]

    customer = customer_data.iloc[0]


    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">'
        '👥 Customer Segmentation & Personalized Marketing Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Analyze customer behavior, understand segments, and generate '
        'personalized marketing strategies.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------------

    st.success(
        f"Customer {customer['CustomerID']} loaded successfully!"
    )


    # --------------------------------------------------------
    # TOP 3 CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="top-card">
                <div class="card-title">
                    👥 Customer Segment
                </div>

                <div class="card-value">
                    {customer['Customer_Segment']}
                </div>

                <div class="card-title">
                    Current customer segment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="top-card">
                <div class="card-title">
                    📊 K-Means Cluster
                </div>

                <div class="card-value">
                    {customer['KMeans_Cluster']}
                </div>

                <div class="card-title">
                    Assigned customer cluster
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="top-card">
                <div class="card-title">
                    🛍️ Spending Score
                </div>

                <div class="card-value">
                    {customer['SpendingScore']} / 100
                </div>

                <div class="card-title">
                    Customer spending behavior
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # --------------------------------------------------------
    # CUSTOMER PROFILE + VISUALIZATION
    # --------------------------------------------------------

    col1, col2 = st.columns([1, 1.6])


    # --------------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------------

    with col1:

        st.subheader("👤 Customer Profile")

        profile = pd.DataFrame({
            "Field": [
                "Customer ID",
                "Age",
                "Annual Income",
                "Purchase History",
                "Spending Score",
                "Segment",
                "Cluster"
            ],

            "Value": [
                customer["CustomerID"],
                f"{int(customer['Age'])} Years",
                f"₹{float(customer['AnnualIncome']):,.0f}",
                f"{int(customer['PurchaseHistory'])} Purchases",
                f"{float(customer['SpendingScore']):.0f} / 100",
                customer["Customer_Segment"],
                customer["KMeans_Cluster"]
            ]
        })

        st.dataframe(
            profile,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # CUSTOMER VISUALIZATION
    # --------------------------------------------------------

    with col2:

        st.subheader("📈 Customer Visualization")

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        segments = df[
            "Customer_Segment"
        ].dropna().unique()


        for segment in segments:

            segment_data = df[
                df["Customer_Segment"] == segment
            ]

            ax.scatter(
                segment_data["AnnualIncome"],
                segment_data["SpendingScore"],
                label=segment,
                alpha=0.65
            )


        # Highlight selected customer

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            s=300,
            edgecolors="black",
            linewidths=1.5,
            label="Selected Customer"
        )


        ax.set_title(
            "Annual Income vs Spending Score"
        )

        ax.set_xlabel(
            "Annual Income"
        )

        ax.set_ylabel(
            "Spending Score"
        )

        ax.legend()

        ax.grid(
            True,
            alpha=0.20
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    st.divider()


    # --------------------------------------------------------
    # MARKETING SUGGESTIONS
    # --------------------------------------------------------

    st.subheader(
        "💡 Personalized Marketing Suggestions"
    )

    st.write(
        "Marketing strategies available for each customer segment."
    )


    budget = df[
        df["Customer_Segment"] == "Budget"
    ]

    regular = df[
        df["Customer_Segment"] == "Regular"
    ]

    premium = df[
        df["Customer_Segment"] == "Premium"
    ]

    vip = df[
        df["Customer_Segment"] == "VIP"
    ]


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="marketing-card">
                <div class="marketing-title">
                    💰 Budget
                </div>

                <div class="marketing-text">
                    {
                        budget["Marketing_Suggestion"].iloc[0]
                        if not budget.empty
                        else "No suggestion available."
                    }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="marketing-card">
                <div class="marketing-title">
                    🛍️ Regular
                </div>

                <div class="marketing-text">
                    {
                        regular["Marketing_Suggestion"].iloc[0]
                        if not regular.empty
                        else "No suggestion available."
                    }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="marketing-card">
                <div class="marketing-title">
                    💎 Premium
                </div>

                <div class="marketing-text">
                    {
                        premium["Marketing_Suggestion"].iloc[0]
                        if not premium.empty
                        else "No suggestion available."
                    }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="marketing-card">
                <div class="marketing-title">
                    👑 VIP
                </div>

                <div class="marketing-text">
                    {
                        vip["Marketing_Suggestion"].iloc[0]
                        if not vip.empty
                        else "No suggestion available."
                    }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <br>

        <div style="
            text-align:center;
            color:#64748b;
            font-size:13px;
            padding:20px;
        ">
            Customer Segmentation & Personalized Marketing Platform
            <br>
            Built with Python, Pandas, Matplotlib and Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Customers",
            len(df)
        )

    with col2:

        st.metric(
            "Average Income",
            f"{df['AnnualIncome'].mean():,.0f}"
        )

    with col3:

        st.metric(
            "Average Spending Score",
            f"{df['SpendingScore'].mean():.2f}"
        )

    with col4:

        st.metric(
            "Number of Segments",
            df["Customer_Segment"].nunique()
        )

    st.divider()

    # ========================================================
    # SEGMENT DISTRIBUTION
    # ========================================================

    st.subheader("👥 Customer Segment Distribution")

    segment_counts = df["Customer_Segment"].value_counts()

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(7, 5))

        segment_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Customers by Segment")
        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Number of Customers")

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)

    with col2:

        fig, ax = plt.subplots(figsize=(7, 5))

        segment_counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_title("Segment Distribution")
        ax.set_ylabel("")

        st.pyplot(fig)

        plt.close(fig)

    st.divider()

    # ========================================================
    # INCOME VS SPENDING
    # ========================================================

    st.subheader("💰 Annual Income vs Spending Score")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        df["AnnualIncome"],
        df["SpendingScore"]
    )

    ax.set_title("Income vs Spending Score")
    ax.set_xlabel("Annual Income")
    ax.set_ylabel("Spending Score")

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # AVERAGE INCOME BY SEGMENT
    # ========================================================

    st.subheader("📈 Average Income by Segment")

    avg_income = (
        df.groupby("Customer_Segment")["AnnualIncome"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    avg_income.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Annual Income by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average Annual Income")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # AVERAGE SPENDING BY SEGMENT
    # ========================================================

    st.subheader("🛍️ Average Spending Score by Segment")

    avg_spending = (
        df.groupby("Customer_Segment")["SpendingScore"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    avg_spending.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Spending Score by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average Spending Score")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # COMPLETE DATASET
    # ========================================================

    st.subheader("📋 Complete Customer Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

elif page == "👥 Customer Segments":

    st.title("👥 Customer Segmentation")

    st.write(
        "Customers are grouped into four segments based on their purchasing behavior."
    )

    # ========================================================
    # CSS
    # ========================================================

    st.markdown(
        """
        <style>

        .segment-card {
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #d9d9d9;
            background-color: black;
            text-align: center;
            min-height: 145px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        }

        .segment-title {
            font-size: 21px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .segment-count {
            font-size: 30px;
            font-weight: 700;
        }

        .segment-label {
            font-size: 14px;
            color: #666;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CREATE SEGMENTS
    # ========================================================

    budget = df[
        df["Customer_Segment"] == "Budget"
    ]

    regular = df[
        df["Customer_Segment"] == "Regular"
    ]

    premium = df[
        df["Customer_Segment"] == "Premium"
    ]

    vip = df[
        df["Customer_Segment"] == "VIP"
    ]


    # ========================================================
    # TOP SEGMENT CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">💰 Budget</div>
                <div class="segment-count">{len(budget)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">🛍️ Regular</div>
                <div class="segment-count">{len(regular)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">💎 Premium</div>
                <div class="segment-count">{len(premium)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">👑 VIP</div>
                <div class="segment-count">{len(vip)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # ========================================================
    # FUNCTION TO DISPLAY SEGMENT
    # ========================================================

    def display_segment(segment_name, segment_data):

        st.subheader(
            f"Customers - {segment_name}"
        )

        st.dataframe(
            segment_data[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not segment_data.empty:

            suggestion = (
                segment_data["Marketing_Suggestion"]
                .dropna()
                .unique()
            )

            for item in suggestion:

                st.info(item)


    # ========================================================
    # BUDGET + REGULAR
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💰 Budget Customers")

        st.dataframe(
            budget[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not budget.empty:

            st.info(
                budget["Marketing_Suggestion"].iloc[0]
            )


    with col2:

        st.markdown("### 🛍️ Regular Customers")

        st.dataframe(
            regular[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not regular.empty:

            st.info(
                regular["Marketing_Suggestion"].iloc[0]
            )


    st.divider()


    # ========================================================
    # PREMIUM + VIP
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💎 Premium Customers")

        st.dataframe(
            premium[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not premium.empty:

            st.info(
                premium["Marketing_Suggestion"].iloc[0]
            )


    with col2:

        st.markdown("### 👑 VIP Customers")

        st.dataframe(
            vip[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not vip.empty:

            st.info(
                vip["Marketing_Suggestion"].iloc[0]
            )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "👤 Customer Analysis":

    st.title("👤 Customer Analysis")

    st.write(
        "Select a Customer ID to view complete customer details."
    )

    customer_ids = sorted(
        df["CustomerID"].dropna().unique().tolist()
    )

    selected_customer_id = st.selectbox(
        "Select Customer ID",
        customer_ids
    )

    customer_data = df[
        df["CustomerID"] == selected_customer_id
    ]

    if not customer_data.empty:

        customer = customer_data.iloc[0]

        st.success(
            f"Customer found: {customer['CustomerID']}"
        )

        st.subheader("📋 Complete Customer Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Customer ID:**",
                customer["CustomerID"]
            )

            st.write(
                "**Age:**",
                int(customer["Age"])
            )

            st.write(
                "**Annual Income:**",
                f"{float(customer['AnnualIncome']):,.2f}"
            )

            st.write(
                "**Purchase History:**",
                int(customer["PurchaseHistory"])
            )

            st.write(
                "**Spending Score:**",
                float(customer["SpendingScore"])
            )

        with col2:

            st.write(
                "**Cluster:**",
                customer["Cluster"]
            )

            st.write(
                "**K-Means Cluster:**",
                customer["KMeans_Cluster"]
            )

            st.write(
                "**Customer Segment:**",
                customer["Customer_Segment"]
            )

        st.divider()

        st.subheader("💡 Marketing Suggestion")

        st.info(
            customer["Marketing_Suggestion"]
        )
# ============================================================
# MARKETING SUGGESTIONS
# ============================================================

elif page == "💡 Marketing Suggestions":

    st.title("💡 Marketing Suggestions")

    st.write(
        "Recommended marketing strategies for each customer segment."
    )

    st.divider()

    segments = [
        "Budget",
        "Regular",
        "Premium",
        "VIP"
    ]

    for segment in segments:

        segment_data = df[
            df["Customer_Segment"] == segment
        ]

        if not segment_data.empty:

            st.subheader(
                f"👥 {segment} Customers"
            )

            st.write(
                f"Total Customers: **{len(segment_data)}**"
            )

            suggestions = (
                segment_data["Marketing_Suggestion"]
                .dropna()
                .unique()
            )

            for suggestion in suggestions:

                st.info(suggestion)

            st.divider()
