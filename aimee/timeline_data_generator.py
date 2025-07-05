import datetime
import json
from typing import List

import numpy as np
import pandas as pd
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import plotly.express as px

"""
This is a helper script to generate fake data to use as examples with the Highcharts Timeline library

https://code.highcharts.com/modules/timeline.js library  

"""

category_names = [
    'Missed/late pickups/drop-offs',
    'Failure to communicate child-related info',
    'Interference w/ parenting time',
    'Emotional outbursts in front of child',
    'Failure to provide necessities',
    'Medical neglect',
    'Attempt at alienation',
    'Police/CPS involvement',
    'Exposing child to inappropriate env'
]

colors = [
    '#E74C3C',  # Vibrant Red
    '#3498DB',  # Bright Blue
    '#2ECC71',  # Emerald Green
    '#F39C12',  # Orange
    '#9B59B6',  # Purple
    '#1ABC9C',  # Turquoise
    '#E67E22',  # Carrot Orange
    '#34495E',  # Dark Slate
    '#F1C40F',  # Golden Yellow
    '#95A5A6'  # Cool Gray
]

probabilities = [0.7, 0.05, 0.05, 0.01, 0.01,
                 0.02, 0.05, 0.01, 0.1]


@dataclass
class Category:
    category_name: str
    color: str
    probability: float


categories = [Category(category_name, color, p) for category_name, color, p in
              zip(category_names, colors, probabilities)]


@dataclass_json
@dataclass
class Connector:
    connectorColor: str  # line to box


@dataclass_json
@dataclass
class Marker:
    fillColor: str  # dot on timeline


@dataclass_json
@dataclass
class Incident:
    x: str  # date
    name: str  # header in tooltip
    label: str  # what shows in vis, not tooltip
    description: str
    dataLabels: Connector
    marker: Marker
    dotColor: str


def get_random_dates_from_range(start_date, end_date, n_incidents) -> List[str]:
    # Create full date range
    all_dates = pd.date_range(start_date, end_date, freq='D')
    iso_dates = all_dates.strftime('%Y-%m-%d')

    # Randomly sample from it
    return np.random.choice(iso_dates, n_incidents, replace=True)


def get_incident(date: str) -> Incident:
    category = np.random.choice(categories, p=probabilities)
    return Incident(
        x=date,
        name=category.category_name,
        label=category.category_name,
        description='Dogs are awesome.',
        dataLabels=Connector(category.color),
        marker=Marker(category.color),
        dotColor=category.color
    )


def serialize(data_list) -> str:
    return json.dumps([_.to_dict() for _ in data_list])


n_incidents = 100
start_date = datetime.date.fromisoformat('2025-01-01')
end_date = datetime.date.today()

dates = get_random_dates_from_range(start_date, end_date, n_incidents)

incidents = [get_incident(_) for _ in dates]

json_output = serialize(incidents)
print(json_output)

df = pd.DataFrame(incidents)

####################
# donut chart in python

agg_df = df['name'].value_counts(normalize=True).reset_index()
fig = px.pie(agg_df, values='proportion', names='name', hole=0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


### export aggregate for highcharts
@dataclass_json
@dataclass
class AggregateIncident:
    name: str
    y: float


aggregate_incidents = [AggregateIncident(row.name, np.round(row.proportion * 100, 1)) for row in agg_df.itertuples()]
json_output = serialize(aggregate_incidents)
print(json_output)
print(len(incidents))
