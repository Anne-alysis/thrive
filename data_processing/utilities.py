import calendar
import datetime
import logging
import os
import re
from dataclasses import dataclass

import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from sqlalchemy import create_engine, text


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
    if period_start_date <= second_try_year <= period_end_date:
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


def upload_data(upload_df: pd.DataFrame) -> None:
    db_url = os.environ.get("LOCAL_DB_URL")
    if db_url is None:
        raise ValueError("Cannot get url! ")

    engine = create_engine(db_url)

    with engine.begin() as txn:
        txn.execute(text("""
            CREATE TEMPORARY TABLE tmp_incident (   
            user_id             integer not null,
            incident_at         timestamp with time zone,
            category            varchar,
            subcategory        varchar,
            description         varchar);
    
        """))

        upload_df.to_sql("tmp_incident", txn, if_exists='append', index=False, chunksize=500, method='multi')

        r = txn.execute(text("""
            INSERT INTO incident.incident as i 
            (user_id, incident_at, category, subcategory, description)
                SELECT t.user_id
                , t.incident_at
                , t.category
                , t.subcategory
                , t.description
                FROM tmp_incident t
            ON CONFLICT (user_id, incident_at, description) 
            DO UPDATE SET
                category = EXCLUDED.category
                , subcategory = EXCLUDED.subcategory
            WHERE i.category is distinct from EXCLUDED.category 
            or i.subcategory is distinct from EXCLUDED.subcategory
    
    
        """))
        logging.info(f"Rows upserted: {r.rowcount}")

        txn.execute(text("""DROP TABLE IF EXISTS tmp_incident;"""))

    return

    # change subcategory
    # add priority and other columns
