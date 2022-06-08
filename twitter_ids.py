#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:58:12 2022

@author: saraheaglesfield
"""

import requests
import os
import json
import pandas as pd


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
os.chdir('/Volumes/Data')
os.environ["BEARER_TOKEN"] = "YOUR_TOKEN"
bearer_token = os.environ.get("BEARER_TOKEN")

def cleanuserlist(list1):
    # This cleans the imported CSV userlist of unwanted punctuation for use in the URL
    # for use in the URL request
    return str(list1).replace('[','').replace(']','').replace('\'','').replace(' ','')

def load_users(csv_file,user_col):
    # Specify the CSV file and the column containing the list of
    # Twitter usernames
    df = pd.read_csv(csv_file, usecols=[user_col])
    n = 100  #chunk row size
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    #TO DO: AUTOMATE ITERATION THROUGH ROWS MANUALLY CHANGE 0 to ITERATE THROUGH EACH ROW
    list_str = list_df[0].to_string(header=False,
                      index=False,
                      index_names=False).split('\n')

    users_str = [','.join(ele.split()) for ele in list_str]
    users_str = cleanuserlist(users_str)
    return users_str


def create_url():
    #Change this to point to your CSV and Username Column
    users_str = load_users('twitterusers.csv', 'Username')
    user_fields = "user.fields=id"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?usernames={}&{}".format(users_str, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()



url = create_url()
json_response = connect_to_endpoint(url)
json_string = json.dumps(json_response, indent=4, sort_keys=True)
a_json = json.loads(json_string)
datalist = a_json['data'] 
userinfo = pd.json_normalize(datalist)
userinfo.drop(['name', 'username'], axis=1, inplace=True)
df = pd.DataFrame(userinfo)
#TO DO: REMERGE ALL DFS TO ONE CSV. SAVE AS CSVS OF 100 ROWS MANUALLY FOR NOW
df.to_csv('output.csv', index=False)
