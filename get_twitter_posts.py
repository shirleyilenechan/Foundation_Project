import os

import twitter
import urllib.parse

def load_tweets(brand):

    print(brand)

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    twitter_file = open("twitter_handles.txt")

    for line in twitter_file:
        line = line.strip().split("|")
        foundation_brand = line[0]
        twitter_handle = line[1]

        if foundation_brand == brand:
            results = []
            count = 0

            while len(results) < 20 and count < 10:
                if count == 0:
                    response = api.GetUserTimeline(screen_name=twitter_handle[1:], include_rts=False, count=200, exclude_replies=True)
                else:
                    response = api.GetUserTimeline(screen_name=twitter_handle[1:], max_id=max_id, include_rts=False, count=200, exclude_replies=True)

                tweets_lst = []

                for tweet in response:
                    tweets_lst.append(tweet._json)

                for status in tweets_lst:
                    if "entities" in status:
                        if "media" in status["entities"]:
                            results.append(status["entities"]["media"][0]["media_url"])

                max_id = tweets_lst[-1]["id"]

                count = count + 1

            return results
