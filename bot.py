#!/usr/bin/python
# import init
# import os
from os import environ
import tweepy
import json
import random
from scanner import Scanner
QUERY_STRING = os.getenv("QUERY_STRING")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")

def init():
    #setup twitter from env
    print(QUERY_STRING)
    api = ""
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

def get_quotes():
    with open('data.json') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def create_random_tweet():
    quote = get_random_quote()
    tweet = """
            {}
            ~{}
            """.format(quote['quote'], quote['character'])
    return tweet

def get_random_quote():
    quotes = get_quotes()
    random_quote = random.choice(quotes)
    return random_quote

def tweet_random_quote():
    test_tweet = create_random_tweet()
    api.update_status(test_tweet)

#Tweet with a comment
def tweet_comment(tweet,message):
    print(tweet)
    pass

def main():
    # tweet_random_quote()
    status = 'original status'
    print(status)

    new_status = """Check this out: {original}
    """.format(original=status)
    print(new_status)
    # myScanner=Scanner(api)
    # myScanner.onTweet(lambda x: print(x))

########################################## MAIN ##########################################
if __name__ == "__main__":
    init()
    main()
    # tweet_random_quote()