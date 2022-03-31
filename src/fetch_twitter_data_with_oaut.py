import argparse
import datetime
import time
import json
from pathlib import Path

import tweepy


KEYWORDS = [
    "covid",
    "corona",
    "coronavirus",
    "virus",
    "vaccine",
    "vaccination",
    "moderna",
    "pfizer",
    "biontech",
    '"johnson & johnson"',
    "astrazeneca",
]
GEOCODE = [
    "57.77463501850391,-125.88274093750294,2289.228667656974km",
    "52.31366809992556,-88.24804211924314,2582.529922089856km",
    "39.83145639732886,-113.9527330340418,980.4072063166424km",
    "37.84637109847029,-89.0796861590418,1586.311004075537km",
]
MAX_RESULTS = 100


def parse_args():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Fetch tweets from Twitter API")
    parser.add_argument(
        "-n", "--num_tweets", type=int, default=100, help="Number of tweets to fetch"
    )
    parser.add_argument("-p", "--path", type=str, help="Path to save tweets")
    # Parse arguments
    args = parser.parse_args()
    num_tweets = args.num_tweets
    assert num_tweets > 0, "Number of tweets must be greater than 0"
    assert num_tweets % MAX_RESULTS == 0, f"Number of tweets must be a multiple of {MAX_RESULTS}"
    path = Path(args.path)
    assert path.suffix == ".json", "Path must be a .json file"
    return path, num_tweets


def get_api():
    # Access and consumer identifiers
    ACCESS_TOKEN = "1458990328397058053-1xGoCmIBUFHGfVMXx2VejKoIrCuCr8"
    ACCESS_TOKEN_SECRET = "bnoxeX2dVJ61U2GtHhP6ZRyBkwlfMzOKMkBrTJziwYC1x"
    CONSUMER_KEY = "5L3uNSKzsrloWMERgYn20aOiH"
    CONSUMER_SECRET = "t6P4gZnfNzRxr1mX1n8bMi4MHrQspeDs5qEnYuey3cyXBKEiSQ"
    # Create api
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_search_query():
    # Get keyword string
    keyword_string = "(" + " OR ".join(KEYWORDS) + ")"
    # Get location string
    geocode_string = "(" + " OR ".join([f"geocode:{elt}" for elt in GEOCODE]) + ")"
    # Create query with english language and no retweet filter
    query = f"{keyword_string} AND {geocode_string} AND lang:en AND -filter:retweets"
    return query


def get_n_most_recent_tweets(num_tweets):
    # Get the api
    api = get_api()
    # Get the query
    query = get_search_query()
    # Setup the initial query parameters
    tweet_data = []
    max_id = None
    # Get the tweets
    while len(tweet_data) < num_tweets:
        # Filter for time window in post-processing
        tweets = api.search_tweets(
            q=query,
            count=MAX_RESULTS,
            tweet_mode="extended",  # Get full text rather than truncated
            max_id=max_id,
        )
        if len(tweets) == 0:
            print("No more tweets found, breaking from loop.")
            break
        tweet_data = tweet_data + [tweet._json for tweet in tweets]
        max_id = tweet_data[-1]["id"] - 1
        # Wait 1 second to not overload the server
        time.sleep(1)
    return tweet_data


def write_tweet_data_to_json(tweet_data, path):
    with open(path, "w") as f:
        for tweet_json in tweet_data:
            json.dump(tweet_json, f)
            f.write("\n")


def main():
    # Use argparse to get number of tweets, path and time window
    path, num_tweets = parse_args()
    # Query the Twitter API
    tweet_data = get_n_most_recent_tweets(num_tweets)
    # Create method to save to json
    write_tweet_data_to_json(tweet_data, path)


if __name__ == "__main__":
    main()
