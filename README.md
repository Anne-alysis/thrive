# thrive

 This repo is a playground for data.  Within, it:
 
- sets up a database migration tool (`alembic`) to apply and track changes to a database
- processes data from raw, only semi-structured files and inserts the data into the database
- reads data from the database to power visualizations

## Starting the dashboard
` streamlit run streamlit_app/Homepage.py`

## Todo:
- hit an open-source LLM API (or have a local one running) in order to classify some natural language text
