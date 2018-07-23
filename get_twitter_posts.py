import os

import twitter
import urllib.parse

def load_tweets(brand):

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    brand = urllib.parse.quote(brand)

    results = api.GetSearch(raw_query="q={}&until=2018-07-22&count=100&qf=on&filter=safe".format(brand))

    return results
