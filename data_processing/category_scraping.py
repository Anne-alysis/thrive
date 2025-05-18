import logging

import pandas as pd
from db_utils import get_engine
from sqlalchemy import text

engine = get_engine()

df = pd.read_csv("data/categories_hash.csv")
df['subcategory'] = df.categories.apply(lambda x: x.split(','))
df = df.explode('subcategory')

with engine.begin() as txn:
    txn.execute(text("""DROP TABLE IF EXISTS tmp_incident_category;"""))

    txn.execute(text("""
           CREATE TEMPORARY TABLE tmp_incident_category (   
           description_hash character varying,
           subcategory character varying)
       """))

    df[['description_hash', 'subcategory']].to_sql("tmp_incident_category", txn, if_exists='append',
                                              index=False, chunksize=500, method='multi')

    r = txn.execute(text("""
        INSERT INTO incident.incident_category as c 
        (incident_id, subcategory)
        SELECT i.incident_id, t.subcategory
        FROM tmp_incident_category t 
        JOIN incident.incident i on i.description_hash = t.description_hash
        ON CONFLICT (incident_id, subcategory)
        DO UPDATE SET 
            category = coalesce(c.category, EXCLUDED.category)
    """))

    logging.info(f"Rows upserted: {r.rowcount}")

    txn.execute(text("""DROP TABLE IF EXISTS tmp_incident_category;"""))

    r = txn.execute(text("""
        UPDATE incident.incident_category c
        SET category = t.category
        FROM (SELECT ic.incident_id, ic.subcategory, c.category FROM incident.incident_category ic
            LEFT JOIN incident.category c on c.subcategory = ic.subcategory
            WHERE ic.category is null) t
        WHERE t.incident_id = c.incident_id and c.subcategory = t.subcategory
    """))

    logging.info(f"Rows upserted: {r.rowcount}")


