from typing import List

import pandas as pd
import streamlit as st


def get_category_level_data(engine) -> pd.DataFrame:
    # this assumes (hopefully, one major category per incident...)
    return pd.read_sql("""
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


def get_subcategory_level_data(engine) -> pd.DataFrame:
    # this assumes (hopefully, one major category per incident...)
    return pd.read_sql("""
        SELECT i.incident_id
        , incident_at::date as date
        , severity, custom_label, description
        , category
        , subcategory
        FROM incident.incident i 
        LEFT JOIN incident.incident_category ic on i.incident_id = ic.incident_id
        WHERE TRUE
            and user_id = 1 
    """, engine)


def set_date_range(df: pd.DataFrame) -> (str, str):
    min_date, max_date = df[df.date.notnull()].date.min(), df[df.date.notnull()].date.max()
    dates = st.date_input("Choose a date range (type in, or use drop down):",
                          value=(min_date, max_date),
                          min_value=min_date,
                          max_value=max_date, format='YYYY-MM-DD')

    if len(dates) != 2:
        st.warning('Please select a date range.')
        st.stop()

    return dates[0], dates[1]


def filter_data_by_date_range(filtered_df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    # explicitly keep any incidents with no date assigned
    filtered_df = filtered_df[((filtered_df.date >= start_date) & (filtered_df.date <= end_date))
                              | (filtered_df.date.isnull())]
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
