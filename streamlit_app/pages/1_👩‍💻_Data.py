import streamlit as st
from streamlit_app.utilities import get_data

df = get_data()

st.dataframe(df)
