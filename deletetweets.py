#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 12:36:13 2023
@author: saraheaglesfield
Warning: this will delete ALL your tweets
"""

import os
import requests
from requests_oauthlib import OAuth1
import json

# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='xxxx'
# export 'CONSUMER_SECRET'='xxxx' etc

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

oauth = OAuth1(CONSUMER_KEY,
               client_secret=CONSUMER_SECRET,
               resource_owner_key=ACCESS_TOKEN,
               resource_owner_secret=ACCESS_TOKEN_SECRET)

def get_tweets(user_id):
    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={user_id}&count=200"
    response = requests.get(url, auth=oauth)

    if response.status_code != 200:
        raise Exception(f"Error while getting tweets: {response.status_code}")

    return response.json()

def delete_tweet(tweet_id):
    url = f"https://api.twitter.com/1.1/statuses/destroy/{tweet_id}.json"
    response = requests.post(url, auth=oauth)

    if response.status_code != 200:
        print(f"Error while deleting tweet {tweet_id}: {response.status_code}")
    else:
        print(f"Successfully deleted tweet {tweet_id}")

def main():
    # Your UserID - don't think it's needed as already authenticated
    user_id = 'your_user_id'

    try:
        tweets_data = get_tweets(user_id)
        tweet_ids = [tweet["id_str"] for tweet in tweets_data]
        
        for tweet_id in tweet_ids:
            delete_tweet(tweet_id)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
