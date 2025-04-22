from typing import Dict

import pandas as pd
import streamlit as st
from streamlit_app.utilities import get_data, set_date_range, filter_by_generic_label, filter_data_by_date_range
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendar View", layout='wide')

severity_colors = {'HIGH': 'red', 'MEDIUM': 'yellow', 'LOW': 'black'}

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        #  "right": "dayGridMonth",
    },
    "initialView": "dayGridMonth",

}

custom_css = """
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""


def form_event(row: pd.Series) -> Dict[str, str]:
    return {
        "title": row.description.split('.')[0],
        "start": str(row.date),
        "end": str(row.date),
        "backgroundColor": severity_colors.get(row.severity, 'black'),
        "severity": row.severity,
        "category": row.category,
        "subcategory": row.subcategory,
        "custom_label": row.custom_label
    }


st.write("# Calendar View")

df = get_data()

# get custom label info
filtered_df = filter_by_generic_label('severity', ['High', 'Medium', 'Low'], df)

calendar_events = [form_event(row) for row in filtered_df.itertuples()]

displayed_calendar = calendar(
    events=calendar_events,
    options=calendar_options,
    # custom_css=custom_css,
    # key='calendar',  # Assign a widget key to prevent state loss [this seems to be messing with the filtering, so removing for now]
)
st.write(displayed_calendar)
