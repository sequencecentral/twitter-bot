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
import twitterwidget
import newswidget

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
            c['topic']=config.NEWS_TOPIC.lower()
            c['min_pop']=int(config.MIN_POP)
            c['character']=config.CHARACTER.lower()
            c['mode']=config.MODE.lower()
            c['username']=config.USERNAME.lower()
            c['userid']=config.USERID.lower()
        except:
            print("Failed to load config")
            exit(1)
    return c

################################# TIME #################################
def minToSec(mins=1):
    return mins*60

def getHour(timezone):
    tzwc=pytz.timezone(timezone)
    return int(datetime.now(tzwc).hour)

################################# ACTIONS #################################
def tweet_news(tw,re,topic,hashtags):
    news = newswidget.get_update(topic)
    new_tweet = """{} {}""".format(re.get_intro(news), hashtags)
    print("Response: ",new_tweet)
    tw.tweet(new_tweet)

def tweet_top_tweet(tw,re,hashtags):
    tt = tw.get_top_tweet()
    new_tweet = """{} {}""".format(re.get_intro(tt.text), hashtags)
    print("Tweet Intro: ",new_tweet)
    tw.tweet(new_tweet)

def reply_top_tweet(tw,re):
    tt = tw.get_top_tweet()
    resp = re.get_reply(tt.text)
    print("Tweet %s Response: %s "%(tw.text,resp))
    tw.tweet_reply(tt, resp)
    # tw.tweet(resp)
########################################## MAIN ##########################################
def main():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitter widget
    tw = twitterwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],c['query_string'],c['hashtags'])
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
                    print("Responding to DMs")
                    if(prod): tw.check_messages(True)
                    #randomize action between selected alternatives, calculate cumulative percentages:
                    q_beh = c['q_pct']
                    n_beh =  c['q_pct']+c['n_pct']
                    if( c['q_pct']+c['n_pct'] > 100): 
                        print("[error] Invalid behavior config! Exiting...")
                        exit(1)
                    r = random.randrange(100)
                    if(r < q_beh):
                        print("Tweeting quote")
                        if(prod): tw.tweet(qw.get_update())
                    elif(r < n_beh):
                        print("Tweeting news")
                        if(prod): tweet_news(tw,re,c['topic'],c['hashtags'])
                    else:
                        dbeh = random.randrange(100) # the ole 50 / 50
                        if(dbeh < 20): #comment 20% of the time. Else just retweet
                            print("Replying to tweet")
                            if(prod): reply_top_tweet(tw,re)
                        else:
                            print("Commenting on tweet")
                            if(prod): tweet_top_tweet(tw,re,c['hashtags'])
                next_intvl=joe.get_next_interval()
                print("""Time is: {}. Sleeping for {} minutes""".format(getHour(c['timezone']),next_intvl))
                #convert interval to seconds for sleep
                sleep(minToSec(next_intvl))
            except:
                print("[Error] Failed to complete action. Sleeping for 30 minutes")
                sleep(minToSec(30))

if __name__ == "__main__":
    #basic check for test parameter in commandline args
    global prod
    prod = True
    if(len(sys.argv)>1):
        if('t' in sys.argv[1].lower()):
            prod=False
        else:
            prod=True
    main()
    # print(dir(newswidget))
    # news = newswidget.get_update('cybersecurity')
    # print(news)
