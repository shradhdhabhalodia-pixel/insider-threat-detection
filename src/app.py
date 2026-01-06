import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd  # pyright: ignore[reportMissingModuleSource]
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Insider Threat Detection Dashboard",
    layout="wide"
)

st.title("🔐 Insider Threat Detection Dashboard")

st.markdown(
    """
This dashboard analyzes **employee behavioral risk** using:
- Login patterns
- File activity
- Web activity
- Psychometric traits

The system is **unsupervised & explainable**, aligned with real SOC practices.
"""
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    # Go up one level from src/ to insider-threat-detection/
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data" / "processed" / "final_insider_risk.csv"

    # Optional: check file exists
    if not data_path.exists():
        st.error(f"File not found: {data_path}")
        st.stop()

    df = pd.read_csv(data_path)
    return df


df = load_data()

# Debug: show basic info
st.info("🚀 Streamlit app is running")
st.write("Data Shape:", df.shape)
st.write("Columns:", df.columns.tolist())
st.write(df.head())

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Guard against missing risk_label or empty dataframe
if 'risk_label' in df.columns:
    risk_labels = df['risk_label'].dropna().unique().tolist()
    risk_filter = st.sidebar.multiselect(
        "Select Risk Level",
        options=risk_labels,
        default=risk_labels
    )
    filtered_df = df[df['risk_label'].isin(risk_filter)]
else:
    st.warning("⚠️ 'risk_label' column not found in data")
    st.stop()

# Handle empty filtered dataframe
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Users", len(filtered_df))
col2.metric("High Risk Users", (filtered_df['risk_label'] == "High Insider Threat").sum())
col3.metric("Medium Risk Users", (filtered_df['risk_label'] == "Medium Risk").sum())

st.divider()

# -----------------------------
# Risk Distribution
# -----------------------------
st.subheader("📊 Risk Score Distribution")

fig, ax = plt.subplots()
ax.hist(filtered_df['final_risk'], bins=30)
ax.set_xlabel("Final Risk Score")
ax.set_ylabel("User Count")
st.pyplot(fig)

# -----------------------------
# Risk Label Breakdown
# -----------------------------
st.subheader("📈 Risk Category Breakdown")
risk_counts = filtered_df['risk_label'].value_counts()
st.bar_chart(risk_counts)

# -----------------------------
# User-Level Drill Down
# -----------------------------
st.subheader("👤 User Risk Analysis")

if 'user' in filtered_df.columns:
    selected_user = st.selectbox(
        "Select a User",
        filtered_df['user'].unique()
    )
    user_data = filtered_df[filtered_df['user'] == selected_user]

    st.write("### Risk Summary")
    st.dataframe(
        user_data[['final_risk', 'risk_label']],
        use_container_width=True
    )
else:
    st.warning("⚠️ 'user' column not found")
    st.stop()

# -----------------------------
# Risk Explanation
# -----------------------------
st.write("### 🔍 Risk Contribution Breakdown")

features = [
    'logon_risk',
    'file_risk',
    'web_risk',
    'psycho_risk',
    'logon_anomaly',
    'file_anomaly',
    'web_anomaly'
]

# Ensure features exist and are numeric
contrib_features = [f for f in features if f in user_data.columns]
contrib_df = user_data[contrib_features].apply(pd.to_numeric, errors='coerce').fillna(0)

if not contrib_df.empty:
    fig2, ax2 = plt.subplots()
    contrib_df.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_ylabel("Risk Contribution")
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig2)
else:
    st.info("No contribution data available for this user.")

# -----------------------------
# Data Download
# -----------------------------
st.subheader("⬇️ Download Results")

st.download_button(
    label="Download Final Insider Risk CSV",
    data=filtered_df.to_csv(index=False),
    file_name="final_insider_risk.csv",
    mime="text/csv"
)
