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
import basicbot as basbot
import quotewidget as qw
# import joesixpack as jsp
import averagejoe as jsp
import twitterwidget
import newswidget
import redditwidget
import pubmedwidget
import rsswidget
import udemywidget
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
        c['tc_pct']=int(environ['TECHCRUNCH_PERCENT'])
        c['ts_pct']=int(environ['TECHSTARTUP_PERCENT'])
        c['udemy_pct']=int(environ['UDEMY_PERCENT'])
        c['genomics_pct']=int(environ['GENOMICS_PERCENT'])
        c['covid19_pct']=int(environ['COVID19_PERCENT'])
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
            c['tc_pct']=int(config.TECHCRUNCH_PERCENT)
            c['ts_pct']=int(config.TECHSTARTUP_PERCENT)
            c['udemy_pct']=int(config.UDEMY_PERCENT)
            c['genomics_pct']=int(config.GENOMICS_PERCENT)
            c['covid19_pct']=int(config.COVID19_PERCENT)
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
        return items[0]
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
    try:
        tw.tweet(qw.get_update())
    except Exception as e:
        print(e)
        print("Unable to tweet")

def tweet_news(tw,re,topic):
    news = newswidget.get_update(topic)
    if(news):
        htags = basbot.tag_it(news,hashtags)
        new_tweet = """{} {}""".format(re.get_intro(news), htags)
        print("Response: ",new_tweet)
        try:
            tw.tweet(new_tweet)
            return
        except Exception as e:
            print(e)
            print("Unable to tweet news.")
    else:
        print('No news is good news')
    tweet_top_tweet(tw,re)

def tweet_pubmed(tw,re,feed_name):
    try:
        ref = rsswidget.get_update(feed_name)
        print("Retrieved tweet from pubmed %s"%(ref['tweet']))
        htags = basbot.tag_it(ref['title'],"#science")
        tweet_post = """{} {}""".format(ref['tweet'],htags)
        print("Tweeting post:  %s"%(tweet_post))
        tw.tweet(tweet_post)
    except Exception as e:
        print(e)
        print("Unable to get genomics update")
        tweet_top_tweet(tw,re)

def tweet_genomics(tw,re):
    tweet_pubmed(tw,re,'genomics')

def tweet_covid19(tw,re):
    tweet_pubmed(tw,re,'covid19')

def tweet_rss(tw,re,feed_name):
    try:
        ref = rsswidget.get_update(feed_name)
        print("Retrieved tweet from RSS %s"%(ref['tweet']))
        htags = basbot.tag_it(ref['title'],"#news")
        tweet_post = """{} {}""".format(ref['tweet'],htags)
        print("Tweeting post:  %s"%(tweet_post))
        tw.tweet(tweet_post)
    except Exception as e:
        print(e)
        print("Unable to tweet RSS %s"%(feed_name))
        tweet_top_tweet(tw,re)

def tweet_techcrunch(tw,re):
    tweet_rss(tw,re,"techcrunch")

def tweet_techstartups(tw,re):
    tweet_rss(tw,re,"startups")

def tweet_reddit(tw,re,subreddit,hashtags="#news"):
    rejects = ['reddit.com','redd.it','reddit','nsfw','redd','red']
    creds = load_reddit_creds()
    ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
    try:
        #             print(get_update(env.client_id,env.client_secret,env.user_agent,"science"))
        post = redditwidget.get_update(creds['client_id'],creds['client_secret'],ua,subreddit)
        print("Tagging post")
        add_tags = basbot.tag_it(post['title'],hashtags)
        tweet_post = """{} {}""".format(post['tweet'],add_tags)
        print("Tweeting post:  %s"%(tweet_post))
        if(prod): tw.tweet(tweet_post)
    except Exception as e:
        print(e)
        print("Unable to tweet post")
        print("Tweeting top tweet instead.")
        if(prod): tweet_top_tweet(tw,re,hashtags)

def tweet_udemy(tw,re):
    creds = load_reddit_creds()
    try:
        udemy = udemywidget.get_update(creds['client_id'],creds['client_secret'],"Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0","udemyfreebies")
        print("Tweeting Udemy: %s"%(udemy['tweet']))
        #tweets come pre-tagged
        tw.tweet(udemy['tweet'])
    except Exception as e:
        print(e)
        print("Unable to tweet.")

def tweet_top_tweet(tw,re,hashtags="#news"):
    tt = tw.get_top_tweet()
    htags = basbot.tag_it(tt.text,hashtags)
    intro = """{}""".format(re.get_intro(tt.text))[:278]
    print("Tweet Intro: ",intro)
    try:
        tw.tweet_comment(tt,intro,htags)
    except Exception as e:
        print(e)
        print("Unable to tweet.")

def reply_top_tweet(tw,re):
    tt = tw.get_top_tweet()
    resp = re.get_reply(tt.text)
    print("Tweet %s Response: %s "%(tt.text,resp))
    try:
        tw.tweet_reply(tt, resp)
    except Exception as e:
        print(e)
        print("Unable to tweet.")

def respond(tw, dm):
    resp = basbot.get_response('default',dm.text)
    print("Responding to message:")
    print("DM %s Response: %s "%(dm.text,resp))
    try:
        tw.respond(dm,resp)
    except Exception as e:
        print(e)
        print("Unable to send response")

########################################## MAIN ##########################################
def main():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitter widget
    print("Initializing Twitter Widget.")
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
                    genomics_beh = r_beh + int(c['genomics_pct'])
                    covid19_beh = genomics_beh + int(c['covid19_pct'])
                    tc_beh = covid19_beh + int(c['tc_pct'])
                    ts_beh = tc_beh + int(c['ts_pct'])
                    udemy_beh = ts_beh + int(c['udemy_pct'])
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
                    elif(r < genomics_beh):
                        print("Tweeting Genomics")
                        if(prod): tweet_genomics(tw,re)
                    elif(r < covid19_beh):
                        print("Tweeting COVID19")
                        if(prod): tweet_covid19(tw,re)
                    elif(r < tc_beh):
                        print("TechCrunch")
                        if(prod): tweet_techcrunch(tw,re)
                    elif(r < ts_beh):
                        print("TechStartups")
                        if(prod):tweet_techstartups(tw,re)
                    elif(r < udemy_beh):
                        print("Tweeting Udemy")
                        if(prod):tweet_udemy(tw,re)
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
                # sleep(minToSec(1))
            except Exception as e:
                print(e)
                print("[Error] Failed to complete action. Sleeping for 15 minutes")
                sleep(minToSec(15))

def test():
    c=load_config()
    auth = load_twitter_creds()
    #initialize twitter widget
    tw = twitterwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],c['query_string'],c['hashtags'])
    #load responder
    re = basbot.responder.Responder()
    #Test specific functions here:
    # tweet_reddit(tw,re,c['subreddit'],c['hashtags'])
    tweet_reddit(tw,re,"technology")
    # tweet_genomics(tw,re)
    # tweet_covid19(tw,re)
    # tweet_udemy(tw,re)

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