# Yelp Fusion API Python Code Sample

## Overview
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to [API documentation](https://www.yelp.com/developers/documentation/v3)
for more details.


## Steps to run

To install the dependencies, run:
`pip install -r requirements.txt`.

Run the code sample without specifying any arguments:
`python sample.py`

Run the code sample by specifying the optional arguments:
`python sample.py --term="bars" --location="San Francisco, CA"`

Run test.ipynb for all of Philadelphia's resturants or test.py
`python test.py --term="bars" --location="Philadelphia, Pa" --street_path='street_name.txt', --data_path= 'data.pkl',--iteration=0`
