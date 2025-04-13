import datetime
import re
import calendar
from termios import VLNEXT

import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from dataclasses import dataclass

"""
# Overview
This script:
- read in a manually written text file that is semi-structured via markdown
- transforms the data into a normalized form
- puts it in the database

# Overall Data Structure and Processing Logic
This assumes the data is chunked in sections of time (called "periods" below), 
where each section has a header that is followed by a list of incidents.  This list may 
or may not have a well-structured date associated with it.  If it does not, a date will 
be estimated in the following way:

1. if a specific date is given, use it
2. if a month is given only, then a random date within that month will be used
3. if no date is given, a random date within the chunk's time period will be used

# Chunk's Individual Structure
Each row in the data is either:

- begins with a header "#" and include a span of dates (e.g., "# May 2023-Oct 2023")
- is a given incident that may have a date or may not, but always begins with a "-"

## Possible Date Formats
For a given incident, here are the possibility of date formats. I could clean up the
base data more, but this is an illustration of how it can be done in code. Each
can also include lower and upper case letters

- "- [Jan 28]"
- "- [jan]"
- "August."
- "Oct 22"
- "- xxx" (e.g., no date)


"""
# set seed for same results
np.random.seed(47)


# this is super overkill perhaps, but fun to see these in action
@dataclass
class PatternGroup:
    pattern: str  # regex pattern to match on string
    group: int  # which group to extract of matched pattern


def get_period_boundaries(incident_df: pd.DataFrame) -> pd.DataFrame:
    """
    This transforms the header time period of each section into start/end dates
    for each incident period

    :param incident_df: unprocessed initial data frame
    :return: cleaned up data frame
    """

    # create period column, fill forward, and get period start and end dates
    incident_df['period'] = np.where(incident_df.full_incident.str.startswith("#"),
                                     incident_df.full_incident.str.strip("# "), np.nan)

    incident_df = incident_df.ffill()
    incident_df[['period_start_date_str', 'period_end_date_str']] = incident_df['period'].str.split('-', expand=True)
    incident_df['period_start_date'] = pd.to_datetime(incident_df['period_start_date_str'], format='mixed')
    incident_df['period_end_date'] = pd.to_datetime(incident_df['period_end_date_str'], format='mixed') + MonthEnd(0)

    # remove unnecessary headers and columns
    incident_df = incident_df[~incident_df.full_incident.str.startswith('#')] \
        .drop(columns=['period', 'period_start_date_str', 'period_end_date_str'])

    return incident_df


def extract_possible_incident_date(s: str) -> str:
    # look for dates given possible patterns
    patterns = [
        PatternGroup(r"^\s*\[(.*?)\]", 1),  # brackets
        PatternGroup(r"^\s*(\w+(\s+\w+)?)\.", 0)  # no brackets
    ]

    for pattern in patterns:
        match = re.search(pattern.pattern, s)
        if match:
            return match.group(pattern.group).strip('.').strip(' ')

    return None


def estimate_date(parsed_date: str, period_start_date: pd.Timestamp, period_end_date: pd.Timestamp) -> pd.Timestamp:
    if parsed_date is None:
        return pd.Timestamp(np.random.uniform(period_start_date.to_datetime64(), period_end_date.to_datetime64()))

    first_try_year = estimate_date_for_given_year(parsed_date, period_start_date)
    if period_start_date <= first_try_year <= period_end_date:
        return pd.to_datetime(first_try_year)

    second_try_year = estimate_date_for_given_year(parsed_date, period_end_date)
    if period_start_date<= second_try_year <= period_end_date:
        return pd.to_datetime(second_try_year)

    raise ValueError(f"Cannot find adequate date for {parsed_date} between {period_start_date} and {period_end_date}")


def estimate_date_for_given_year(parsed_date: str, period_date: pd.Timestamp) -> datetime.datetime:
    year = period_date.year

    split_parsed_date = parsed_date.split(" ")
    month = split_parsed_date[0].capitalize()

    if month in calendar.month_name:
        month_format = "%B"
    elif month in calendar.month_abbr:
        month_format = "%b"
    else:
        raise ValueError(f"Cannot find valid month from {month}")

    month_num = datetime.datetime.strptime(month, month_format).month

    if len(split_parsed_date) > 1 and split_parsed_date[1].isnumeric():
        day = int(split_parsed_date[1])
    else:
        # need to estimate day
        last_day_of_month = calendar.monthrange(year, month_num)[1]
        day = np.random.randint(1, last_day_of_month + 1)

    return datetime.datetime(year, month_num, day)


filename = 'data/incidents.txt'

with open(filename) as file:
    incidents = file.readlines()

# remove blank lines, clean up newline metadata
incidents_cleaned = [incident.strip('\n').strip("-") for incident in incidents if incident != '\n']

# convert to dataframe
incident_df = pd.DataFrame(incidents_cleaned, columns=['full_incident'])

# transform the data into only a list of incidents and a period start and end
incident_df = get_period_boundaries(incident_df)

incident_df['parsed_date'] = incident_df.full_incident.apply(extract_possible_incident_date)
incident_df['estimated_date'] = incident_df \
    .apply(lambda x: estimate_date(x.parsed_date, x.period_start_date, x.period_end_date), axis=1)
