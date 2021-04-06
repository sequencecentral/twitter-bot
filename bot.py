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
# import basicbot
# from basicbot import responder
import seqbot
import quotewidget as qw
import joesixpack as jsp
import twitterwidget

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
 
########################################## MAIN ##########################################
def main():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitterr widget
    tw = twitterwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],c['query_string'],c['hashtags'])
    #load responder
    re = seqbot.responder.Responder()
    #first message check -- get all current messages
    if(prod): tw.check_messages(False)
    if('interval' in c['mode']):
        #start timer
        joe = jsp.Joe(c['timezone'],c['waketime'],c['bedtime'],c['min_interval'],c['randmzn'])
        while True:
            if(joe.is_awake()):
                print("Responding to DMs")
                if(prod): tw.check_messages(True)
                #randomize action between selected alternatives:
                r = random.randrange(100)
                if(r < c['q_pct']):
                    print("Tweeting quote")
                    if(prod): tw.tweet(qw.get_update())
                else:
                    print("Tweeting top tweet")
                    tt = tw.get_top_tweet()
                    resp = re.get_intro(tt.text)
                    print("Tweet Response: ",resp)
                    if(prod): tw.tweet(resp)
            next_intvl=joe.get_next_interval()
            print("""Time is: {}. Sleeping for {} minutes""".format(getHour(c['timezone']),next_intvl))
            #convert interval to seconds for sleep
            sleep(minToSec(next_intvl))
    #alternative is stream mode--respond instantly
    else:
        pass

if __name__ == "__main__":
    #basic check for test parameter in commandline args
    global prod
    prod = True
    if(len(sys.argv)>1):
        if('t' in sys.argv[1].lower()):
            prod=False
            print('Running in TEST mode')
        else:
            prod=True
            print('Running in PROD mode')
    print('Error chasing #3')
    main()
