import pandas as pd
import streamlit as st
from lets_plot import *
from streamlit_app.utilities import get_data, set_date_range, filter_data_by_date_range, filter_by_generic_label
from streamlit_letsplot import st_letsplot

LetsPlot.setup_html()
st.set_page_config(page_title="Trends", layout='wide')

df = get_data()

st.write("# Trend Examples")
# get date range
start_date, end_date = set_date_range(df)

# get custom label info
custom_labels = [_.capitalize() for _ in df.custom_label.unique()]
filtered_df = filter_by_generic_label('custom_label', ['All'] + custom_labels, df)

# filter by date
filtered_df = filter_data_by_date_range(filtered_df, start_date, end_date)

st.write("## Histogram")
include_categories = st.checkbox("Include categories")

g = ggplot(filtered_df, aes(x='date')) + theme_light() + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents") + ggsize(800, 400)

if include_categories:
    g = g + geom_histogram(aes(fill='category'))
else:
    g = g + geom_histogram(fill='darkgreen')
g.show()

st_letsplot(g)

st.write("## Trend Line")

agg_df = filtered_df.groupby(['date', 'custom_label'], as_index=False)['incident_id'] \
    .count().rename(columns={'incident_id': 'n'})

date_df = pd.DataFrame({'date': pd.date_range(start=filtered_df.date.min(), end=filtered_df.date.max())})
n_labels = filtered_df.custom_label.nunique()
plot_df = pd.DataFrame()
for label in filtered_df.custom_label.unique():
    date_df['custom_label'] = label
    temp = pd.merge(date_df, agg_df, on=['date', 'custom_label'], how='left')
    temp['n'] = temp['n'].fillna(0)
    plot_df = pd.concat([plot_df, temp])

g = ggplot(plot_df, aes(x='date', y='n')) + geom_point(aes(col='custom_label')) + \
    geom_line(aes(col='custom_label')) + \
    theme_light() + ggsize(800, 400) + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents By Label")
g.show()

st_letsplot(g)
