import pandas as pd
import plotly.io as pio
import streamlit as st
from plotly_calplot import calplot
from streamlit_app.utilities import get_data

df = get_data()

agg_df = df.groupby('date', as_index=False).count()[['date', 'incident_at']].rename(columns={'incident_at': 'n'})

fig = calplot(
    agg_df,
    x="date",  # Column with date information
    y="n",  # Column with values
    years_title="Activity Heatmap",  # Title of the calendar
    colorscale="Greens",  # Color scale for the heatmap
    showscale=True,  # Show color bar
    dark_theme=True
)
fig.show()

# fig.update_layout(height = 500,
#                   width = 1500,
#                   font=dict(size = 16),
#                   margin = {'t':0, 'b':0, 'l':40})

#fig.show()
#plt.savefig(f'plots/heatmap.pdf', bbox_inches='tight')
pio.write_image(fig, 'plots/calplot.png', engine='kaleido')

st.image("plots/calplot.png", caption="Sunrise by the mountains")
