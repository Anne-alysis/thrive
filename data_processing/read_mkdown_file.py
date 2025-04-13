import datetime
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

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


# def parse_date(s: str) -> datetime.date:
#

filename = 'data/incidents.txt'

with open(filename) as file:
    incidents = file.readlines()

# remove blank lines, clean up newline metadata
incidents_cleaned = [incident.strip('\n') for incident in incidents if incident != '\n']

# convert to dataframe
incident_df = pd.DataFrame(incidents_cleaned, columns=['full_incident'])

# transform the data into only a list of incidents and a period start and end
incident_df = get_period_boundaries(incident_df)


