import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
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

    file_path = (
        "data/customer_segmentation_exact.csv"
        if os.path.exists("data/customer_segmentation_exact.csv")
        else "customer_segmentation_exact.csv"
    )

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
# GLOBAL DESIGN
# ============================================================

st.html("""
<style>

    /* -------------------------------------------------------
       MAIN APPLICATION
       ------------------------------------------------------- */

    [data-testid="stAppViewContainer"] {
        background-color: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1500px;
    }


    /* -------------------------------------------------------
       SIDEBAR
       ------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: #16243b;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] p {
        color: white;
    }

    [data-testid="stSidebar"] input {
        background: white !important;
        color: #111827 !important;
        border-radius: 7px !important;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        font-weight: 600 !important;
    }


    /* -------------------------------------------------------
       HEADINGS
       ------------------------------------------------------- */

    h1 {
        color: #172033 !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #24344d !important;
        font-weight: 700 !important;
    }


    /* -------------------------------------------------------
       TOP CARDS
       ------------------------------------------------------- */

    .top-card {

        background: white;

        border-radius: 14px;

        border: 1px solid #e2e8f0;

        padding: 22px;

        min-height: 155px;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.08);

    }

    .top-card-blue {

        background: #eef5ff;

        border: 1px solid #cbdcff;

    }

    .top-card-green {

        background: #eefbf4;

        border: 1px solid #c9efd9;

    }

    .top-card-yellow {

        background: #fff8e8;

        border: 1px solid #f2dfae;

    }

    .card-small-title {

        font-size: 15px;

        font-weight: 700;

        color: #475569;

        margin-bottom: 10px;

    }

    .card-value {

        font-size: 27px;

        font-weight: 800;

        margin-bottom: 10px;

    }

    .blue-value {
        color: #2456d8;
    }

    .green-value {
        color: #15945b;
    }

    .yellow-value {
        color: #d99416;
    }


    /* -------------------------------------------------------
       PROFILE CARD
       ------------------------------------------------------- */

    .profile-box {

        background: white;

        border: 1px solid #e2e8f0;

        border-radius: 14px;

        padding: 18px;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.06);

    }


    /* -------------------------------------------------------
       MARKETING CARDS
       ------------------------------------------------------- */

    .marketing-card {

        background: white;

        border: 1px solid #e2e8f0;

        border-radius: 13px;

        padding: 18px;

        min-height: 150px;

        box-shadow:
            0 3px 10px rgba(15, 23, 42, 0.06);

    }

    .marketing-title {

        font-size: 17px;

        font-weight: 800;

        margin-bottom: 10px;

    }

    .marketing-text {

        font-size: 14px;

        color: #475569;

        line-height: 1.5;

    }


    /* -------------------------------------------------------
       INFO BOXES
       ------------------------------------------------------- */

    [data-testid="stAlert"] {

        border-radius: 10px;

    }


    /* -------------------------------------------------------
       TABLE
       ------------------------------------------------------- */

    [data-testid="stDataFrame"] {

        border-radius: 12px;

        overflow: hidden;

        border: 1px solid #e2e8f0;

    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SELECTED CUSTOMER
# ============================================================

selected_id = str(
    st.session_state.selected_customer_id
)

selected_data = df[
    df["CustomerID"].astype(str) == selected_id
]

if selected_data.empty:

    selected_id = str(
        df["CustomerID"].iloc[0]
    )

    selected_data = df[
        df["CustomerID"].astype(str) == selected_id
    ]

customer = selected_data.iloc[0]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.html(
    """
    <div style="
        text-align:center;
        padding:5px 5px 20px 5px;
        border-bottom:1px solid rgba(255,255,255,0.25);
        margin-bottom:20px;
    ">

        <div style="
            font-size:34px;
            margin-bottom:5px;
        ">
            👥
        </div>

        <div style="
            color:white;
            font-size:20px;
            font-weight:800;
            line-height:1.2;
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
    """,
    unsafe_allow_html=True
)


# ============================================================
# CUSTOMER DETAILS
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        color:white;
        font-size:16px;
        font-weight:800;
        margin-bottom:10px;
    ">
        Enter Customer Details
    </div>
    """,
    unsafe_allow_html=True
)


customer_ids = sorted(
    df["CustomerID"]
    .dropna()
    .astype(str)
    .tolist()
)


customer_input = st.sidebar.text_input(
    "Customer ID",
    value=selected_id
)


input_customer = df[
    df["CustomerID"].astype(str)
    == customer_input.strip()
]


