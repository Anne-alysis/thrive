import logging

import pandas as pd
from db_utils import get_engine
from sqlalchemy import text

engine = get_engine()

df = pd.read_csv("data/categories.csv")
df['subcategory'] = df.categories.apply(lambda x: x.split(', '))
df = df.explode('subcategory')

with engine.begin() as txn:
    txn.execute(text("""DROP TABLE IF EXISTS tmp_incident_category;"""))

    txn.execute(text("""
           CREATE TEMPORARY TABLE tmp_incident_category (   
           incident_id uuid,
           subcategory character varying)
       """))

    df[['incident_id', 'subcategory']].to_sql("tmp_incident_category", txn, if_exists='append',
                                              index=False, chunksize=500, method='multi')

    r = txn.execute(text("""
        INSERT INTO incident.incident_category
        (incident_id, subcategory)
        SELECT incident_id, subcategory
        FROM tmp_incident_category
    """))

    logging.info(f"Rows upserted: {r.rowcount}")

    txn.execute(text("""DROP TABLE IF EXISTS tmp_incident_category;"""))