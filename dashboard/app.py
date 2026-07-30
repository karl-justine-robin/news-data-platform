import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="News Dashboard",
    layout="wide"
)

st.title("📰 News Data Platform Dashboard")

API_URL = os.getenv("API_URL", "http://192.168.100.8:8000")

# -------------------------------------
# Search
# -------------------------------------

search = st.text_input(
    "🔍 Search Articles",
    placeholder="Search by headline or body..."
)

if search:
    response = requests.get(
        f"{API_URL}/search",
        params={"q": search}
    )
else:
    response = requests.get(
        f"{API_URL}/articles",
        params={
            "page": 1,
            "size": 100,
            "sort": "published_at",
            "direction": "desc",
        },
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

source_response = requests.get(f"{API_URL}/analytics/sources")
trend_response = requests.get(f"{API_URL}/analytics/publication-trend")

if source_response.status_code != 200:
    st.error("Failed to load source analytics.")
    st.stop()

if trend_response.status_code != 200:
    st.error("Failed to load publication trend.")
    st.stop()

source_df = pd.DataFrame(source_response.json())
trend_df = pd.DataFrame(trend_response.json())

# -------------------------------------
# KPI Cards
# -------------------------------------

total_articles = data["total"]

source_count = (
    df["source"].nunique()
    if "source" in df.columns
    else 0
)

latest_date = (
    df["published_at"].max()
    if "published_at" in df.columns
    else "N/A"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Articles", total_articles)

with col2:
    st.metric("Sources", source_count)

with col3:
    st.metric("Latest Date", latest_date)

st.divider()

# -------------------------------------
# Articles by Source
# -------------------------------------

if not source_df.empty:

    fig = px.bar(
        source_df,
        x="source",
        y="count",
        title="Articles by Source",
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------
# Articles by Date
# -------------------------------------

if not trend_df.empty:

    fig2 = px.line(
        trend_df,
        x="published_at",
        y="count",
        markers=True,
        title="Articles by Publication Date",
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------
# Latest Articles
# -------------------------------------

st.subheader("Latest Articles")

display_columns = [
    "headline",
    "source",
    "published_at",
    "loaded_at",
]

available_columns = [
    c for c in display_columns
    if c in df.columns
]

st.dataframe(
    df[available_columns],
    use_container_width=True,
    hide_index=True,
)