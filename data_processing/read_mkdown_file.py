import argparse
import logging

import numpy as np
import pandas as pd

from data_processing.utilities import get_period_boundaries, extract_possible_incident_date, estimate_date, upload_data

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

"""
# Overview
This script:
- read in a manually written text file that is semi-structured via markdown
- transforms the data into a normalized form
- puts it in the database

# Overall Data Structure and Processing Logic
This assumes the data may be chunked in sections of time (called "periods" below), 
where each section has a header that is followed by a list of incidents.  If no header exists,
dates will not be inferred.  

This list may or may not have a well-structured date associated with it.  If it does not, a date will 
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


def read_data_into_raw_df(filename: str) -> pd.DataFrame:
    with open(filename) as file:
        incidents = file.readlines()

    # remove blank lines, clean up newline metadata
    incidents_cleaned = [incident.strip('\n').strip('\t').strip("-") for incident in incidents if incident != '\n']

    # convert to dataframe
    return pd.DataFrame(incidents_cleaned, columns=['full_incident'])


def transform_data_for_upload(incident_df: pd.DataFrame, infer_dates: bool) -> pd.DataFrame:
    # transform the data into only a list of incidents and a period start and end
    incident_df = get_period_boundaries(incident_df)

    incident_df['parsed_date'] = incident_df.full_incident.apply(extract_possible_incident_date)
    if infer_dates:
        incident_df['incident_at'] = incident_df \
            .apply(lambda x: estimate_date(x.parsed_date, x.period_start_date, x.period_end_date), axis=1)
    else:
        incident_df['incident_at'] = np.nan

    incident_df['description'] = incident_df \
        .apply(lambda x: x.full_incident.replace(x.parsed_date or '', '').replace('[]', '').strip(' ').strip('.'),
               axis=1)

    # get into format for db insertion
    incident_df['user_id'] = 1
    incident_df['category'] = None
    incident_df['subcategory'] = None
    incident_df['severity'] = None
    incident_df['custom_label'] = None

    return incident_df[['user_id', 'incident_at', 'category', 'subcategory', 'severity',
                        'custom_label', 'description']]


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--filename', type=str, help='Specify raw markdown file to read from')
    parser.add_argument('--infer-dates', help='Add if want to estimate dates from headers',
                        action='store_true', default=False)

    args = parser.parse_known_args()
    if args.filename:
        filename = args.filename
    else:
        filename = 'data/incidents.txt'

    infer_dates = True if args.infer_dates else False

    logging.info(f"Reading data from {filename}..")
    incident_df = read_data_into_raw_df(filename)

    logging.info("Transforming data...")
    upload_df = transform_data_for_upload(incident_df, infer_dates)

    logging.info("Uploading data into db...")
    upload_data(upload_df)


if __name__ == '__main__':
    main()
