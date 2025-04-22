import numpy as np
import pandas as pd
import streamlit as st
from db_utils import get_engine
from lets_plot import *
from streamlit_letsplot import st_letsplot

LetsPlot.setup_html()

st.set_page_config(page_title="Word Clouds", layout='wide')
st.write("# Word Clouds")
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


def get_agg_plot(df: pd.DataFrame, group: str) -> pd.DataFrame:
    n_groups = df[group].nunique()
    max_axis = n_groups * 1.2
    agg_df = df.groupby(group, as_index=False)['incident_id'].count().rename(columns={'incident_id': 'n'})

    agg_df['x'] = np.linspace(1, n_groups + 1, num=n_groups)
    agg_df['y'] = 0
    st.dataframe(agg_df[[group, 'n']].sort_values(by='n', ascending=False), hide_index=True, width=300)

    g = ggplot(agg_df, aes(x='x', y='y')) + geom_point(aes(size='n', col=group)) + theme_void() + \
        scale_size(range=[1, n_groups * 2]) + lims([0, max_axis * 1.5], [-2, 2]) + guides(size='none') + \
        ggsize(800, 400)
    g.show()

    return g


st.write("# Categories")
g = get_agg_plot(df, 'category')
st_letsplot(g)

st.write(" # Subcategories")
g = get_agg_plot(df, 'subcategory')
st_letsplot(g)

