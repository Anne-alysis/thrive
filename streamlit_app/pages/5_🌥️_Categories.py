from typing import List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from db_utils import get_engine
from lets_plot import *

LetsPlot.setup_html()

st.set_page_config(page_title="Visualizing Categories", layout='wide')
st.write("# Visualizing Categories")
np.random.seed(27)

engine = get_engine()

# this assumes (hopefully, one major category per incident...)
df = pd.read_sql("""
     SELECT i.incident_id
     , category
     , subcategory
     FROM incident.incident i 
     JOIN incident.incident_category ic on i.incident_id = ic.incident_id
     WHERE TRUE
         and user_id = 1 
         and category is not null
 """, engine)


def get_agg_plot(df: pd.DataFrame, group: List[str]) -> None:
    agg_df = df.groupby(group, as_index=False)['incident_id'].count().rename(columns={'incident_id': 'n'})
    n_groups = len(agg_df)

    agg_df['x'] = np.arange(n_groups)
    agg_df['y'] = np.random.rand(n_groups) * 10
    st.dataframe(agg_df[group + ['n']].sort_values(by='n', ascending=False), hide_index=True, width=300)

    # g = ggplot(agg_df, aes(x='x', y='y')) + geom_point(aes(size='n', col=group[-1])) + theme_void() + \
    #     scale_size(range=[1, n_groups * 2]) + lims([0, max_axis * 1.5], [-2, 2]) + guides(size='none') + \
    #     ggsize(800, 400)
    # g.show()

    # Create bubble chart
    fig = go.Figure(data=[go.Scatter(
        x=agg_df['x'],
        y=agg_df['y'],
        mode='markers+text',
        marker=dict(
            size=agg_df['n'],  # Size based on count
            sizemode='area',  # Area proportional to value
            sizeref=2. * max(agg_df['n']) / (60. ** 2),  # Scale bubbles
            color=np.arange(n_groups),  # Different color for each category
            colorscale='Plasma',
            showscale=False,
            opacity=0.8,
            line=dict(width=1, color='black')
        ),
        text=agg_df[group[-1]] + '<br>' + agg_df['n'].astype(str),
        hoverinfo='text',
        textposition="bottom center"
    )])

    # Update layout
    fig.update_layout(
        # title='',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        width=800
    )
    # fig.show()

    st.plotly_chart(fig)

    return


st.write("# Categories")
get_agg_plot(df, ['category'])

st.write(" # Subcategories")
get_agg_plot(df, ['category', 'subcategory'])
