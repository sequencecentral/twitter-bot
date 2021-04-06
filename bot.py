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
import basicbot
from basicbot import responder
import quotewidget as qw
import joesixpack as jsp
import twitterwidget

def load_twitter_creds():
    creds = {}
    try:
        cred['consumer_key'] = environ['API_KEY']
        cred['consumer_secret_key'] = environ['API_SECRET_KEY']
        cred['access_token'] = environ['ACCESS_TOKEN']
        cred['access_token_secret'] = environ['ACCESS_TOKEN_SECRET']
    except:
        try:
            print("Env not found. Attempting to load AUTH from local file.")
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
    re = basicbot.Responder()
    #first message check -- get all current messages
    if(prod): tw.check_messages(False)
    #starrt timer
    joe = jsp.Joe(c['timezone'],c['waketime'],c['bedtime'],c['min_interval'],c['randmzn'])
    if('interval' in c['mode']):
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
    try:
        global prod
        if('t' in sys.argv[1].lower()):
            prod=False
            print('Running in TEST mode')
            # print(sys.argv)
    except:
        prod=True
        print('Running in PROD mode')
    main()

    # init()
    # print(joe.get_next_interval())
    # print(qw.get_update())
    # pass
    # import env
    # consumer_key = env.API_KEY
    # consumer_secret_key = env.API_SECRET_KEY
    # access_token = env.ACCESS_TOKEN
    # access_token_secret = env.ACCESS_TOKEN_SECRET
    # t = tw.TwitterWidget(consumer_key,consumer_secret_key,access_token,access_token_secret)
    # t.config("#bitcoin","#bitcoin")
    # print("Configured")
    # print("Get top tweet:")
    # tt=t.get_top_tweet()
    # print(tt.text)

# def old_main():
#     global dm
#     dm={}
#     global prod
#     prod=True
#     init()
#     print('Loaded bot at:',getHour())
#     # randomize_daily_interval()
#     print('Loading any existing messages for this account.')
#     check_messages(False)
#     #interval mode: perform behaviors in between sleep intervals
#     if('interval' in mode):
#         # tweet_random_quote()
#         while(True):
#             init()
#             # respond_to_messages()
#             print('Checking for any new messages')
#             check_messages(prod)
#             #randomize behaviors by percentages
#             r = random.randrange(100)
#             if(r < q_pct ):
#                 print('tweet quote')
#                 tweet_random_quote()
#             else:
#                 print('tweeting')
#                 retweet_top_tweet()
#             # next_intvl=getTimeInterval(daily_min_interval,randmzn)
#             next_intvl=joe.get_next_interval()
#             print("""Time is: {}. Sleeping for {} minutes""".format(getHour(),next_intvl))
#             sleep(minToSec(next_intvl))
#         #continuous mode: perform behaviors continuously
#     elif('stream' in mode):
#         print('Continuous Mode')
#         while(True):
#             listen_messages(True)


# def load_intros():
#     global intros
#     with open("""characters/{}.json""".format(character)) as f:
#         intros = json.load(f)["retweet"]

# def load_replies():
#     global replies
#     with open("""characters/{}.json""".format(character)) as f:
#         replies = json.load(f)["reply"]

# def load_emojis():
#     global emojis
#     with open('emojis.json') as f:
#         emojis = json.load(f)

# def load_chat():
#     global chat
#     chat=basicbot.get_chat()

# ################################# Intros #################################
# def get_random_intro():
#     random_intro = random.choice(intros["neutral"])
#     return random_intro

# def get_pos_intro():
#     random_intro = random.choice(intros["positive"])
#     return random_intro

# def get_neg_intro():
#     random_intro = random.choice(intros["negative"])
#     return random_intro

# ################################# Replies #################################
# def get_random_reply():
#     random_reply = random.choice(replies["neutral"])
#     return random_reply

# def get_pos_reply():
#     random_reply = random.choice(replies["positive"])
#     return random_reply

# def get_neg_reply():
#     random_reply = random.choice(replies["negative"])
#     return random_reply

# ################################# Emojis #################################
# def get_random_emoji():
#     random_emoji = random.choice(emojis["neutral"])
#     return random_emoji

# def get_pos_emoji():
#     random_emoji = random.choice(emojis["positive"])
#     return random_emoji

# def get_neg_emoji():
#     random_emoji = random.choice(emojis["negative"])
#     return random_emoji

