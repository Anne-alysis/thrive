import streamlit as st

from utilities import get_engine, get_data

engine = get_engine()

df = get_data()

st.set_page_config(page_title="Survivor Data", page_icon="📊")

st.write("# Welcome!")

st.markdown("""Please select a page from the sidebar""")




