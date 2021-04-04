#!/usr/bin/python3
import os
from os import environ
import sys
import tweepy
from time import sleep
from datetime import datetime
import json
import random
import quotes
import sentiment
import pytz
import numpy as np
import nltk
import steve
import basicbot
from BotStreamListener import BotStreamListener

def auth():
    global api
    try:
        consumer_key = environ['API_KEY']
        consumer_secret_key = environ['API_SECRET_KEY']
        access_token = environ['ACCESS_TOKEN']
        access_token_secret = environ['ACCESS_TOKEN_SECRET']
    except:
        try:
            print("Env not found. Attempting to load AUTH from local file.")
            import env
            consumer_key = env.API_KEY
            consumer_secret_key = env.API_SECRET_KEY
            access_token = env.ACCESS_TOKEN
            access_token_secret = env.ACCESS_TOKEN_SECRET
        except:
            print("Unable to authenticate")
            exit(1)
    t = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    t.set_access_token(access_token, access_token_secret)
    api = tweepy.API(t)
    print("Loaded Twitter API")

def config():
    global query_string
    global hashtags
    global randmzn
    global waketime
    global bedtime
    global q_pct
    global min_pop
    global mode
    global character
    global min_interval
    # min_interval = 1
    global daily_min_interval
    # daily_min_interval = 1
    global username
    global userid
    try:
        query_string=environ['QUERY_STRING']
        hashtags=environ['HASHTAGS'].lower()
        min_interval=int(environ['INTERVAL'])
        randmzn=int(environ['RANDOMIZATION'])
        waketime=int(environ['WAKETIME'])
        bedtime=int(environ['BEDTIME'])
        q_pct=int(environ['QUOTES_PERCENT'])
        min_pop=int(environ['MIN_POP'])
        character=environ['CHARACTER'].lower()
        mode=environ['MODE'].lower()
        username=environ['USERNAME'].lower()
        userid=environ['USERID'].lower()
    except:
        print("Env not found. Attempting to load CONFIG from file")
        try:
            import config
            query_string=config.QUERY_STRING
            hashtags=config.HASHTAGS.lower()
            min_interval=int(config.INTERVAL)
            randmzn=int(config.RANDOMIZATION)
            waketime=int(config.WAKETIME)
            bedtime=int(config.BEDTIME)
            q_pct=int(config.QUOTES_PERCENT)
            min_pop=int(config.MIN_POP)
            character=config.CHARACTER.lower()
            mode=config.MODE.lower()
            username=config.USERNAME.lower()
            userid=config.USERID.lower()
        except:
            print("Failed to load config")
            exit(1)


#initialize api
def init():
    auth()
    config()
    load_intros()
    load_replies()
    load_emojis()
    load_chat()

def load_intros():
    global intros
    with open("""characters/{}.json""".format(character)) as f:
        intros = json.load(f)["retweet"]

def load_replies():
    global replies
    with open("""characters/{}.json""".format(character)) as f:
        replies = json.load(f)["reply"]

def load_emojis():
    global emojis
    with open('emojis.json') as f:
        emojis = json.load(f)

def load_chat():
    global chat
    chat=basicbot.get_chat()

################################# Intros #################################

def get_random_intro():
    random_intro = random.choice(intros["neutral"])
    return random_intro

def get_pos_intro():
    random_intro = random.choice(intros["positive"])
    return random_intro

def get_neg_intro():
    random_intro = random.choice(intros["negative"])
    return random_intro

################################# Replies #################################

def get_random_reply():
    random_reply = random.choice(replies["neutral"])
    return random_reply

def get_pos_reply():
    random_reply = random.choice(replies["positive"])
    return random_reply

def get_neg_reply():
    random_reply = random.choice(replies["negative"])
    return random_reply

################################# Emojis #################################

def get_random_emoji():
    random_emoji = random.choice(emojis["neutral"])
    return random_emoji

def get_pos_emoji():
    random_emoji = random.choice(emojis["positive"])
    return random_emoji

