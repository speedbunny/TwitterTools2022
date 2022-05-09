#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:58:12 2022

@author: saraheaglesfield
"""

import requests
import os
import json
import pandas as pd


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
os.chdir('/Volumes/Data')
os.environ["BEARER_TOKEN"] = "YOUR_BEARER_TOKEN_HERE"
bearer_token = os.environ.get("BEARER_TOKEN")



# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    return "https://api.twitter.com/2/tweets/search/all/"


def get_params():
    
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    
    return {"query": "from:zenxv",
            "since_id": "10000",
            "max_results":"500",
            "pagination_token":"NEXT_PAGE_HERE"}


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
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    json_string = json.dumps(json_response, indent=4, sort_keys=True)
    a_json = json.loads(json_string)
    datalist = a_json['data'] 
    tweets = pd.json_normalize(datalist)
    df = pd.DataFrame(tweets)
    df.to_csv('tweets.csv', mode='a', index=False)

if __name__ == "__main__":
    main()


