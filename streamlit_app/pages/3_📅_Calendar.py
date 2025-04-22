from typing import Dict

import pandas as pd
import streamlit as st
from streamlit_app.utilities import get_data
from streamlit_calendar import calendar

df = get_data()

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

severity_colors = {'HIGH': 'red', 'MEDIUM': 'yellow', 'LOW': 'black'}


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


calendar_events = [form_event(row) for row in df.itertuples()]

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

calendar = calendar(
    events=calendar_events,
    options=calendar_options,
    # custom_css=custom_css,
    key='calendar',  # Assign a widget key to prevent state loss
)
st.write(calendar)
