#!/usr/bin/python3
import os
from os import environ
import sys
import tweepy
from time import sleep
from datetime import datetime
import json
import random
import pytz
import numpy as np
import nltk

from BotStreamListener import BotStreamListener
# import seqbot
import basbot
import quotewidget as qw
import joesixpack as jsp
import twitwidget
import newswidget
import redditwidget2
version = "1.0"

def load_twitter_creds():
    creds = {}
    try:
        creds['consumer_key'] = environ['API_KEY']
        creds['consumer_secret_key'] = environ['API_SECRET_KEY']
        creds['access_token'] = environ['ACCESS_TOKEN']
        creds['access_token_secret'] = environ['ACCESS_TOKEN_SECRET']
    except:
        print("Env not found. Attempting to load AUTH from local file.")
        try:
            import env
            creds['consumer_key'] = env.API_KEY
            creds['consumer_secret_key'] = env.API_SECRET_KEY
            creds['access_token'] = env.ACCESS_TOKEN
            creds['access_token_secret'] = env.ACCESS_TOKEN_SECRET
        except:
            print("Unable to authenticate")
            exit(1)
    return creds

def load_reddit_creds():
    creds = {}
    try:
        creds['client_id'] = environ['REDDIT_CLIENT_ID']
        creds['client_secret'] = environ['REDDIT_CLIENT_SECRET']
    except:
        print("Env not found. Attempting to load Reddit AUTH from local file.")
        try:
            import env
            creds['client_id'] = env.REDDIT_CLIENT_ID
            creds['client_secret'] = env.REDDIT_CLIENT_SECRET
        except:
            print("Unable to authenticate to Reddit")
            exit(1)
    return creds

def load_config():
    c={}
    try:
        c['query_string']=environ['QUERY_STRING']
        c['hashtags']=environ['HASHTAGS'].lower()
        c['min_interval']=int(environ['INTERVAL'])
        c['randmzn']=int(environ['RANDOMIZATION'])
        c['waketime']=int(environ['WAKETIME'])
        c['bedtime']=int(environ['BEDTIME'])
        c['timezone']=environ['TIMEZONE'].lower()
        c['q_pct']=int(environ['QUOTES_PERCENT'])
        c['n_pct']=int(environ['NEWS_PERCENT'])
        c['r_pct']=int(environ['REDDIT_PERCENT'])
        c['subreddit']=environ['SUBREDDIT'].lower()
        c['topic']=environ['NEWS_TOPIC'].lower()
        c['min_pop']=int(environ['MIN_POP'])
        c['character']=environ['CHARACTER'].lower()
        c['mode']=environ['MODE'].lower()
        c['username']=environ['USERNAME'].lower()
        c['userid']=environ['USERID'].lower()
    except:
        print("Config not found. Attempting to load CONFIG from file")
        try:
            import config
            c['query_string']=config.QUERY_STRING
            c['hashtags']=config.HASHTAGS.lower()
            c['min_interval']=int(config.INTERVAL)
            c['randmzn']=int(config.RANDOMIZATION)
            c['waketime']=int(config.WAKETIME)
            c['bedtime']=int(config.BEDTIME)
            c['timezone']=(config.TIMEZONE).lower()
            c['q_pct']=int(config.QUOTES_PERCENT)
            c['n_pct']=int(config.NEWS_PERCENT)
            c['r_pct']=int(config.REDDIT_PERCENT)
            c['subreddit']=config.SUBREDDIT.lower()
            c['topic']=config.NEWS_TOPIC.lower()
            c['min_pop']=int(config.MIN_POP)
            c['character']=config.CHARACTER.lower()
            c['mode']=config.MODE.lower()
            c['username']=config.USERNAME.lower()
            c['userid']=config.USERID.lower()
        except:
            print("Failed to load config")
            exit(1)
        global hashtags
        hashtags = c['hashtags']
    return c

#split list on spaces
def get_item(lis):
    items = lis.split(' ')
    if(len(items)==1):
        return items
    else:
        return random.choice(items)

################################# TIME #################################
def minToSec(mins=1):
    return mins*60

def getHour(timezone):
    tzwc=pytz.timezone(timezone)
    return int(datetime.now(tzwc).hour)

################################# ACTIONS #################################
def tweet_quote(tw):
    tw.tweet(qw.get_update())

def tweet_news(tw,re,topic):
    news = newswidget.get_update(topic)
    if(news):
        new_tweet = """{} {}""".format(re.get_intro(news), hashtags)
        print("Response: ",new_tweet)
        tw.tweet(new_tweet)
    else:
        print('No news is good news')


