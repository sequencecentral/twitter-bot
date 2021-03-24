#!/usr/bin/python3
# import init
import os
from os import environ
import tweepy
from time import sleep
import json
import random
import env
import quotes
interval=10
try:
    consumer_key = environ['API_KEY']
    consumer_secret_key = environ['API_SECRET_KEY']
    access_token = environ['ACCESS_TOKEN']
    access_token_secret = environ['ACCESS_TOKEN_SECRET']
    query_string=environ['QUERY_STRING']
    hashtags=environ['HASHTAGS']
    interval=environ['INTERVAL']

except:
    consumer_key = env.API_KEY
    consumer_secret_key = env.API_SECRET_KEY
    access_token = env.ACCESS_TOKEN
    access_token_secret = env.ACCESS_TOKEN_SECRET
    query_string=env.QUERY_STRING
    hashtags=env.HASHTAGS
    interval=env.INTERVAL


#initialize api
def init():
    #setup twitter from env
    global api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    load_intros()

def load_intros():
    global intros
    global emojis
    with open('intro.json') as f:
        intros = json.load(f)['intro']
    with open('intro.json') as f:
        emojis = json.load(f)['emojis']

def get_random_intro():
    # intros = get_intros()
    random_intro = random.choice(intros)
    return random_intro

def get_random_emoji():
    random_emoji = random.choice(emojis)
    return random_emoji

################################# CORE TWITTER FNs #################################
#Tweet with a comment
def tweet_comment(tweet,message):
    # print(tweet)
    new_text = """{} {} {}""".format(message,tweet.text,hashtags)
    api.update_status(new_text)

def get_top_tweet():
    tweets = api.search(q=query_string,rpp=100,count=100,lang='en',RESULT_TYPE='popular')
    # print(tweets)
    pop = [t for t in tweets if int(t.user.followers_count)>1000]
    # for tweet in pop:
        # print("""{} {}""".format(tweet.id,  tweet.user.followers_count))
    rand_pop = random.choice(pop)
    # print("popular tweet:")
    # print("""{} {}""".format(rand_pop.user.followers_count, rand_pop.text))
    return rand_pop

def follow_back_all():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

################################# ADDDON TWITTER FNs #################################
def tweet_random_quote():
    test_tweet = quotes.create_random_tweet()
    api.update_status(test_tweet)

def retweet_top_tweet():
    new_tweet = get_top_tweet()
    intro = """{}{} {} """.format(get_random_emoji(),get_random_emoji(),get_random_intro())
    tweet_comment(new_tweet,intro)
    # print(intro)

def main():
    init()
    mins=60
    while(True):
        print("tweeting")
        retweet_top_tweet()
        sleep(int(interval)*mins)

########################################## MAIN ##########################################
if __name__ == "__main__":
    # init()
    main()
    # tweet_random_quote()