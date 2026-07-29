import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="News Data Platform",
    page_icon="📰",
    layout="wide",
)

st.title("📰 News Data Platform")

# ---------------------------------
# Load data from FastAPI
# ---------------------------------
try:
    response = requests.get(f"{API_URL}/articles", timeout=10)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data["items"])

except Exception as e:
    st.error(f"Unable to connect to FastAPI:\n\n{e}")
    st.stop()

# ---------------------------------
# KPI Cards
# ---------------------------------
total_articles = data["total"]

country_count = (
    df["country"].nunique()
    if "country" in df.columns
    else 0
)

source_count = (
    df["source"].nunique()
    if "source" in df.columns
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Articles", total_articles)

with col2:
    st.metric("Countries", country_count)

with col3:
    st.metric("Sources", source_count)

# ---------------------------------
# Latest Articles
# ---------------------------------
st.subheader("Latest Articles")

st.dataframe(
    df,
    use_container_width=True,
)

# ---------------------------------
# Articles by Country
# ---------------------------------
if "country" in df.columns:

    country_summary = (
        df.groupby("country")
        .size()
        .reset_index(name="article_count")
    )

    st.subheader("Articles by Country")

    fig = px.bar(
        country_summary,
        x="country",
        y="article_count",
        title="Articles by Country",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )