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
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

oauth = OAuth1(CONSUMER_KEY,
               client_secret=CONSUMER_SECRET,
               resource_owner_key=ACCESS_TOKEN,
               resource_owner_secret=ACCESS_TOKEN_SECRET)

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

def get_liked_tweets(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/liked_tweets"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error while getting liked tweets: {response.status_code}")

    return response.json()

def unlike_tweet(tweet_id):
    url = f"https://api.twitter.com/1.1/favorites/destroy.json?id={tweet_id}"
    response = requests.post(url, auth=oauth)

    if response.status_code != 200:
        print(f"Error while unliking tweet {tweet_id}: {response.status_code}")
    else:
        print(f"Successfully unliked tweet {tweet_id}")

def main():
  # Your user ID
    user_id = "123456"

    try:
        liked_tweets_data = get_liked_tweets(user_id)
        liked_tweet_ids = [tweet["id"] for tweet in liked_tweets_data["data"]]

        for tweet_id in liked_tweet_ids:
            unlike_tweet(tweet_id)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
