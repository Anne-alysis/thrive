
"""
# Overview
This script:
- read in a manually written text file that is semi-structured via markdown
- transforms the data into a normalized form
- puts it in the database

# Overall Data Structure and Processing Logic
This assumes the data is chunked in sections of time, where each section has a header
that is followed by a list of incidents.  This list may or may not have a well-structured
date associated with it.  If it does not, a date will be estimated in the following way:

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


filename = 'data/incidents.txt'

with open(filename) as file:
   incidents = file.readlines()


