import streamlit as st
from lets_plot import *
from streamlit_letsplot import st_letsplot
from streamlit_app.utilities import get_data

LetsPlot.setup_html()
st.set_page_config(page_title="Trends")


df = get_data()

st.write("Trend Examples")

g = ggplot(df, aes(x='incident_at')) + geom_histogram(fill='darkgreen') + theme_light() + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents")
g.show()

st_letsplot(g)
