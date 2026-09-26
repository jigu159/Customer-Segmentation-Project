import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    if os.path.exists("data/customer_segmentation_exact.csv"):
        file_path = "data/customer_segmentation_exact.csv"
    else:
        file_path = "customer_segmentation_exact.csv"

    return pd.read_csv(file_path)


try:
    df = load_data()

except Exception as e:
    st.error(f"Unable to load customer data: {e}")
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = str(
        df["CustomerID"].iloc[0]
    )


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

    /* ================= MAIN ================= */

    [data-testid="stAppViewContainer"] {
        background: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background: #f7f9fc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* ================= SIDEBAR ================= */

    [data-testid="stSidebar"] {
        background: #17263e;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] input {
        background: white !important;
        color: #172033 !important;
        border-radius: 7px !important;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        font-weight: 700 !important;
    }


    /* ================= HEADINGS ================= */

    h1 {
        color: #172033 !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #24344d !important;
        font-weight: 750 !important;
    }


    /* ================= TABLES ================= */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #dfe6ef;
    }


    /* ================= ALERTS ================= */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SELECTED CUSTOMER
# ============================================================

selected_id = str(
    st.session_state.selected_customer_id
)

selected_rows = df[
    df["CustomerID"].astype(str) == selected_id
]

if selected_rows.empty:

    selected_id = str(df["CustomerID"].iloc[0])

    selected_rows = df[
        df["CustomerID"].astype(str) == selected_id
    ]

