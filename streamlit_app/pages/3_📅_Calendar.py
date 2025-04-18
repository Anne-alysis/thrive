from streamlit_app.utilities import get_data
from streamlit_calendar import calendar
import streamlit as st

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
calendar_events = [
    {
        "title": "Pick up kids",
        "start": "2025-04-30T08:30:00",
        "end": "2025-04-30T10:30:00",
        "resourceId": "a",
        "textColor": 'red',
        "backgroundColor": 'green',

       # "borderColor": 'purple'
    },
    {
        "title": "boreas",
        "start": "2025-04-14T08:30:00",
        "end": "2025-04-14T10:30:00",
              "backgroundColor": "#FF6C6C",
              "borderColor": "#FF6C6C"
    },
    {
        "title": "Event 3",
        "start": "2023-07-31T10:40:00",
        "end": "2023-07-31T12:30:00",
        "resourceId": "a",
    }
]
custom_css="""
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
    #custom_css=custom_css,
    key='calendar', # Assign a widget key to prevent state loss
    )
#st.write(calendar)