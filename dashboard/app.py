import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from dotenv import load_dotenv
from api_client import APIClient


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
# Pipeline Monitoring API
# -------------------------------------

try:

    pipeline_stats = (
        api_client
        .get_pipeline_stats()
    )

    latest_pipeline_run = (
        api_client
        .get_latest_pipeline_run()
    )

    pipeline_runs = (
        api_client
        .get_pipeline_runs()
    )

except requests.RequestException as error:

    st.error(
        f"Unable to load pipeline monitoring: {error}"
    )

    st.stop()


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
# Pipeline Monitoring
# -------------------------------------

st.subheader(
    "⚙ Pipeline Monitoring"
)

pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4 = (
    st.columns(4)
)


pipeline_col1.metric(
    "Total Runs",
    pipeline_stats["total_runs"],
)


pipeline_col2.metric(
    "Success Rate",
    f'{pipeline_stats["success_rate"]:.2f}%',
)


pipeline_col3.metric(
    "Avg Duration",
    f'{pipeline_stats["average_duration_seconds"]:.2f}s',
)


pipeline_col4.metric(
    "Records Processed",
    pipeline_stats["total_records_processed"],
)


st.subheader(
    "Latest Pipeline Run"
)


if latest_pipeline_run:

    latest_col1, latest_col2, latest_col3 = (
        st.columns(3)
    )

    latest_col1.metric(
        "Status",
        latest_pipeline_run["status"],
    )

    latest_col2.metric(
        "Records",
        latest_pipeline_run["records_processed"],
    )

    latest_col3.metric(
        "Duration",
        f'{latest_pipeline_run["duration_seconds"]:.2f}s',
    )

    st.caption(
        f'Started: {latest_pipeline_run["start_time"]}'
    )

    if latest_pipeline_run["end_time"]:

        st.caption(
            f'Finished: {latest_pipeline_run["end_time"]}'
        )

    if latest_pipeline_run["error_message"]:

        st.error(
            latest_pipeline_run["error_message"]
        )

else:

    st.info(
        "No pipeline runs available."
    )


# -------------------------------------
# Pipeline Run History
# -------------------------------------

st.subheader(
    "Pipeline Run History"
)


if pipeline_runs:

    pipeline_df = pd.DataFrame(
        pipeline_runs
    )

    pipeline_df = pipeline_df[
        [
            "id",
            "pipeline_name",
            "status",
            "start_time",
            "end_time",
            "duration_seconds",
            "records_processed",
            "error_message",
        ]
    ]

    pipeline_df = pipeline_df.rename(
        columns={
            "id": "Run ID",
            "pipeline_name": "Pipeline",
            "status": "Status",
            "start_time": "Started",
            "end_time": "Finished",
            "duration_seconds": "Duration (s)",
            "records_processed": "Records",
            "error_message": "Error",
        }
    )

    st.dataframe(
        pipeline_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No pipeline run history available."
    )


st.divider()


# -------------------------------------
# Articles Table
# -------------------------------------

st.subheader(
    "Articles"
)


st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)