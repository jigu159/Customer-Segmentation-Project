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
    if os.path.exists("data/customer_segmentation_exact.csv"):
        path = "data/customer_segmentation_exact.csv"
    else:
        path = "customer_segmentation_exact.csv"
    return pd.read_csv(path)

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

# Make CustomerID consistently text
df["CustomerID"] = df["CustomerID"].astype(str)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = df["CustomerID"].iloc[0]

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stAppViewContainer"] {
        background: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background: #f7f9fc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 1.5rem;
    }

    [data-testid="stSidebar"] {
        background: #16243b;
    }

    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] input {
        background: #ffffff !important;
        color: #172033 !important;
        border-radius: 7px !important;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    h1, h2, h3 {
        color: #172033 !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #dfe6ef;
        border-radius: 12px;
        overflow: hidden;
    }

    .success-banner {
        background: #edf9f1;
        border: 1px solid #c9efd9;
        color: #177245;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .profile-row {
        display: flex;
        justify-content: space-between;
        padding: 11px 12px;
        border-bottom: 1px solid #edf0f5;
        font-size: 14px;
    }

    .profile-row:last-child {
        border-bottom: none;
    }

    .profile-key {
        color: #475569;
        font-weight: 600;
    }

    .profile-value {
        color: #172033;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SELECTED CUSTOMER
# ============================================================

selected_id = str(st.session_state.selected_customer_id)

selected_rows = df[df["CustomerID"] == selected_id]

if selected_rows.empty:
    selected_id = df["CustomerID"].iloc[0]
    selected_rows = df[df["CustomerID"] == selected_id]
    st.session_state.selected_customer_id = selected_id

customer = selected_rows.iloc[0]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div style="
        text-align:center;
        padding:8px 4px 20px 4px;
        border-bottom:1px solid rgba(255,255,255,0.25);
        margin-bottom:20px;
    ">
        <div style="font-size:36px;">👥</div>
        <div style="
            color:white;
            font-size:21px;
            font-weight:800;
            line-height:1.15;
        ">
            Customer Segmentation<br>Platform
        </div>
        <div style="
            color:#cbd5e1;
            font-size:12px;
            margin-top:7px;
        ">
            Personalized Marketing Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    customer_input = st.text_input(
        "Customer ID",
        value=str(selected_id)
    )

    input_rows = df[
        df["CustomerID"] == customer_input.strip()
    ]

    if not input_rows.empty:
        input_customer = input_rows.iloc[0]
        input_age = int(input_customer["Age"])
        input_income = float(input_customer["AnnualIncome"])
        input_purchase = int(input_customer["PurchaseHistory"])
        input_spending = float(input_customer["SpendingScore"])
    else:
        input_age = 0
        input_income = 0.0
        input_purchase = 0
        input_spending = 0.0

    st.number_input("Age", value=input_age, disabled=True)
    st.number_input("Income (₹)", value=input_income, step=1000.0, disabled=True)
    st.number_input("Purchase History (Number of Purchases)", value=input_purchase, disabled=True)
    st.number_input("Spending Score (1 - 100)", value=input_spending, disabled=True)

    if st.button("🔍 Predict Customer", use_container_width=True):
        new_id = customer_input.strip()

        if new_id in set(df["CustomerID"]):
            st.session_state.selected_customer_id = new_id
            st.session_state.page = "🏠 Home"
            st.rerun()
        else:
            st.error("Customer ID not found.")

    if st.button("↻ Reset", use_container_width=True):
        st.session_state.selected_customer_id = df["CustomerID"].iloc[0]
        st.session_state.page = "🏠 Home"
        st.rerun()

    st.markdown("---")
    st.markdown("### Navigation")

    if st.button("🏠  Home", use_container_width=True):
        st.session_state.page = "🏠 Home"
        st.rerun()

    if st.button("📊  Dashboard", use_container_width=True):
        st.session_state.page = "📊 Dashboard"
        st.rerun()

    if st.button("👥  Customer Segments", use_container_width=True):
        st.session_state.page = "👥 Customer Segments"
        st.rerun()

    if st.button("👤  Customer Analysis", use_container_width=True):
        st.session_state.page = "👤 Customer Analysis"
        st.rerun()

    if st.button("💡  Marketing Suggestions", use_container_width=True):
        st.session_state.page = "💡 Marketing Suggestions"
        st.rerun()

    st.markdown("---")

    if st.button("ℹ️  About Project", use_container_width=True):
        st.session_state.page = "ℹ️ About Project"
        st.rerun()

    if st.button("👥  Team", use_container_width=True):
        st.session_state.page = "👥 Team"
        st.rerun()

page = st.session_state.page

# ============================================================
# HELPER
# ============================================================

priority_map = {
    "Budget": "Low",
    "Regular": "Medium",
    "Premium": "High",
    "VIP": "Very High"
}

# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown("""
    <div style="
        font-size:35px;
        font-weight:800;
        color:#172033;
        line-height:1.15;
    ">
        Customer Segmentation & Personalized
        Marketing Analytics
    </div>

    <div style="
        color:#64748b;
        font-size:16px;
        margin-top:7px;
        margin-bottom:18px;
    ">
        Analyze customer behavior, understand segments and create
        targeted marketing strategies.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="success-banner">✅ Customer {customer["CustomerID"]} loaded successfully!</div>',
        unsafe_allow_html=True
    )

    priority = priority_map.get(
        str(customer["Customer_Segment"]),
        "Medium"
    )

    # ---------------- TOP CARDS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        score = float(customer["SpendingScore"])
        st.markdown(f"""
        <div style="
            background:#eef5ff;
            border:1px solid #cbdcff;
            border-radius:14px;
            padding:20px;
            min-height:160px;
        ">
            <div style="font-size:15px;font-weight:700;color:#475569;">
                👤 Customer Segment
            </div>
            <div style="font-size:27px;font-weight:800;color:#2456d8;margin-top:7px;">
                {customer["Customer_Segment"]}
            </div>
            <div style="color:#475569;margin-top:14px;">
                Spending Score
            </div>
            <div style="font-size:20px;font-weight:800;color:#2456d8;margin-top:4px;">
                {score:.0f} / 100
            </div>
            <div style="
                width:100%;height:8px;background:#dbe7ff;
                border-radius:20px;margin-top:9px;
            ">
                <div style="
                    width:{min(max(score,0),100)}%;height:8px;
                    background:#2456d8;border-radius:20px;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background:#eefbf4;
            border:1px solid #c9efd9;
            border-radius:14px;
            padding:20px;
            min-height:160px;
        ">
            <div style="font-size:15px;font-weight:700;color:#475569;">
                👥 K-Means Cluster
            </div>
            <div style="font-size:27px;font-weight:800;color:#15945b;margin-top:7px;">
                Cluster {customer["KMeans_Cluster"]}
            </div>
            <div style="color:#475569;margin-top:14px;">
                Description
            </div>
            <div style="color:#178555;font-size:15px;line-height:1.5;margin-top:5px;">
                Customer belongs to the {customer["Customer_Segment"]}
                segment based on purchasing behavior.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        strategy = str(customer["Marketing_Suggestion"])
        if len(strategy) > 120:
            strategy = strategy[:120] + "..."

        st.markdown(f"""
        <div style="
            background:#fff8e8;
            border:1px solid #f2dfae;
            border-radius:14px;
            padding:20px;
            min-height:160px;
        ">
            <div style="font-size:15px;font-weight:700;color:#475569;">
                ⭐ Marketing Priority
            </div>
            <div style="font-size:27px;font-weight:800;color:#d99416;margin-top:7px;">
                {priority}
            </div>
            <div style="color:#475569;margin-top:14px;">
                Recommended Strategy
            </div>
            <div style="color:#5f4b22;font-size:14px;line-height:1.5;margin-top:5px;">
                {strategy}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- PROFILE + VISUALIZATION ----------------

    left, right = st.columns([1, 1.7])

    with left:

        st.subheader("👤 Customer Profile")

        profile_rows = [
            ("Customer ID", customer["CustomerID"]),
            ("Age", f'{int(customer["Age"])} Years'),
            ("Income", f'₹{float(customer["AnnualIncome"]):,.0f}'),
            ("Purchase History", f'{int(customer["PurchaseHistory"])} Purchases'),
            ("Spending Score", f'{float(customer["SpendingScore"]):.0f} / 100'),
            ("Segment", customer["Customer_Segment"]),
            ("Cluster", customer["KMeans_Cluster"])
        ]

        profile_html = '<div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:8px 14px;">'

        for key, value in profile_rows:
            profile_html += f"""
            <div class="profile-row">
                <span class="profile-key">{key}</span>
                <span class="profile-value">{value}</span>
            </div>
            """

        profile_html += "</div>"

        st.markdown(profile_html, unsafe_allow_html=True)

    with right:

        st.subheader("📊 Cluster Visualization")

        fig, ax = plt.subplots(figsize=(8, 5))

        clusters = sorted(
            df["KMeans_Cluster"].dropna().unique(),
            key=lambda x: str(x)
        )

        plot_colors = [
            "#dc2626",
            "#2563eb",
            "#16a34a",
            "#9333ea",
            "#f59e0b",
            "#0891b2"
        ]

        for i, cluster_value in enumerate(clusters):

            cluster_data = df[
                df["KMeans_Cluster"] == cluster_value
            ]

            ax.scatter(
                cluster_data["AnnualIncome"],
                cluster_data["SpendingScore"],
                color=plot_colors[i % len(plot_colors)],
                alpha=0.65,
                s=38,
                label=f"Cluster {cluster_value}"
            )

        ax.scatter(
            float(customer["AnnualIncome"]),
            float(customer["SpendingScore"]),
            color="#111827",
            marker="*",
            s=300,
            edgecolors="white",
            linewidths=1.5,
            label=f"Customer ({customer['CustomerID']})"
        )

        ax.set_title("Income vs Spending Score")
        ax.set_xlabel("Annual Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=0.18)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- MARKETING CARDS ----------------

    st.subheader("💡 Personalized Marketing Suggestions")

    marketing_cards = [
        ("🎁", "Premium Membership", "Offer premium membership or exclusive benefits to valuable customers."),
        ("🏷️", "Festival Discount", "Provide suitable seasonal discounts and promotional deals."),
        ("⭐", "Loyalty Rewards", "Give loyalty points and rewards to encourage repeat purchases."),
        ("✉️", "Personalized Offers", "Send targeted messages with products relevant to customer behavior."),
        ("⏰", "Early Access", "Provide early access to selected products, offers or sales.")
    ]

    card_cols = st.columns(5)

    card_backgrounds = [
        "#eef5ff",
        "#edf9f1",
        "#fff8e8",
        "#f5efff",
        "#fff0f0"
    ]

    card_foregrounds = [
        "#2456d8",
        "#15945b",
        "#d99416",
        "#7c3aed",
        "#dc2626"
    ]

    for i, (icon, title, text) in enumerate(marketing_cards):

        with card_cols[i]:

            st.markdown(f"""
            <div style="
                background:{card_backgrounds[i]};
                border:1px solid #dfe6ef;
                border-radius:13px;
                padding:16px;
                min-height:155px;
                box-shadow:0 3px 10px rgba(15,23,42,0.05);
            ">
                <div style="
                    color:{card_foregrounds[i]};
                    font-size:16px;
                    font-weight:800;
                    margin-bottom:10px;
                ">
                    {icon} {title}
                </div>
                <div style="
                    color:#475569;
                    font-size:13px;
                    line-height:1.5;
                ">
                    {text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;color:#64748b;font-size:12px;padding:15px;border-top:1px solid #e2e8f0;">© Customer Segmentation Platform | Built with Python, Pandas, Matplotlib & Streamlit</div>',
        unsafe_allow_html=True
    )

# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title("📊 Customer Segmentation Dashboard")
    st.write("Overall analysis of customer demographics, income and spending behavior.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Customers", f"{len(df):,}")
    col2.metric("💰 Average Income", f"₹{df['AnnualIncome'].mean():,.0f}")
    col3.metric("🛍️ Average Spending", f"{df['SpendingScore'].mean():.2f}")
    col4.metric("📌 Segments", df["Customer_Segment"].nunique())

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👥 Customer Distribution")

        counts = df["Customer_Segment"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 5))
        counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Number of Customers")
        ax.tick_params(axis="x", rotation=0)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    with col2:

        st.subheader("💰 Income vs Spending")

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(
            df["AnnualIncome"],
            df["SpendingScore"],
            alpha=0.65
        )
        ax.set_xlabel("Annual Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=0.18)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    st.subheader("📋 Segment Summary")

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

    st.title("👥 Customer Segments")

    st.write(
        "Customers are grouped into Budget, Regular, Premium and VIP segments."
    )

    st.divider()

    segment_info = [
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]

    cols = st.columns(4)

    for col, (title, segment) in zip(cols, segment_info):

        with col:

            count = len(
                df[
                    df["Customer_Segment"] == segment
                ]
            )

            st.metric(
                title,
                count
            )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💰 Budget Customers")

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

        st.subheader("🛍️ Regular Customers")

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

        st.subheader("💎 Premium Customers")

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

        st.subheader("👑 VIP Customers")

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

    st.title("👤 Customer Analysis")

    st.write(
        "Complete information for the selected customer."
    )

    st.divider()

    st.success(
        f"Customer {customer['CustomerID']} loaded successfully!"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📋 Customer Details")

        st.write("**Customer ID:**", customer["CustomerID"])
        st.write("**Age:**", int(customer["Age"]))
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

    with col2:

        st.subheader("📊 Customer Position")

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.scatter(
            df["AnnualIncome"],
            df["SpendingScore"],
            alpha=0.55
        )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="#111827",
            marker="*",
            s=300,
            edgecolors="white",
            linewidths=1.4
        )

        ax.set_xlabel("Annual Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=0.18)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

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
        ("💰 Budget", "Budget"),
        ("🛍️ Regular", "Regular"),
        ("💎 Premium", "Premium"),
        ("👑 VIP", "VIP")
    ]

    col1, col2 = st.columns(2)

    for index, (title, segment) in enumerate(segments):

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

        target_col = (
            col1 if index % 2 == 0
            else col2
        )

        with target_col:

            st.subheader(title)

            st.metric(
                "Customers",
                len(segment_data)
            )

            st.info(suggestion)

            st.markdown("---")

# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "ℹ️ About Project":

    st.title("ℹ️ About Project")

    st.subheader(
        "Customer Segmentation & Personalized Marketing Analytics"
    )

    st.write(
        """
        This project analyzes customer information and groups customers
        into meaningful segments based on their purchasing behavior.
        The platform helps understand customer characteristics and
        supports personalized marketing strategies.
        """
    )

    st.divider()

    st.subheader("🎯 Project Objectives")

    st.write(
        """
        • Analyze customer purchasing behavior

        • Identify customer segments

        • Understand income and spending patterns

        • Identify valuable customer groups

        • Provide personalized marketing suggestions
        """
    )

    st.subheader("🛠️ Technologies Used")

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

    st.title("👥 Team")

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
