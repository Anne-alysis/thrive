import streamlit as st
from streamlit_app.utilities import get_data

st.set_page_config(page_title="Trends", layout='wide')
st.write("# The Base Data")

df = get_data()

st.dataframe(df)
