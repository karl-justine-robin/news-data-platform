import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title="News Dashboard",
    layout="wide",
)

st.title("📰 News Data Platform Dashboard")

load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

# -------------------------------------
# Sidebar
# -------------------------------------

st.sidebar.title("⚙ Dashboard")

refresh = st.sidebar.button("🔄 Refresh Dashboard")

st.sidebar.markdown("---")

search = st.sidebar.text_input(
    "🔍 Search Articles",
    placeholder="Headline or body...",
)

source_filter = st.sidebar.selectbox(
    "📰 Source",
    [
        "All",
        "Bloomberg",
        "BusinessDesk",
        "CNBC",
        "Reuters",
    ],
)

st.sidebar.markdown("---")

if refresh:
    st.rerun()

# -------------------------------------
# Articles API
# -------------------------------------

params = {
    "page": 1,
    "size": 100,
    "sort": "published_at",
    "direction": "desc",
}

if source_filter != "All":
    params["source"] = source_filter

if search:
    response = requests.get(
        f"{API_URL}/api/v1/search",
        params={"q": search},
        timeout=10,
    )
else:
    response = requests.get(
        f"{API_URL}/api/v1/articles",
        params=params,
        timeout=10,
    )

if response.status_code != 200:
    st.error(f"API Error: {response.status_code}")
    st.stop()

data = response.json()

if len(data["items"]) == 0:
    st.warning("No articles found.")
    st.stop()

df = pd.DataFrame(data["items"])

# -------------------------------------
# Analytics API
# -------------------------------------

source_response = requests.get(
    f"{API_URL}/api/v1/analytics/sources",
    timeout=10,
)

trend_response = requests.get(
    f"{API_URL}/api/v1/analytics/publication-trend",
    timeout=10,
)

if source_response.status_code != 200:
    st.error("Failed to load source analytics.")
    st.stop()

if trend_response.status_code != 200:
    st.error("Failed to load publication trend.")
    st.stop()

source_df = pd.DataFrame(source_response.json())
trend_df = pd.DataFrame(trend_response.json())

# -------------------------------------
# KPI Metrics
# -------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Articles",
    len(df),
)

col2.metric(
    "Sources",
    df["source"].nunique(),
)

col3.metric(
    "Publication Dates",
    df["published_at"].nunique(),
)

st.divider()

# -------------------------------------
# Charts
# -------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Articles by Source")

    fig = px.bar(
        source_df,
        x="source",
        y="count",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.subheader("Publication Trend")

    fig = px.line(
        trend_df,
        x="published_at",
        y="count",
        markers=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

st.divider()

# -------------------------------------
# Articles Table
# -------------------------------------

st.subheader("Articles")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)