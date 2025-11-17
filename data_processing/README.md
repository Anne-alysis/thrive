
## Quickstart for processing into database

```
create database thrive_db

alembic upgrade head

export PYTHONPATH='.'

python -m data_processing.read_mkdown_file --filename data/random_oddities.txt
python -m data_processing.read_mkdown_file --infer-dates
python data_processing/category_scraping.py

streamlit run streamlit_app/Homepage.py
```