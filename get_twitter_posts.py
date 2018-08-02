import os

import twitter
import urllib.parse

def find_twitter_handle(brand):
    twitter_file = open("twitter_handles.txt")

    # get the brand name and twitter handle for each brand
    for line in twitter_file:
        line = line.strip().split("|")
        foundation_brand = line[0]
        twitter_handle = line[1]

        # return the twitter handle for that brand
        if foundation_brand == brand:
            twitter_file.close()
            return twitter_handle


def load_tweets(brand):
    """return media for brand's twitter posts"""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    twitter_handle = find_twitter_handle(brand)

    if twitter_handle is None:
        return []
    else:
        results = []
        count = 0

        # keep querying api for media posts until we get 20 media posts, up to a max of 10 queries
        while len(results) < 20 and count < 10:
            if count == 0:
                # the first time we query, there will not be a max id
                response = api.GetUserTimeline(screen_name=twitter_handle[1:], include_rts=False, count=200, exclude_replies=True)
            else:
                # the subsquent times we query, the max id should be set to the oldest post, which will be tweets_lst[-1]
                # the next query will get the prior 200 posts prior to that oldest post
                response = api.GetUserTimeline(screen_name=twitter_handle[1:], max_id=max_id, include_rts=False, count=200, exclude_replies=True)

            tweets_lst = []

            for tweet in response:
                tweets_lst.append(tweet._json)

            # for each twitter post, search for media in the post and add it to the results list
            for status in tweets_lst:
                if "entities" in status:
                    if "media" in status["entities"]:
                        results.append(status["entities"]["media"][0]["media_url"])

            # if there are twitter posts, but less than 20 results, then we should set the max id to the oldest post, and then next time
            # the loop runs it will query starting from the previously oldest post
            if len(tweets_lst) > 1:
                max_id = tweets_lst[-1]["id"]
            # if there is less than or only one tweet, then return what we already have in the results list
            else:
                return results
            # add one to the count to track we do not exceed the 10 query count
            count = count + 1
        return results