customer = selected_rows.iloc[0]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.html("""
    <div style="
        text-align:center;
        padding:8px 4px 20px 4px;
        border-bottom:1px solid rgba(255,255,255,0.25);
        margin-bottom:20px;
    ">

        <div style="
            font-size:36px;
            margin-bottom:6px;
        ">
            👥
        </div>

        <div style="
            color:white;
            font-size:21px;
            font-weight:800;
            line-height:1.15;
        ">
            Customer Segmentation<br>
            Platform
        </div>

        <div style="
            color:#cbd5e1;
            font-size:12px;
            margin-top:7px;
        ">
            Personalized Marketing Analytics
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------------

    st.markdown(
        "### Enter Customer Details"
    )


    customer_input = st.text_input(
        "Customer ID",
        value=selected_id
    )


    input_rows = df[
        df["CustomerID"].astype(str)
        == customer_input.strip()
    ]


    if not input_rows.empty:

        input_customer = input_rows.iloc[0]

        input_age = int(
            input_customer["Age"]
        )

        input_income = float(
            input_customer["AnnualIncome"]
        )

        input_purchase = int(
            input_customer["PurchaseHistory"]
        )

        input_spending = float(
            input_customer["SpendingScore"]
        )

    else:

        input_age = 0
        input_income = 0.0
        input_purchase = 0
        input_spending = 0.0


    st.number_input(
        "Age",
        value=input_age,
        disabled=True
    )


    st.number_input(
        "Income (₹)",
        value=input_income,
        step=1000.0,
        disabled=True
    )


    st.number_input(
        "Purchase History (Number of Purchases)",
        value=input_purchase,
        disabled=True
    )


    st.number_input(
        "Spending Score (1 - 100)",
        value=input_spending,
        disabled=True
    )


    # --------------------------------------------------------
    # PREDICT BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔍 Predict Customer",
        use_container_width=True
    ):

        if input_rows.empty:

            st.error(
                "Customer ID not found."
            )

        else:

            st.session_state.selected_customer_id = (
                customer_input.strip()
            )

            st.session_state.page = "🏠 Home"

            st.rerun()


    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if st.button(
        "↻ Reset",
        use_container_width=True
    ):

        st.session_state.selected_customer_id = str(
            df["CustomerID"].iloc[0]
        )

        st.session_state.page = "🏠 Home"

        st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.markdown("### Navigation")


    if st.button(
        "🏠  Home",
        use_container_width=True
    ):

        st.session_state.page = "🏠 Home"

        st.rerun()


    if st.button(
        "📊  Dashboard",
        use_container_width=True
    ):

        st.session_state.page = "📊 Dashboard"

        st.rerun()


    if st.button(
        "👥  Customer Segments",
        use_container_width=True
    ):

        st.session_state.page = "👥 Customer Segments"

        st.rerun()


    if st.button(
        "👤  Customer Analysis",
        use_container_width=True
    ):

        st.session_state.page = "👤 Customer Analysis"

        st.rerun()


    if st.button(
        "💡  Marketing Suggestions",
        use_container_width=True
    ):

        st.session_state.page = "💡 Marketing Suggestions"

        st.rerun()


    st.markdown("---")


    if st.button(
        "ℹ️  About Project",
        use_container_width=True
    ):

        st.session_state.page = "ℹ️ About Project"

        st.rerun()


    if st.button(
        "👥  Team",
        use_container_width=True
    ):

        st.session_state.page = "👥 Team"

        st.rerun()


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html("""
    <div style="
        margin-bottom:8px;
    ">
        <div style="
            font-size:35px;
            font-weight:800;
            color:#172033;
        ">
            Customer Segmentation & Personalized
            Marketing Analytics
        </div>

        <div style="
            color:#64748b;
            font-size:16px;
            margin-top:6px;
        ">
            Analyze customer behavior and generate
            personalized marketing strategies.
        </div>
    </div>
    """)


    st.success(
        f"✅ Customer {customer['CustomerID']} loaded successfully!"
    )


    # --------------------------------------------------------
    # TOP CARDS
    # --------------------------------------------------------

    priority_map = {
        "Budget": "Low",
        "Regular": "Medium",
        "Premium": "High",
        "VIP": "Very High"
    }

    priority = priority_map.get(
        str(customer["Customer_Segment"]),
        "Medium"
    )


    col1, col2, col3 = st.columns(3)


    # ================= CARD 1 =================

    with col1:

        st.html(f"""
        <div style="
            background:#eef5ff;
            border:1px solid #cbdcff;
            border-radius:14px;
            padding:22px;
            min-height:170px;
        ">

            <div style="
                font-size:15px;
                font-weight:700;
                color:#475569;
            ">
                👤 Customer Segment
            </div>

            <div style="
                font-size:27px;
                font-weight:800;
                color:#2456d8;
                margin-top:8px;
            ">
                {customer["Customer_Segment"]}
            </div>

            <div style="
                color:#475569;
                margin-top:12px;
            ">
                Spending Score
            </div>

            <div style="
                font-size:20px;
                font-weight:700;
                color:#2456d8;
                margin-top:5px;
            ">
                {float(customer["SpendingScore"]):.0f} / 100
            </div>

            <div style="
                width:100%;
                height:8px;
                background:#dbe7ff;
                border-radius:20px;
                margin-top:10px;
            ">

                <div style="
                    width:{min(float(customer["SpendingScore"]), 100)}%;
                    height:8px;
                    background:#2456d8;
                    border-radius:20px;
                ">
                </div>

            </div>

        </div>
        """)


    # ================= CARD 2 =================

    with col2:

        st.html(f"""
        <div style="
            background:#eefbf4;
            border:1px solid #c9efd9;
            border-radius:14px;
            padding:22px;
            min-height:170px;
        ">

            <div style="
                font-size:15px;
                font-weight:700;
                color:#475569;
            ">
                👥 K-Means Cluster
            </div>

            <div style="
                font-size:27px;
                font-weight:800;
                color:#15945b;
                margin-top:8px;
            ">
                Cluster {customer["KMeans_Cluster"]}
            </div>

            <div style="
                color:#475569;
                margin-top:12px;
            ">
                Description
            </div>

            <div style="
                color:#178555;
                font-size:15px;
                line-height:1.5;
                margin-top:5px;
            ">
                Customer belongs to the
                {customer["Customer_Segment"]}
                segment based on purchasing behavior.
            </div>

        </div>
        """)


    # ================= CARD 3 =================

    with col3:

        suggestion_short = str(
            customer["Marketing_Suggestion"]
        )

        if len(suggestion_short) > 125:
            suggestion_short = (
                suggestion_short[:125] + "..."
            )


        st.html(f"""
        <div style="
            background:#fff8e8;
            border:1px solid #f2dfae;
            border-radius:14px;
            padding:22px;
            min-height:170px;
        ">

            <div style="
                font-size:15px;
                font-weight:700;
                color:#475569;
            ">
                ⭐ Marketing Priority
            </div>

            <div style="
                font-size:27px;
                font-weight:800;
                color:#d99416;
                margin-top:8px;
            ">
                {priority}
            </div>

            <div style="
                color:#475569;
                margin-top:12px;
            ">
                Recommended Strategy
            </div>

            <div style="
                color:#5f4b22;
                font-size:14px;
                line-height:1.5;
                margin-top:5px;
            ">
                {suggestion_short}
            </div>

        </div>
        """)


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # PROFILE + CHART
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 1.7]
    )


    # ================= PROFILE =================

    with col1:

        st.subheader(
            "👤 Customer Profile"
        )


        profile_df = pd.DataFrame({

            "Field": [
                "Customer ID",
                "Age",
                "Income",
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
            profile_df,
            use_container_width=True,
            hide_index=True
        )


    # ================= CHART =================

    with col2:

        st.subheader(
            "📊 Customer Visualization"
        )


        fig, ax = plt.subplots(
            figsize=(8, 5)
        )


        clusters = (
            df["KMeans_Cluster"]
            .dropna()
            .astype(str)
            .unique()
        )


        colors = [
            "#e74c3c",
            "#2563eb",
            "#16a34a",
            "#9333ea",
            "#f59e0b"
        ]


        for i, cluster in enumerate(clusters):

            cluster_df = df[
                df["KMeans_Cluster"]
                .astype(str)
                == cluster
            ]


            ax.scatter(
                cluster_df["AnnualIncome"],
                cluster_df["SpendingScore"],
                color=colors[
                    i % len(colors)
                ],
                alpha=0.65,
                s=40,
                label=f"Cluster {cluster}"
            )


        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="#111827",
            marker="*",
            s=300,
            edgecolors="white",
            linewidths=1.5,
            label=f"Customer ({customer['CustomerID']})"
        )


        ax.set_title(
            "Income vs Spending Score"
        )

        ax.set_xlabel(
            "Annual Income"
        )

        ax.set_ylabel(
            "Spending Score"
        )

        ax.grid(
            True,
            alpha=0.2
        )

        ax.legend(
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )


        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # MARKETING SECTION
    # --------------------------------------------------------

    st.subheader(
        "💡 Personalized Marketing Suggestions"
    )


    col1, col2, col3, col4 = st.columns(4)


    cards = [

        (
            "🎁",
            "Personalized Offers",
            "Send offers based on the customer's segment and spending behavior."
        ),

        (
            "🏷️",
            "Seasonal Discounts",
            "Use suitable discounts and seasonal deals to increase purchases."
        ),

        (
            "⭐",
            "Loyalty Rewards",
            "Reward repeat customers with points, benefits and exclusive offers."
        ),

        (
            "✉️",
            "Personalized Campaigns",
            "Use targeted messages and relevant product recommendations."
        )
    ]


    for column, card in zip(
        [col1, col2, col3, col4],
        cards
    ):

        icon, title, text = card

        with column:

            st.html(f"""
            <div style="
                background:white;
                border:1px solid #dfe6ef;
                border-radius:13px;
                padding:18px;
                min-height:145px;
                box-shadow:0 3px 10px rgba(15,23,42,0.06);
            ">

                <div style="
                    font-size:17px;
                    font-weight:800;
                    color:#2456d8;
                    margin-bottom:10px;
                ">
                    {icon} {title}
                </div>

                <div style="
                    color:#475569;
                    font-size:14px;
                    line-height:1.5;
                ">
                    {text}
                </div>

            </div>
            """)


    st.markdown("<br>", unsafe_allow_html=True)


    st.html("""
    <div style="
        text-align:center;
        color:#64748b;
        font-size:13px;
        padding:18px;
        border-top:1px solid #e2e8f0;
    ">
        © Customer Segmentation Platform |
        Built with Python, Pandas, Matplotlib & Streamlit
    </div>
    """)


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title(
        "📊 Customer Segmentation Dashboard"
    )

    st.write(
        "Overview of customer demographics, income, spending and segments."
    )

    st.divider()


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "👥 Total Customers",
            len(df)
        )

    with col2:
        st.metric(
            "💰 Average Income",
            f"₹{df['AnnualIncome'].mean():,.0f}"
        )

    with col3:
        st.metric(
            "🛍️ Average Spending",
            f"{df['SpendingScore'].mean():.2f}"
        )

    with col4:
        st.metric(
            "📌 Segments",
            df["Customer_Segment"].nunique()
        )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "👥 Customer Distribution"
        )

        counts = (
            df["Customer_Segment"]
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel(
            "Customer Segment"
        )

        ax.set_ylabel(
            "Number of Customers"
        )

        ax.tick_params(
            axis="x",
            rotation=0
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    with col2:

        st.subheader(
            "💰 Income vs Spending"
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.scatter(
            df["AnnualIncome"],
            df["SpendingScore"],
            alpha=0.65
        )

        ax.set_xlabel(
            "Annual Income"
        )

        ax.set_ylabel(
            "Spending Score"
        )

        ax.grid(
            True,
            alpha=0.20
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    st.divider()


    st.subheader(
        "📋 Segment Summary"
    )


    summary = (
        df.groupby("Customer_Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Average_Income=("AnnualIncome", "mean"),
            Average_Spending=("SpendingScore", "mean"),
            Average_Purchases=("PurchaseHistory", "mean")
        )
        .reset_index()
    )


    st.dataframe(
        summary.round(2),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

elif page == "👥 Customer Segments":

    st.title(
        "👥 Customer Segments"
    )

    st.write(
        "Customers are grouped according to their customer segment."
    )

    st.divider()


    col1, col2, col3, col4 = st.columns(4)


    segment_info = [
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]


    for column, item in zip(
        [col1, col2, col3, col4],
        segment_info
    ):

        title, segment = item

        with column:

            st.metric(
                title,
                len(
                    df[
                        df["Customer_Segment"] == segment
                    ]
                )
            )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "💰 Budget Customers"
        )

        budget = df[
            df["Customer_Segment"] == "Budget"
        ]

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


    with col2:

        st.subheader(
            "🛍️ Regular Customers"
        )

        regular = df[
            df["Customer_Segment"] == "Regular"
        ]

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


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "💎 Premium Customers"
        )

        premium = df[
            df["Customer_Segment"] == "Premium"
        ]

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


    with col2:

        st.subheader(
            "👑 VIP Customers"
        )

        vip = df[
            df["Customer_Segment"] == "VIP"
        ]

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


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "👤 Customer Analysis":

    st.title(
        "👤 Customer Analysis"
    )

    st.success(
        f"✅ Customer {customer['CustomerID']} loaded successfully!"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "👤 Customer Profile"
        )

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
                int(customer["Age"]),
                f"₹{float(customer['AnnualIncome']):,.2f}",
                int(customer["PurchaseHistory"]),
                float(customer["SpendingScore"]),
                customer["Customer_Segment"],
                customer["KMeans_Cluster"]
            ]

        })


        st.dataframe(
            profile,
            use_container_width=True,
            hide_index=True
        )


    with col2:

        st.subheader(
            "💡 Marketing Suggestion"
        )

        st.info(
            customer["Marketing_Suggestion"]
        )


        st.subheader(
            "📊 Classification"
        )

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


# ============================================================
# MARKETING SUGGESTIONS
# ============================================================

elif page == "💡 Marketing Suggestions":

    st.title(
        "💡 Marketing Suggestions"
    )

    st.write(
        "Recommended strategies for each customer segment."
    )

    st.divider()


    strategies = [
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]


    col1, col2 = st.columns(2)


    for index, item in enumerate(
        strategies
    ):

        title, segment = item

        segment_data = df[
            df["Customer_Segment"] == segment
        ]


        if segment_data.empty:
            continue


        suggestion = str(
            segment_data[
                "Marketing_Suggestion"
            ].dropna().iloc[0]
        )


        target_column = (
            col1 if index % 2 == 0
            else col2
        )


        with target_column:

            st.subheader(title)

            st.metric(
                "Customers",
                len(segment_data)
            )

            st.info(
                suggestion
            )

            st.markdown("---")


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "ℹ️ About Project":

    st.title(
        "ℹ️ About Project"
    )

    st.subheader(
        "Customer Segmentation & Personalized Marketing Analytics"
    )

    st.write(
        """
        This project analyzes customer information and divides customers
        into different segments based on their purchasing behavior.
        The platform helps identify customer characteristics and supports
        personalized marketing strategies.
        """
    )

    st.divider()

    st.subheader(
        "🎯 Project Objectives"
    )

    st.write(
        """
        • Analyze customer purchasing behavior

        • Divide customers into meaningful segments

        • Understand income and spending patterns

        • Identify high-value customer groups

        • Provide personalized marketing suggestions
        """
    )

    st.subheader(
        "🛠️ Technologies"
    )

    st.write(
        """
        Python  
        Pandas  
        Matplotlib  
        Streamlit  
        K-Means Customer Segmentation
        """
    )


# ============================================================
# TEAM
# ============================================================

elif page == "👥 Team":

    st.title(
        "👥 Team"
    )

    st.subheader(
        "Customer Segmentation Project"
    )

    st.write(
        "Academic Data Analytics Project"
    )

    st.divider()

    st.info(
        "Add your team member names, college name and guide details here."
    )
