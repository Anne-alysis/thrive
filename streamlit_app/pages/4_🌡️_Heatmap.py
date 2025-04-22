import plotly.io as pio
import streamlit as st
from plotly_calplot import calplot
from streamlit_app.utilities import get_data, set_date_range, filter_by_generic_label, filter_data_by_date_range

st.set_page_config(page_title="Calendar Heatmap View", layout='wide')

st.write("# Calendar Heatmap View")

df = get_data()
start_date, end_date = set_date_range(df)

# get custom label info
filtered_df = filter_by_generic_label('severity', ['All', 'High', 'Medium', 'Low'], df)

# filter by date
filtered_df = filter_data_by_date_range(filtered_df, start_date, end_date)

if filtered_df.empty:
    st.write("No data to display")
else:


    agg_df = filtered_df.groupby('date', as_index=False)['incident_id'] \
        .count().rename(columns={'incident_id': 'n'})

    fig = calplot(
        agg_df,
        x="date",  # Column with date information
        y="n",  # Column with values
        years_title="Activity Heatmap",  # Title of the calendar
        colorscale="Greens",  # Color scale for the heatmap
        showscale=True,  # Show color bar
        dark_theme=True
    )
    #fig.show()

    # fig.update_layout(height = 500,
    #                   width = 1500,
    #                   font=dict(size = 16),
    #                   margin = {'t':0, 'b':0, 'l':40})

    # fig.show()
    # plt.savefig(f'plots/heatmap.pdf', bbox_inches='tight')
    pio.write_image(fig, 'plots/calplot.png', engine='kaleido')

    st.image("plots/calplot.png", caption="")
