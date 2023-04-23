#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 05:36:13 2023
@author: saraheaglesfield
Twitter Block v1.0
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 05:36:13 2023
@author: saraheaglesfield
Twitter Block v1.0
"""
import time
import csv
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import json
import os

#Set these values in your environment using export
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

oauth = OAuth1(CONSUMER_KEY,
               client_secret=CONSUMER_SECRET,
               resource_owner_key=ACCESS_TOKEN,
               resource_owner_secret=ACCESS_TOKEN_SECRET)

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

def read_user_ids_from_csv(file_path):
    user_ids = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            user_ids.append(int(row[0]))
    user_ids.sort(reverse=True)
    return user_ids

def handle_rate_limit(response):
    if response.status_code == 429:
        reset_time = int(response.headers['x-rate-limit-reset'])
        wait_time = reset_time - int(time.time())
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
        time.sleep(wait_time + 1)
        return True
    return False

# Your Twitter ID
id = "12345678"

# Replace this line with the path to your CSV file containing user IDs
csv_file_path = "accounts.csv"

user_ids = read_user_ids_from_csv(csv_file_path)


for target_user_id in user_ids:
    payload = {"target_user_id": str(target_user_id)}
    
    while True:
        oauth = OAuth1Session(CONSUMER_KEY,
               client_secret=CONSUMER_SECRET,
               resource_owner_key=ACCESS_TOKEN,
               resource_owner_secret=ACCESS_TOKEN_SECRET)
        response = oauth.post(
            "https://api.twitter.com/2/users/{}/blocking".format(id), json=payload
        )
        
        if response.status_code != 200:
            print(
                "Error blocking user {}: {} {}".format(
                    target_user_id, response.status_code, response.text
                )
            )
            if not handle_rate_limit(response):
                break
        else:
            print("Successfully blocked user {}".format(target_user_id))
            break