if not input_customer.empty:

    input_row = input_customer.iloc[0]

    sidebar_age = int(input_row["Age"])

    sidebar_income = float(
        input_row["AnnualIncome"]
    )

    sidebar_purchase = int(
        input_row["PurchaseHistory"]
    )

    sidebar_spending = float(
        input_row["SpendingScore"]
    )

else:

    sidebar_age = 0

    sidebar_income = 0.0

    sidebar_purchase = 0

    sidebar_spending = 0.0


st.sidebar.number_input(
    "Age",
    value=sidebar_age,
    disabled=True
)


st.sidebar.number_input(
    "Income (₹)",
    value=sidebar_income,
    step=1000.0,
    disabled=True
)


st.sidebar.number_input(
    "Purchase History\n(Number of Purchases)",
    value=sidebar_purchase,
    disabled=True
)


st.sidebar.number_input(
    "Spending Score (1 - 100)",
    value=sidebar_spending,
    disabled=True
)


# ============================================================
# PREDICT BUTTON
# ============================================================

if st.sidebar.button(
    "🔍 Predict Customer",
    use_container_width=True
):

    if input_customer.empty:

        st.sidebar.error(
            "Customer ID not found."
        )

    else:

        st.session_state.selected_customer_id = (
            customer_input.strip()
        )

        st.session_state.page = "🏠 Home"

        st.rerun()


# ============================================================
# RESET BUTTON
# ============================================================

if st.sidebar.button(
    "↻ Reset",
    use_container_width=True
):

    st.session_state.selected_customer_id = str(
        df["CustomerID"].iloc[0]
    )

    st.session_state.page = "🏠 Home"

    st.rerun()


st.sidebar.markdown("---")


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "### Navigation"
)


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


st.sidebar.markdown("---")


if st.sidebar.button(
    "ℹ️  About Project",
    use_container_width=True
):

    st.session_state.page = "ℹ️ About Project"

    st.rerun()


