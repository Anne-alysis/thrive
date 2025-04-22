import pandas as pd
import streamlit as st
from lets_plot import *
from streamlit_letsplot import st_letsplot
from streamlit_app.utilities import get_data
import datetime
LetsPlot.setup_html()
st.set_page_config(page_title="Trends")


df = get_data()

st.write("# Trend Examples")
custom_labels = [_.capitalize() for _ in df.custom_label.unique()]
filtered_label = st.selectbox("Select custom label:", ['All'] + custom_labels)


dates = st.date_input("Choose a date range (type in, or use drop down):",
                      value=(df.date.min(), df.date.max()),
                      min_value=df.date.min(),
                      max_value=df.date.max(), format='YYYY-MM-DD')

if len(dates) != 2:
    st.warning('Please select a date range.')
    st.stop()

start_date = dates[0]
end_date = dates[1]

# filter by custom label
if filtered_label != 'All':
    filtered_df = df[df.custom_label.str.capitalize() == filtered_label]
    st.write(f"Showing only custom label: {filtered_label}")

else:
    filtered_df = df

# filter by date
filtered_df = filtered_df[(filtered_df.date >= start_date) & (filtered_df.date <= end_date)]
filtered_df['date'] = pd.to_datetime(filtered_df.date)

st.write("## Histogram")

g = ggplot(filtered_df, aes(x='date')) + geom_histogram(fill='darkgreen') + theme_light() + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents")
g.show()

st_letsplot(g)

st.write("## Trend Line")

agg_df = filtered_df.groupby(['date', 'custom_label'], as_index=False)['incident_id']\
    .count().rename(columns={'incident_id': 'n'})

date_df = pd.DataFrame({'date': pd.date_range(start=filtered_df.date.min(), end=filtered_df.date.max())})
n_labels = filtered_df.custom_label.nunique()
plot_df = pd.DataFrame()
for label in filtered_df.custom_label.unique():
    date_df['custom_label'] = label
    temp = pd.merge(date_df, agg_df, on=['date', 'custom_label'], how='left')
    temp['n']= temp['n'].fillna(0)
    plot_df = pd.concat([plot_df, temp])

g = ggplot(plot_df, aes(x='date', y='n')) + geom_point(aes(col='custom_label')) +  \
    geom_line(aes(col='custom_label')) +\
    theme_light() + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents By Label")
g.show()

st_letsplot(g)
