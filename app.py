import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


def format_days(day_str):
    if "d+" in day_str:
        return int(day_str.replace("d+", "")) + 1
    elif "h" in day_str:
        return 0
    else:
        return int(day_str.replace("d", ""))


@st.cache_data
def load_data():
    data = pd.read_csv("data/data_science_jobs.csv")
    data["Days_Past"] = data["Date"].apply(format_days)
    current_date = datetime.now()
    current_date = pd.Timestamp(current_date)
    data["Date"] = data["Days_Past"].apply(
        lambda days: current_date - timedelta(days=days)
    )
    data["Date"] = pd.to_datetime(data["Date"])
    data.drop(columns=["Days_Past"], inplace=True)

    return data


# Load your data
df = load_data()
st.title("Job Market Dashboard")
st.write(df.head())

# Add "None" option for each select box
locations = ["None"] + list(df["Location"].unique())
selected_location = st.sidebar.selectbox(
    "Select Location", locations, index=locations.index("Austin, TX")
)

job_titles = ["None"] + list(df["Job Title"].unique())
selected_job = st.sidebar.selectbox("Select Job Title", job_titles)

companies = ["None"] + list(df["Company Name"].unique())
selected_company = st.sidebar.selectbox("Select Company", companies)

date_range = st.sidebar.date_input(
    "Select Date Range", [df["Date"].min(), df["Date"].max()]
)

# Filter DataFrame based on selected values
filtered_df = df[
    (df["Location"] == selected_location if selected_location != "None" else True)
    & (df["Job Title"] == selected_job if selected_job != "None" else True)
    & (df["Company Name"] == selected_company if selected_company != "None" else True)
    & (df["Date"].between(*(pd.Timestamp(d) for d in date_range)))
]

st.write(filtered_df)

# Salary Distribution
st.subheader("Salary Distribution")
plt.figure(figsize=(10, 6))
sns.histplot(filtered_df["Salary"], kde=True)
plt.xticks(rotation=45)
st.pyplot(plt)

# Top Companies by Job Listings
st.subheader("Top Companies by Job Listings")
top_companies = filtered_df["Company Name"].value_counts().head(10)
st.bar_chart(top_companies)

st.subheader("Job Links")
for i, row in filtered_df.iterrows():
    st.write(f"[{row['Job Title']}]({row['Job Link']}) at {row['Company Name']}")
