import pandas as pd
import streamlit as st

from db_utils import get_engine
from streamlit_app.utilities import get_category_level_data

engine = get_engine()

st.set_page_config(page_title="Trends", layout='wide')
st.write("# The Base Data")

df = get_category_level_data(engine)

category_df = pd.read_sql("""
    SELECT subcategory 
    FROM incident.category
    
    UNION 
    
    SELECT distinct subcategory
    FROM incident.incident_category
""", engine)

subcategories = list(category_df.sort_values(by='subcategory').subcategory)

st.write("## Categories")
subcategories_to_display = st.multiselect("OPTIONAL: Include only the following subcategories", subcategories)

if len(subcategories_to_display) > 0:
    show_df = df[df.subcategories.apply(lambda x: any([_ in x for _ in subcategories_to_display]))]
else:
    show_df = df

st.dataframe(show_df.drop(columns='incident_id'), hide_index=True)
