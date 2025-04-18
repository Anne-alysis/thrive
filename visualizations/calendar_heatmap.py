import pandas as pd
from plotly_calplot import calplot

from db_utils import get_engine

engine = get_engine()

df = pd.read_sql("""
    SELECT incident_id, incident_at FROM incident.incident
    WHERE TRUE
        and user_id = 1 
        and incident_at is not null
""", engine)

df['date'] = df['incident_at'].dt.date
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

fig = calplot(
    agg_df[agg_df.date.dt.year == 2023],
    x="date",  # Column with date information
    y="n",  # Column with values
    years_title="Activity Heatmap",  # Title of the calendar
    colorscale="Greens",  # Color scale for the heatmap
    showscale=True,  # Show color bar
    dark_theme=True
)
fig.show()

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
