#!/usr/bin/python3
import os
from os import environ
import tweepy
from time import sleep
from datetime import datetime
import json
import random
import quotes
import sentiment
import pytz
import numpy as np

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

def config():
    global api
    global query_string
    global hashtags
    global min_interval
    global randmzn
    global waketime
    global bedtime
    global q_pct
    global min_pop
    global character
    try:
        query_string=environ['QUERY_STRING']
        hashtags=environ['HASHTAGS']
        min_interval=int(environ['INTERVAL'])
        randmzn=int(environ['RANDOMIZATION'])
        waketime=int(environ['WAKETIME'])
        bedtime=int(environ['BEDTIME'])
        q_pct=int(environ['QUOTES_PERCENT'])
        min_pop=int(environ['MIN_POP'])
        character=environ['CHARACTER']
    except:
        print("Env not found. Attempting to load CONFIG from file")
        try:
            import config
            query_string=config.QUERY_STRING
            hashtags=config.HASHTAGS
            min_interval=int(config.INTERVAL)
            randmzn=int(config.RANDOMIZATION)
            waketime=int(config.WAKETIME)
            bedtime=int(config.BEDTIME)
            q_pct=int(config.QUOTES_PERCENT)
            min_pop=int(config.MIN_POP)
            character=config.CHARACTER
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

################################# Intros #################################

def get_random_intro():
    # intros = get_intros()
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
    # replys = get_replys()
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
    # print(tweet)
    turl = """https://twitter.com/{}/status/{}""".format(tweet.user.id_str,tweet.id)
    new_text = """{} {} {} {}""".format(message,tweet.text,turl,hashtags)
    api.update_status(new_text)

def tweet_reply(tweet,message):
    api.update_status(status = message, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

def get_top_tweet():
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
    test_tweet = quotes.create_random_tweet()
    api.update_status(test_tweet)

def retweet_top_tweet():
    print("Retweet top tweet")
    top_tweet = get_top_tweet()
    intro = respond_to_tweet(top_tweet)
    tweet_comment(top_tweet,intro)

def reply_top_tweet():
    print("Reply to top tweet")
    top_tweet = get_top_tweet()
    intro = reply_to_tweet(top_tweet)
    tweet_reply(top_tweet,intro)

def retweet_respond_top_tweet():
    print("Retweet & reply to top tweet")
    top_tweet = get_top_tweet()
    intro = respond_to_tweet(top_tweet)
    r = reply_to_tweet(top_tweet)
    tweet_comment(top_tweet,intro)
    tweet_reply(top_tweet,r)

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
################################# TIME #################################
def minToSec(mins=1):
    return mins*60

def hoursToMins(hrs=1):
    return hrs*60

def hoursToSec(hrs=1):
    return hrs * 60 * 60

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

def amAwake():
    hour = getHour()
    if hour > waketime and hour < bedtime:
        return True
    else:
        print("Am asleep. Zzzz...")
        return False

def getTimeInterval(mins=10,spread=1):
    curr_hour = getHour()
    rand_60m=randomizeInterval(60,spread)
    if(amAwake()):
        return randomizeInterval(mins,spread)
    # else:
        # return 2
    else: #return sleep interval to next waketime
        if(curr_hour < waketime):  #if before waketime, subtract current hour i.e., 5AM - 3AM = 2 hrs & also randomize wake time by 10%
            return hoursToMins(waketime - curr_hour-1)+rand_60m
        else: #if after waketime then must be evening
            return hoursToMins(24 - bedtime + waketime -1)+rand_60m

########################################## MAIN ##########################################
def main():
    # init()
    # retweet_top_tweet()
    while(True):
        # print(get_random_emoji())
        init()
        #randomize behaviors by percentages
        r = random.randrange(100)
        if(r < q_pct ):
            print('tweet quote')
            tweet_random_quote()
            # try:
            # except:
            #     print("Error tweeting random quote")
        # elif(r < q_pct+50):
        else:
            print('tweeting')
            retweet_top_tweet()
            # retweet_respond_top_tweet()
            # try:
            # except:
            #     print("Error retweeting top tweet")
        next_intvl=getTimeInterval(min_interval,randmzn)
        print("""Time is: {}. Sleeping for {} minutes""".format(getHour(),next_intvl))
        sleep(minToSec(next_intvl))

if __name__ == "__main__":
    main()