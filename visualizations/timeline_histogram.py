import pandas as pd
from lets_plot import *

from db_utils import get_engine

engine = get_engine()

df = pd.read_sql("""
    SELECT incident_id, incident_at FROM incident.incident
    WHERE user_id = 1; 
""", engine)

g = ggplot(df, aes(x='incident_at')) + geom_histogram(fill='darkgreen') + theme_light() + \
    labs(x="Date", y="Frequency of Incidents", title="Timeline of Incidents")
g.show()
ggsave(g, 'timeline.pdf', path='plots/')