# ################################# CORE TWITTER FNs #################################
# #Tweet with a comment
# def tweet_comment(tweet,message):
#     turl = """https://twitter.com/{}/status/{}""".format(tweet.user.id_str,tweet.id)
#     new_text = """{} {} {} {}""".format(message,tweet.text,turl,hashtags)
#     try:
#         if(prod): api.update_status(new_text)
#     except:
#         print('[Tweet failed]: ',new_text)

# def tweet_reply(tweet,message):
#     if(prod): api.update_status(status = message, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

# def get_top_tweet():
#     print(query_string)
#     tweets = api.search(q=query_string,rpp=100,count=100,lang='en',RESULT_TYPE='popular')
#     # print(tweets)
#     pop = [t for t in tweets if int(t.user.followers_count)>min_pop and t.in_reply_to_status_id_str is None]
#     # pop = [t for t in tweets if int(t.retweet_count)>min_pop]
#     # for tweet in pop:
#         # print("""{} {}""".format(tweet.id,  tweet.user.followers_count))
#     rand_pop = random.choice(pop)
#     # print("popular tweet:")
#     # print("""{} {}""".format(rand_pop.user.followers_count, rand_pop.text))
#     return rand_pop

# ################################# ADDDON TWITTER FNs #################################
# def tweet_random_quote():
#     q = qw.get_update()
#     if(prod): api.update_status(q)

# def retweet_top_tweet():
#     print("Retweet top tweet")
#     top_tweet = get_top_tweet()
#     intro = respond_to_tweet(top_tweet)
#     if(prod): tweet_comment(top_tweet,intro)

# def reply_top_tweet():
#     print("Reply to top tweet")
#     top_tweet = get_top_tweet()
#     intro = reply_to_tweet(top_tweet)
#     if(prod): tweet_reply(top_tweet,intro)

# def retweet_respond_top_tweet():
#     print("Retweet & reply to top tweet")
#     top_tweet = get_top_tweet()
#     intro = respond_to_tweet(top_tweet)
#     r = reply_to_tweet(top_tweet)
#     if(prod): tweet_comment(top_tweet,intro)
#     if(prod): tweet_reply(top_tweet,r)

# def respond_to_tweet(top_tweet):
#     sent = sentiment.get_sentiment(top_tweet.text)
#     if 'Positive' in sent:
#         intro = """{} {} {} """.format(get_pos_emoji(),get_pos_emoji(),get_pos_intro()["content"])
#     elif 'Negative' in sent:
#         intro = """{} {} {} """.format(get_neg_emoji(),get_neg_emoji(),get_neg_intro()["content"])
#     else:
#         intro = """{} {} {} """.format(get_random_emoji(),get_random_emoji(),get_random_intro()["content"])
#     print("Tweet Text is: %s"%(top_tweet.text))
#     print("Sentiment is %s"%(sent))
#     print("Intro: %s"%(intro))
#     return intro

# def reply_to_tweet(top_tweet):
#     sent = sentiment.get_sentiment(top_tweet.text)
#     if 'Positive' in sent:
#         r = """{} {} {} """.format(get_pos_emoji(),get_pos_reply()["content"],get_pos_emoji())
#     elif 'Negative' in sent:
#         r = """{} {} """.format(get_neg_emoji(),get_neg_reply()["content"])
#     else:
#         r = """{} {} {} """.format(get_random_emoji(),get_random_reply()["content"],get_random_emoji())
#     print("Tweet Text is: %s"%(top_tweet.text))
#     print("Sentiment is %s"%(sent))
#     print("Reply: %s"%(r))
#     return r

# ################################# DIRECT MESSAGES #################################
# def check_messages(re=False):
#     global dm
#     messages = api.list_direct_messages()
#     for m in messages:
#         if m.id not in dm:
#             dm[m.id]=m
#             if(re & prod): respond(m)

# def respond(m):
#     t = str(m.message_create['message_data']['text'])
#     sender = str(m.message_create['sender_id'])
#     r = chat.respond(t)
#     print('[Message]: {} [Response:] {}'.format(t,r))
#     if(prod): api.send_direct_message(sender, r)

# def listen_messages(re=False):
#     print('listening to messages')
#     botStream = BotStreamListener(on_status_update)
#     bs = tweepy.Stream(auth = api.auth, listener=botStream)
#     bs.filter(follow=[userid])
#     # bs.filter(track='#teamsapnap')
#     # bs.on_status(on_status_update)

# def on_status_update(status):
#     print("status update: ",status.text, status.id_str)
#     exit(0)
#     # respond(status)