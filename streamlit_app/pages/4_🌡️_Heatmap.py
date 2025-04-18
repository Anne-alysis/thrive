import streamlit as st
from plotly_calplot import calplot
import matplotlib.pyplot as plt

import pandas as pd
data = {
    "date": pd.date_range(start="2023-01-01", end="2023-12-31", freq="D"),
    "value": [i % 10 + 1 for i in range(365)]
}

# example case with every date filled out
df1 = pd.DataFrame(data)
fig = calplot(
    df1,
    x="date",  # Column with date information
    y="value",  # Column with values
    years_title="Activity Heatmap",  # Title of the calendar
    colorscale="Greens",  # Color scale for the heatmap
    showscale=True,  # Show color bar
    dark_theme=True
)

fig.show()



st.pyplot(fig)