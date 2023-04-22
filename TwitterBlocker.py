from requests_oauthlib import OAuth1Session
import os
import csv
import time

# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# Be sure to replace your-user-id with your own user ID or one of an authenticating user
# You can find a user ID by using the user lookup endpoint
id = "12345678"

# CSV file containing list of user IDs to block
filename = "accounts.csv"

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

# Be sure to replace Access Token & Access Secret
access_token = "134242-dsojKOLKorperksopdmlsdmd;sl"
access_token_secret = "dsl;oOiwpoasmd;lkosegml;kmglsd,l;s,"
print("Got Access token: %s" % resource_owner_key)

# Read user IDs from CSV file
user_ids = []
with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        user_ids.append(row[0])

# Loop over user IDs and block each user
request_count = 0
for target_user_id in user_ids:
    # Rate limit to 50 requests every 15 minutes
    if request_count >= 50:
        print("Waiting 15 minutes for rate limit...")
        time.sleep(900)
        request_count = 0
    
    payload = {"target_user_id": target_user_id}
    # Make the request
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
    else:
        print("Successfully blocked user {}".format(target_user_id))
        request_count += 1
