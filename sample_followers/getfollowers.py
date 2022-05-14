#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 03:58:12 2022

@author: saraheaglesfield
"""

import requests
import os
import json
import pandas as pd
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

os.environ["BEARER_TOKEN"] = "YOUR_TWITTER_BEARER_TOKEN_HERE"
bearer_token = os.environ.get("BEARER_TOKEN")
global next_cursor
next_cursor = -1


def create_url():   
    user_id = 19091173 # Steven Crowder
    return  "https://api.twitter.com/2/users/{}/followers".format(user_id)


def get_params():
    
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if (next_cursor != -1 ):
        return { "max_results":"1000",
                "pagination_token":"{}".format(next_cursor)}
    else:
        return {"max_results":"1000"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()



def main():
    global next_cursor, df
    while (next_cursor != None ):
        url = create_url()
        params = get_params()
        json_response = connect_to_endpoint(url, params)
        json_string = json.dumps(json_response, indent=4, sort_keys=True)
        a_json = json.loads(json_string)
        datalist = a_json['data'] 
        next_cursor = a_json['meta']['next_token']
        followerids = pd.json_normalize(datalist)
        df = pd.DataFrame(followerids)
        df.to_csv('followers.csv', mode='a', index=False)
        time.sleep(15)


if __name__ == "__main__" :
    main()
