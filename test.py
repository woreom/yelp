#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import traceback

from tqdm import tqdm
import pandas as pd
import time
import os



from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


# In[75]:


#get_ipython().system('{sys.executable} -m pip install -r requirements.txt')


# In[4]:


class Args():
    def __init__(self, term='restaurants', location='Philadelphia, Pa', streets_path='street_name.txt', data_path= 'data.pkl',iteration=0, iteration_main=0):
        
        self.term=term
        self.location=location
        self.streets_path=streets_path
        self.data_path=data_path
        self.iteration=iteration
        self.iteration_main=iteration_main
        
    def init_parsearges(self):
        ap = argparse.ArgumentParser()
        
        # Argument of insightface
        ap.add_argument("--term", default=self.term,
                        type=str, help='Search term')
        
        ap.add_argument("--location", default=self.location,
                        type=str, help='Search location')
        ap.add_argument("--streets_path", default=self.streets_path,
                        type=str, help='path to names of the streets')
        ap.add_argument("--data_path", default=self.data_path,
                        type=str, help='path to save data')
        
        ap.add_argument("-j","--iteration", default=self.iteration,
                         type=int, help='starting iteration')
        
        ap.add_argument("-i","--iteration-main", default=self.iteration,
                         type=int, help='starting iteration')

        args = ap.parse_args()
        
        return args


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= 'cwhlm9INXDobbgkfHlDhVVVVrncPHYNw9DoTcVLXuHkeCcGVVj7F7iPgMqaeW2JH5fKS24dRBQJoIkKJfLLgpJCGbPLmMuHSIqHsFsyyggXyzcohMWKSajdxGOHfX3Yx' 


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'Philadelphia, Pa'
SEARCH_LIMIT = 50


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

#     print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def logger(response,location ,i):
    error=response['error']['code']
    description=response['error']['description']
    with open('error.log', 'a') as f:
        string=f'{location} iteration={str(i)}\n    Error: "{error}"\n    Description: "{description}"\n'
        f.write(string)
        f.close()
    print(error)
    return error
    
def query_api(term, location, i):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        error=logger(response, location,i)
        if error == "ACCESS_LIMIT_REACHED":
            time.sleep(3600)
            return query_api(term, location, i)
        return []

#     business_id = businesses[0]['id']

#     print(u'{0} businesses found, querying business info ' \
#         'for the top result "{1}" ...'.format(
#             len(businesses), business_id))
#     response = get_business(API_KEY, business_id)

#     data = [get_business(API_KEY, business['id']) for business in businesses ]
#     print(u'Result for business "{0}" found:'.format(business_id))
#     pprint.pprint(response, indent=2)
    return businesses

def read_street(path='street_name.txt'):
    with open(path, 'r') as f:
        streets = f.readlines()
    return [street.replace("\n","") for street in streets]

def read_data(path='data.pkl'):
    return pd.read_pickle(path)

def main(term='restaurants', location='Philadelphia, Pa', streets_path='street_name.txt', data_path= 'data.pkl',iteration=0):
    
#     parser = argparse.ArgumentParser()

#     parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
#                         type=str, help='Search term (default: %(default)s)')
#     parser.add_argument('-l', '--location', dest='location',
#                         default=DEFAULT_LOCATION, type=str,
#                         help='Search location (default: %(default)s)')

#     input_values = parser.parse_args()

    try:

    	streets = read_street(path=streets_path)
    	data=[] if iteration==0 else read_data(data_path).to_dict(orient='records')
    	for (i, street) in tqdm(enumerate(streets)):
        	if i>=iteration:
        		address = street +' '+ location
        		data.extend(query_api(term, address,i))
        	else:
        		pass
        
    	print("-------------------SAVING DATA---------------------")
    	df = pd.DataFrame(data)
    	df.to_pickle(data_path)
    
    	return df

    except:
        df = pd.DataFrame(data)
        print("===========SAVING DATA=============")
        df.to_pickle(data_path)
        traceback.print_exc()
        sys.exit()
        
def super_main(term='restaurants', streets='street names/', data="Data/", i=0, j=0):
    files_and_directories = os.listdir(streets)
    cities = [ file[:file.find('.txt')] for file in files_and_directories if file.find('.txt')!=-1]
    inputs = [c.split(", ") for c in cities]
    try:
        for (k, arg) in tqdm(enumerate(inputs)):
            if k>=i:
                location=arg[1]+', '+arg[0]
                streets_path=streets+arg[0]+', '+arg[1]+'.txt'
                data_path= data+arg[1]+', '+arg[0]+'.pkl'
                iteration=j
                streets = read_street(path=streets_path)
                data=[] if iteration==0 else read_data(data_path).to_dict(orient='records')
                for (l, street) in tqdm(enumerate(streets)):
                    if i>=iteration:
                        address = street +' '+ location
                        data.extend(query_api(term, address,l))
                    else:
                        pass

                print("-------------------SAVING DATA---------------------")
                df = pd.DataFrame(data)
                df.to_pickle(data_path)

                return df
            else:
                pass

    except:
        df = pd.DataFrame(data)
        print("===========SAVING DATA=============")
        df.to_pickle(data_path)
        traceback.print_exc()
        sys.exit()
        
if __name__ == '__main__':
    args=Args(term='restaurants', streets_path='street names/', data_path="Data/",iteration_main=0, iteration=0)
    args=args.init_parsearges()
    super_main(term=args.term, streets=args.streets_path, i=args.iteration_main, j=args.iteration)