def get_neg_emoji():
    random_emoji = random.choice(emojis["negative"])
    return random_emoji

################################# CORE TWITTER FNs #################################
#Tweet with a comment
def tweet_comment(tweet,message):
    turl = """https://twitter.com/{}/status/{}""".format(tweet.user.id_str,tweet.id)
    new_text = """{} {} {} {}""".format(message,tweet.text,turl,hashtags)
    try:
        if(prod): api.update_status(new_text)
    except:
        print('[Tweet failed]: ',new_text)

def tweet_reply(tweet,message):
    if(prod): api.update_status(status = message, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

def get_top_tweet():
    print(query_string)
    tweets = api.search(q=query_string,rpp=100,count=100,lang='en',RESULT_TYPE='popular')
    # print(tweets)
    pop = [t for t in tweets if int(t.user.followers_count)>min_pop and t.in_reply_to_status_id_str is None]
    # pop = [t for t in tweets if int(t.retweet_count)>min_pop]
    # for tweet in pop:
        # print("""{} {}""".format(tweet.id,  tweet.user.followers_count))
    rand_pop = random.choice(pop)
    # print("popular tweet:")
    # print("""{} {}""".format(rand_pop.user.followers_count, rand_pop.text))
    return rand_pop

################################# ADDDON TWITTER FNs #################################
def tweet_random_quote():
    q = quotes.create_random_tweet()
    if(prod): api.update_status(q)

def retweet_top_tweet():
    print("Retweet top tweet")
    top_tweet = get_top_tweet()
    intro = respond_to_tweet(top_tweet)
    if(prod): tweet_comment(top_tweet,intro)

def reply_top_tweet():
    print("Reply to top tweet")
    top_tweet = get_top_tweet()
    intro = reply_to_tweet(top_tweet)
    if(prod): tweet_reply(top_tweet,intro)

def retweet_respond_top_tweet():
    print("Retweet & reply to top tweet")
    top_tweet = get_top_tweet()
    intro = respond_to_tweet(top_tweet)
    r = reply_to_tweet(top_tweet)
    if(prod): tweet_comment(top_tweet,intro)
    if(prod): tweet_reply(top_tweet,r)

def respond_to_tweet(top_tweet):
    sent = sentiment.get_sentiment(top_tweet.text)
    if 'Positive' in sent:
        intro = """{} {} {} """.format(get_pos_emoji(),get_pos_emoji(),get_pos_intro()["content"])
    elif 'Negative' in sent:
        intro = """{} {} {} """.format(get_neg_emoji(),get_neg_emoji(),get_neg_intro()["content"])
    else:
        intro = """{} {} {} """.format(get_random_emoji(),get_random_emoji(),get_random_intro()["content"])
    print("Tweet Text is: %s"%(top_tweet.text))
    print("Sentiment is %s"%(sent))
    print("Intro: %s"%(intro))
    return intro

def reply_to_tweet(top_tweet):
    sent = sentiment.get_sentiment(top_tweet.text)
    if 'Positive' in sent:
        r = """{} {} {} """.format(get_pos_emoji(),get_pos_reply()["content"],get_pos_emoji())
    elif 'Negative' in sent:
        r = """{} {} """.format(get_neg_emoji(),get_neg_reply()["content"])
    else:
        r = """{} {} {} """.format(get_random_emoji(),get_random_reply()["content"],get_random_emoji())
    print("Tweet Text is: %s"%(top_tweet.text))
    print("Sentiment is %s"%(sent))
    print("Reply: %s"%(r))
    return r

################################# DIRECT MESSAGES #################################
def check_messages(re=False):
    global dm
    messages = api.list_direct_messages()
    for m in messages:
        if m.id not in dm:
            dm[m.id]=m
            if(re & prod): respond(m)

def respond(m):
    t = str(m.message_create['message_data']['text'])
    sender = str(m.message_create['sender_id'])
    r = chat.respond(t)
    print('[Message]: {} [Response:] {}'.format(t,r))
    if(prod): api.send_direct_message(sender, r)

def listen_messages(re=False):
    print('listening to messages')
    botStream = BotStreamListener(on_status_update)
    bs = tweepy.Stream(auth = api.auth, listener=botStream)
    bs.filter(follow=[userid])
    # bs.filter(track='#teamsapnap')
    # bs.on_status(on_status_update)

def on_status_update(status):
    print("status update: ",status.text, status.id_str)
    exit(0)
    # respond(status)

################################# TIME #################################
def minToSec(mins=1):
    return mins*60

def hoursToMins(hrs=1):
    return hrs*60

def hoursToSec(hrs=1):
    return hrs * 60 * 60

def amAwake():
    global wake
    global was_wake
    hour = getHour()
    if hour > waketime and hour < bedtime:
        awake = True
        if(was_wake == False): 
            print('Bot has just woken up.')
            randomize_daily_interval()
        was_wake=awake
        return True
    else:
        print("Am asleep. Zzzz...")
        awake = False
        was_wake=awake
        return False

def randomize_daily_interval():
    global daily_min_interval
    spread = min_interval*10/100
    rng = np.random.default_rng(); 
    n = rng.normal(min_interval,spread,1000)
    daily_min_interval = abs(round(random.choice(n)))
    print("Daily time interval %s has been randomized to: %s minutes"%(min_interval, daily_min_interval))

def randomizeInterval(ti=10,randomization=1):
    spread = ti*randomization/100
    # t = abs(round(random.uniform(ti-spread,ti+spread)))
    # return t
    rng = np.random.default_rng(); 
    n = rng.normal(ti,spread,1000)
    rand_unit = abs(round(random.choice(n))) #use randomized increment as unit
    #For Poisson distribution
    # p = rng.poisson(1, 100) #poisson dist with lambda 1 -- select random value & multiply it
    # multiplier = random.choice(p)+1
    # ri = multiplier*rand_unit
    return rand_unit

def getHour():
    tzwc=pytz.timezone('America/Los_Angeles')
    return int(datetime.now(tzwc).hour)

def getTimeInterval(mins=10,spread=1):
    curr_hour = getHour()
    rand_60m=randomizeInterval(60,spread)
    if(amAwake()):
        return randomizeInterval(mins,spread)
    else: #return sleep interval to next waketime
        if(curr_hour < waketime):  #if before waketime, subtract current hour i.e., 5AM - 3AM = 2 hrs & also randomize wake time by 10%
            return hoursToMins(waketime - curr_hour-1)+rand_60m
        else: #if after waketime then must be evening
            return hoursToMins(24 - bedtime + waketime - curr_hour)+rand_60m

########################################## MAIN ##########################################
def main():
    init()
    print('Loaded bot at:',getHour())
    randomize_daily_interval()
    print('Loading any existing messages for this account.')
    check_messages(False)
    #interval mode: perform behaviors in between sleep intervals
    if('interval' in mode):
        while(True):
            init()
            # respond_to_messages()
            print('Checking for any new messages')
            check_messages(prod)
            #randomize behaviors by percentages
            r = random.randrange(100)
            if(r < q_pct ):
                print('tweet quote')
                tweet_random_quote()
            else:
                print('tweeting')
                retweet_top_tweet()
            next_intvl=getTimeInterval(daily_min_interval,randmzn)
            print("""Time is: {}. Sleeping for {} minutes""".format(getHour(),next_intvl))
            sleep(minToSec(next_intvl))
        #continuous mode: perform behaviors continuously
    elif('stream' in mode):
        print('Continuous Mode')
        while(True):
            listen_messages(True)

dm={}
prod=True
awake = True
was_wake = True

try:
    if('t' in sys.argv[1].lower()):
        prod=False
        print('Running in TEST mode')
        print(sys.argv)
except:
    prod=True
    print('Running in PROD mode')

if __name__ == "__main__":
    main()