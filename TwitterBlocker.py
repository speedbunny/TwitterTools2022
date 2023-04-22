#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 05:36:13 2023
@author: saraheaglesfield
"""
import time
import csv
from requests_oauthlib import OAuth1Session
import os

def read_user_ids_from_csv(file_path):
    user_ids = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            user_ids.append(row[0])
    return user_ids

def handle_rate_limit(response):
    if response.status_code == 429:
        reset_time = int(response.headers['x-rate-limit-reset'])
        wait_time = reset_time - int(time.time())
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
        time.sleep(wait_time + 1)

# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# Be sure to replace your-user-id with your own user ID or one of an authenticating user
# You can find a user ID by using the user lookup endpoint
id = "123435"

# Replace this line with the path to your CSV file containing user IDs
csv_file_path = "/Volumes/Data/accounts.csv"

user_ids = read_user_ids_from_csv(csv_file_path)

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("There may have been an issue with the consumer_key or consumer_secret you entered.")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Be sure to replace with your own access_token
access_token = "15232443-dssgdssdsgdss"
access_token_secret = "bsdsdsddsssG"
print("Got Access token: %s" % resource_owner_key)


for target_user_id in user_ids:
    payload = {"target_user_id": target_user_id}
    
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    response = oauth.post(
        "https://api.twitter.com/2/users/{}/blocking".format(id), json=payload
    )
    
    if response.status_code != 200:
        print(
            "Error blocking user {}: {} {}".format(
                target_user_id, response.status_code, response.text
            )
        )
        handle_rate_limit(response)
    else:
        print("Successfully blocked user {}".format(target_user_id))