def tweet_reddit(tw,re,subreddit,hashtags="#news"):
    # print(env)
    rejects = ['reddit.com','redd.it','reddit','nsfw']
    creds = load_reddit_creds()
    max_attempts=5
    attempts = 0
    post = False
    while(not post and attempts < max_attempts):
        attempts += 1
        sr = get_item(subreddit)
        try:
            print("Getting post from subreddit %s. Attempt %d"%(sr, attempts))
            post = redditwidget2.get_update(creds['client_id'],creds['client_secret'],"Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",sr)
            print("Retrieved post:")
            print(post)
            if(not post): raise Exception("Blank Post")
            if any(term in post['url'] for term in rejects):
                raise Exception("Invalid Post")
            else:
                print("Going with reddit post: %s"%(post['title']))
                break
        except Exception as e:
            print(e)
            print("Post is invalid. Trying again.")
            post = False
    if(post):
        tweet_post = """{} {}""".format(post['tweet'][0:260],hashtags)
        print("Tweeting post:  %s"%(tweet_post))
        if(prod): 
            tw.tweet(tweet_post)
        else:
            print(tweet_post)
    else:
        print("Tweeting top tweet instead.")
        tweet_top_tweet(tw,re)

def tweet_top_tweet(tw,re):
    tt = tw.get_top_tweet()
    intro = """{} """.format(re.get_intro(tt.text))[:278]
    print("Tweet Intro: ",intro)
    tw.tweet_comment(tt,intro)

def reply_top_tweet(tw,re):
    tt = tw.get_top_tweet()
    resp = re.get_reply(tt.text)
    print("Tweet %s Response: %s "%(tt.text,resp))
    tw.tweet_reply(tt, resp)

def respond(tw, dm):
    resp = basbot.get_response('default',dm.text)
    print("Responding to message:")
    print("DM %s Response: %s "%(dm.text,resp))
    tw.respond(dm,resp)

########################################## MAIN ##########################################
def main():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitter widget
    print("Initializing Twitter Widget.")
    tw = twitwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],c['query_string'],c['hashtags'])
    #load responder
    re = basbot.responder.Responder()
    #first message check -- get all current messages
    if(prod): tw.check_messages(False)
    #----------------------------- Chat Mode (chat only) ----------------------------------
    if('chat' in c['mode']):
        if(joe.is_awake()):
            print("Responding to DMs")
            if(prod): tw.check_messages(True)
            next_intvl=joe.get_next_interval()
            print("""Time is: {}. Sleeping for {} minutes""".format(getHour(c['timezone']),next_intvl))
            #convert interval to seconds for sleep
            sleep(minToSec(next_intvl))
    #----------------------------- Stream Mode --------------------------------------------
    elif('stream' in c['mode']):
        pass #not implemented yet
    #----------------------------- Interval Mode (default) --------------------------------
    # if('interval' in c['mode']):
    else: #default behavior
        print("Starting default behavior: Interval Mode")
        #start timer
        joe = jsp.Joe(c['timezone'],c['waketime'],c['bedtime'],c['min_interval'],c['randmzn'])
        while True:
            try:
                if(joe.is_awake()):
                    print("Checking for DMs")
                    if(prod): 
                        msgs = tw.check_messages(True)
                        if(msgs):
                            print("Responding ot DMs")
                            for msg in msgs:
                              respond(tw,dm)
                        else:
                            print("No messages")
                    q_beh = int(c['q_pct'])
                    n_beh = q_beh + int(c['n_pct'])
                    r_beh = n_beh + int(c['r_pct'])
                    if( c['q_pct']+c['n_pct'] > 100): 
                        print("Error] Invalid behavior config! Exiting...")
                        exit(1)
                    r = random.randrange(100)
                    if(r < q_beh):
                        print("Tweeting quote")
                        if(prod): tweet_quote(tw)
                    elif(r < n_beh):
                        print("Tweeting news")
                        if(prod): tweet_news(tw,re,c['topic'])
                    elif(r < r_beh):
                        print("Tweeting from reddit")
                        if(prod): tweet_reddit(tw,re,c['subreddit'],c['hashtags'])
                    else:
                    # if(True):
                        #split comments and replies
                        dbeh = random.randrange(100) # the ole 50 / 50
                        if(dbeh < 20): #comment 20% of the time. Else just retweet
                            print("Replying to tweet")
                            if(prod): reply_top_tweet(tw,re)
                        else:
                            print("Commenting on tweet")
                            if(prod): tweet_top_tweet(tw,re)
                next_intvl=joe.get_next_interval()
                print("""Time is: {}. Sleeping for {} minutes""".format(getHour(c['timezone']),next_intvl))
                #convert interval to seconds for sleep
                sleep(minToSec(next_intvl))
                # sleep(minToSec(1))
            except Exception as e:
                print(e)
                print("[Error] Failed to complete action. Sleeping for 15 minutes")
                sleep(minToSec(15))

def test():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitter widget
    tw = twitwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],c['query_string'],c['hashtags'])
    #load responder
    re = basbot.responder.Responder()
    #first message check -- get all current messages
    print("Tweeting from reddit")
    tweet_reddit(tw,re,c['subreddit'],c['hashtags'])

if __name__ == "__main__":
    print("Running Twitter Bot Version %s"%(version))
    global prod
    prod = True
    if(len(sys.argv)>1):
        if('t' in sys.argv[1].lower()):
            prod=False
            print("Running in test mode")
            test()
            exit(0)
    print("Running in prod mode")
    main()
    exit(0)