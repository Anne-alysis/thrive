import os

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

        df = pd.read_sql("""
            SELECT incident_id, incident_at, description FROM incident.incident
            WHERE TRUE
                and user_id = 1 
                and incident_at is not null
        """, engine)

        st.session_state.df = df
        return df

    return st.session_state.df
