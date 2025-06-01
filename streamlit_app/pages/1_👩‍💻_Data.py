import streamlit as st
from db_utils import get_engine
from streamlit_app.utilities import get_category_level_data, get_subcategory_level_data

engine = get_engine()

st.set_page_config(page_title="Trends", layout='wide')
st.write("# The Base Data")

df = get_category_level_data(engine)
st.write("## Categories")
st.dataframe(df.drop(columns='incident_id'), hide_index=True)