if st.sidebar.button(
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

    st.markdown(
        """
        <div style="
            font-size:34px;
            font-weight:800;
            color:#172033;
            margin-bottom:8px;
        ">
            Customer Segmentation & Personalized
            Marketing Analytics
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            font-size:16px;
            color:#64748b;
            margin-bottom:20px;
        ">
            Analyze customer behavior and generate
            personalized marketing strategies.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.success(
        f"Customer {customer['CustomerID']} loaded successfully!"
    )


    # --------------------------------------------------------
    # MARKETING PRIORITY
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


    # --------------------------------------------------------
    # TOP THREE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="top-card top-card-blue">

                <div class="card-small-title">
                    👤 Customer Segment
                </div>

                <div class="card-value blue-value">
                    {customer["Customer_Segment"]}
                </div>

                <div style="
                    color:#475569;
                    margin-bottom:8px;
                ">
                    Spending Score
                </div>

                <div style="
                    font-size:20px;
                    font-weight:700;
                    color:#2456d8;
                ">
                    {float(customer["SpendingScore"]):.0f} / 100
                </div>

                <div style="
                    height:8px;
                    background:#dbe7ff;
                    border-radius:10px;
                    margin-top:10px;
                ">

                    <div style="
                        height:8px;
                        width:{min(float(customer["SpendingScore"]),100)}%;
                        background:#2456d8;
                        border-radius:10px;
                    "></div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="top-card top-card-green">

                <div class="card-small-title">
                    👥 K-Means Cluster
                </div>

                <div class="card-value green-value">
                    Cluster {customer["KMeans_Cluster"]}
                </div>

                <div style="
                    color:#475569;
                    margin-bottom:6px;
                ">
                    Description
                </div>

                <div style="
                    color:#178555;
                    font-size:15px;
                    line-height:1.5;
                ">
                    {customer["Customer_Segment"]}
                    customer based on
                    purchasing behavior.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="top-card top-card-yellow">

                <div class="card-small-title">
                    ⭐ Marketing Priority
                </div>

                <div class="card-value yellow-value">
                    {priority}
                </div>

                <div style="
                    color:#475569;
                    margin-bottom:6px;
                ">
                    Recommended Strategy
                </div>

                <div style="
                    color:#5f4b22;
                    font-size:14px;
                    line-height:1.5;
                ">
                    {customer["Marketing_Suggestion"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # PROFILE + VISUALIZATION
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 1.65]
    )


    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------------

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


        chart_colors = [
            "#ef4444",
            "#2563eb",
            "#16a34a",
            "#9333ea",
            "#f59e0b"
        ]


        for index, cluster in enumerate(
            clusters
        ):

            cluster_data = df[
                df["KMeans_Cluster"]
                .astype(str)
                == cluster
            ]


            ax.scatter(
                cluster_data["AnnualIncome"],
                cluster_data["SpendingScore"],
                label=f"Cluster {cluster}",
                color=chart_colors[
                    index % len(chart_colors)
                ],
                alpha=0.65,
                s=40
            )


        # Selected customer

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            s=280,
            color="#111827",
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
            alpha=0.20
        )

        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1.02, 1)
        )


        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # MARKETING SUGGESTIONS
    # --------------------------------------------------------

    st.subheader(
        "💡 Personalized Marketing Suggestions"
    )


    col1, col2, col3, col4 = st.columns(4)


    strategy_data = [

        (
            "🎁",
            "Personalized Offers",
            "Use the customer's segment and spending behavior "
            "to send targeted offers."
        ),

        (
            "🏷️",
            "Seasonal Discounts",
            "Provide suitable discounts and seasonal deals "
            "based on the customer segment."
        ),

        (
            "⭐",
            "Loyalty Rewards",
            "Encourage repeat purchases using loyalty points "
            "and rewards."
        ),

        (
            "✉️",
            "Personalized Campaigns",
            "Send relevant products and promotions through "
            "personalized marketing campaigns."
        )
    ]


    for column, item in zip(
        [col1, col2, col3, col4],
        strategy_data
    ):

        icon, title, text = item

        with column:

            st.markdown(
                f"""
                <div class="marketing-card">

                    <div class="marketing-title">
                        {icon} {title}
                    </div>

                    <div class="marketing-text">
                        {text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
        <div style="
            text-align:center;
            color:#64748b;
            font-size:13px;
            padding:15px;
        ">
            © Customer Segmentation Platform |
            Built with Python, Pandas, Matplotlib & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title(
        "📊 Customer Segmentation Dashboard"
    )

    st.write(
        "Overall analysis of customer data."
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
            "Customers"
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
        "Customers grouped according to their customer segment."
    )

    st.divider()


    segments = [
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]


    col1, col2, col3, col4 = st.columns(4)


    for column, item in zip(
        [col1, col2, col3, col4],
        segments
    ):

        icon_name, segment_name = item

        segment_data = df[
            df["Customer_Segment"] == segment_name
        ]


        with column:

            st.metric(
                icon_name,
                len(segment_data)
            )


    st.divider()


    # Budget + Regular

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


    # Premium + VIP

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

    st.write(
        "Complete information for the selected customer."
    )

    st.divider()


    st.success(
        f"Customer loaded: {customer['CustomerID']}"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "📋 Customer Details"
        )

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
            f"₹{float(customer['AnnualIncome']):,.2f}"
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

        st.subheader(
            "📊 Customer Classification"
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

        st.divider()

        st.subheader(
            "💡 Marketing Suggestion"
        )

        st.info(
            customer["Marketing_Suggestion"]
        )


# ============================================================
# MARKETING SUGGESTIONS
# ============================================================

elif page == "💡 Marketing Suggestions":

    st.title(
        "💡 Marketing Suggestions"
    )

    st.write(
        "Segment-wise marketing strategies."
    )

    st.divider()


    strategies = [
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]


    col1, col2 = st.columns(2)


    for index, item in enumerate(strategies):

        icon_name, segment_name = item

        segment_data = df[
            df["Customer_Segment"] == segment_name
        ]


        if segment_data.empty:
            continue


        suggestion = (
            segment_data["Marketing_Suggestion"]
            .dropna()
            .iloc[0]
        )


        target_col = col1 if index % 2 == 0 else col2


        with target_col:

            st.subheader(
                f"{icon_name} Customers"
            )

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
        into meaningful segments based on purchasing behavior.
        The system helps understand customer characteristics and provides
        personalized marketing suggestions.
        """
    )

    st.divider()


    st.subheader(
        "🎯 Objectives"
    )

    st.write(
        """
        • Analyze customer purchasing behavior

        • Identify customer segments

        • Understand income and spending patterns

        • Support personalized marketing decisions

        • Present customer insights through an interactive dashboard
        """
    )


    st.subheader(
        "🛠️ Technologies Used"
    )

    st.write(
        """
        Python  
        Pandas  
        Matplotlib  
        Streamlit  
        Machine Learning / K-Means Segmentation
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
        "Project developed as an academic data analytics project."
    )

    st.divider()


    st.info(
        "Add your team member names, college name and guide details here."
    )
