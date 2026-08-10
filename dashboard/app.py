import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from dotenv import load_dotenv

from dashboard.api_client import APIClient


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

api_client = APIClient(API_URL)


# -------------------------------------
# Sidebar
# -------------------------------------

st.sidebar.title("⚙ Dashboard")

refresh = st.sidebar.button(
    "🔄 Refresh Dashboard"
)

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


try:

    if search:

        data = api_client.search_articles(
            search
        )

    else:

        data = api_client.get_articles(
            params
        )

except requests.RequestException as error:

    st.error(
        f"Unable to connect to API: {error}"
    )

    st.stop()


articles = data.get(
    "items",
    [],
)


if not articles:

    st.warning(
        "No articles found."
    )

    st.stop()


df = pd.DataFrame(articles)


# -------------------------------------
# Warehouse Analytics API
# -------------------------------------

try:

    source_data = (
        api_client
        .get_warehouse_sources()
    )

    date_data = (
        api_client
        .get_warehouse_dates()
    )

    month_data = (
        api_client
        .get_warehouse_months()
    )

    day_data = (
        api_client
        .get_warehouse_days_of_week()
    )

except requests.RequestException as error:

    st.error(
        f"Unable to load warehouse analytics: {error}"
    )

    st.stop()


source_df = pd.DataFrame(
    source_data
)

date_df = pd.DataFrame(
    date_data
)

month_df = pd.DataFrame(
    month_data
)

day_df = pd.DataFrame(
    day_data
)


# -------------------------------------
# KPI Metrics
# -------------------------------------

total_articles = (
    source_df["article_count"].sum()
    if not source_df.empty
    else 0
)

total_sources = (
    source_df["source"].nunique()
    if not source_df.empty
    else 0
)

total_dates = (
    date_df["date"].nunique()
    if not date_df.empty
    else 0
)


col1, col2, col3 = st.columns(3)


col1.metric(
    "Articles",
    int(total_articles),
)


col2.metric(
    "Sources",
    int(total_sources),
)


col3.metric(
    "Publication Dates",
    int(total_dates),
)


st.divider()


# -------------------------------------
# Articles by Source
# -------------------------------------

left, right = st.columns(2)


with left:

    st.subheader(
        "Articles by Source"
    )

    fig = px.bar(
        source_df,
        x="source",
        y="article_count",
        labels={
            "source": "Source",
            "article_count": "Articles",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# -------------------------------------
# Articles by Date
# -------------------------------------

with right:

    st.subheader(
        "Publication Trend"
    )

    if not date_df.empty:

        date_df["date"] = pd.to_datetime(
            date_df["date"]
        )

        fig = px.line(
            date_df,
            x="date",
            y="article_count",
            markers=True,
            labels={
                "date": "Date",
                "article_count": "Articles",
            },
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info(
            "No publication data available."
        )


st.divider()


# -------------------------------------
# Monthly Analytics
# -------------------------------------

st.subheader(
    "Articles by Month"
)


if not month_df.empty:

    month_df["period"] = (
        month_df["month_name"]
        + " "
        + month_df["year"].astype(str)
    )

    fig = px.bar(
        month_df,
        x="period",
        y="article_count",
        labels={
            "period": "Month",
            "article_count": "Articles",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.info(
        "No monthly analytics available."
    )


# -------------------------------------
# Day of Week Analytics
# -------------------------------------

st.subheader(
    "Articles by Day of Week"
)


if not day_df.empty:

    fig = px.bar(
        day_df,
        x="day_of_week",
        y="article_count",
        labels={
            "day_of_week": "Day",
            "article_count": "Articles",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.info(
        "No day-of-week analytics available."
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