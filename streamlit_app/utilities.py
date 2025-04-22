import os
from typing import List

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


# Note: this is code that also exists in db_utils.py more generally but couldn't
# be reached by the streamlit_app app, so for simplicity, adding here for now
def get_engine():
    db_url = os.environ.get("LOCAL_DB_URL")
    if db_url is None:
        raise ValueError("Cannot get url! ")

    return create_engine(db_url)


def get_data() -> pd.DataFrame:
    engine = get_engine()

    if "data" not in st.session_state:
        # startup

        # this assumes (hopefully, one major category per incident...)
        df = pd.read_sql("""
            SELECT i.incident_id
            , incident_at::date as date
            , severity, custom_label, description
            , string_agg(distinct category, ',') as category
            FROM incident.incident i 
            LEFT JOIN incident.incident_category ic on i.incident_id = ic.incident_id
            WHERE TRUE
                and user_id = 1 
                and incident_at is not null
            GROUP BY 1,2,3,4,5
        """, engine)

        st.session_state.df = df
        return df

    return st.session_state.df


def set_date_range(df: pd.DataFrame) -> (str, str):
    dates = st.date_input("Choose a date range (type in, or use drop down):",
                          value=(df.date.min(), df.date.max()),
                          min_value=df.date.min(),
                          max_value=df.date.max(), format='YYYY-MM-DD')

    if len(dates) != 2:
        st.warning('Please select a date range.')
        st.stop()

    return dates[0], dates[1]


def filter_data_by_date_range(filtered_df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    filtered_df = filtered_df[(filtered_df.date >= start_date) & (filtered_df.date <= end_date)]
    filtered_df['date'] = pd.to_datetime(filtered_df.date)

    return filtered_df


def filter_by_generic_label(label: str, label_possibilities: List[str], df: pd.DataFrame) -> pd.DataFrame:
    displayed_label = label.replace("_", " ").capitalize()
    filtered_label = st.selectbox(f"Select {displayed_label}:", ['All'] + label_possibilities)

    # filter by custom label
    if filtered_label != 'All':
        filtered_df = df[df[label].str.capitalize() == filtered_label]
        st.write(f"Showing only {displayed_label}: {filtered_label}")

    else:
        filtered_df = df

    return filtered_df
