import argparse
from pathlib import Path
import os
import datetime
import time

import pandas as pd
import tweepy


TWEET_FIELDS = ["id", "text", "author_id", "created_at", "geo"]
MAX_RESULTS = 100


def parse_args():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Fetch tweets from Twitter API")
    # parser.add_argument(
    #     "-n", "--num_tweets", type=int, default=100, help="Number of tweets to fetch"
    # )
    parser.add_argument("-p", "--path", type=str, help="Path to save tweets")
    parser.add_argument("-t", "--time_window", type=int, default=3, help="Time window in days")
    # Parse arguments
    args = parser.parse_args()
    # num_tweets = args.num_tweets
    # assert num_tweets > 0, "Number of tweets must be greater than 0"
    path = Path(args.path)
    assert path.suffix == ".csv", "Path must be a .csv file"
    time_window = args.time_window
    return path, time_window


def get_bearer_token():
    bearer_token = "AAAAAAAAAAAAAAAAAAAAABAzWAEAAAAAhwRIcVi74Vls5vPatzUbIp8Po38%3DN0vbKrA26Ta8D682G5XEn2kzbAVH5rRqH8kEqXSUFTLBbueWO3"
    return bearer_token


def get_search_query():
    # Search query
    query = """(covid OR corona OR coronavirus OR virus OR vaccine
                OR vaccination OR moderna OR pfizer OR biontech
                OR "johnson & johnson" OR astrazeneca) 
                -is:retweet lang:en"""
    return query


def get_most_recent_tweets(time_window):
    # Set up the api connection
    bearer_token = get_bearer_token()
    client = tweepy.Client(bearer_token=bearer_token)
    # Get the query
    query = get_search_query()
    # Setup the initial query parameters
    current_utc_times = datetime.datetime.utcnow()
    delta = datetime.timedelta(days=time_window)
    start_time = (current_utc_times - delta).isoformat()
    query_params = {
        "tweet_fields": TWEET_FIELDS,
        "max_results": MAX_RESULTS,
        "until_id": None,
        # "start_time": start_time,
    }
    tweet_data = []
    # Get the tweets
    while len(tweet_data) < 1000:
        # TODO: No geo location right now and not using time window
        tweets = client.search_recent_tweets(query=query, **query_params)
        tweet_data = [*tweet_data, *tweets.data]
        query_params["until_id"] = tweets.data[-1].id
    return tweet_data


def write_tweet_data_to_csv(tweet_data, path):
    # Start with dict for dataframe
    dataframe_dict = {}
    for field in TWEET_FIELDS:
        dataframe_dict[field] = [tweet.data.get(field, "na") for tweet in tweet_data]
    # Convert to dataframe
    df = pd.DataFrame(data=dataframe_dict)
    # Write to csv
    df.to_csv(path)


def main():
    # Use argparse to get number of tweets, path and time window
    path, time_window = parse_args()
    time_window = 3
    # Query the Twitter API
    tweet_data = get_most_recent_tweets(time_window)
    # Create method to save to json
    write_tweet_data_to_csv(tweet_data, path)


if __name__ == "__main__":
    main()
