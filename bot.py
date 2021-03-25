#!/usr/bin/python3
import os
from os import environ
import tweepy
from time import sleep
from datetime import datetime
import json
import random
import quotes
try:
    consumer_key = environ['API_KEY']
    consumer_secret_key = environ['API_SECRET_KEY']
    access_token = environ['ACCESS_TOKEN']
    access_token_secret = environ['ACCESS_TOKEN_SECRET']
    query_string=environ['QUERY_STRING']
    hashtags=environ['HASHTAGS']
    min_interval=int(environ['INTERVAL'])
    randmzn=int(environ['RANDOMIZATION'])
    waketime=int(environ['WAKETIME'])
    bedtime=int(environ['BEDTIME'])
    q_pct=int(environ['QUOTES_PERCENT'])

except:
    import env
    consumer_key = env.API_KEY
    consumer_secret_key = env.API_SECRET_KEY
    access_token = env.ACCESS_TOKEN
    access_token_secret = env.ACCESS_TOKEN_SECRET
    query_string=env.QUERY_STRING
    hashtags=env.HASHTAGS
    min_interval=int(env.INTERVAL)
    randmzn=int(env.RANDOMIZATION)
    waketime=int(env.WAKETIME)
    bedtime=int(env.BEDTIME)
    q_pct=int(env.QUOTES_PERCENT)

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

################################# ADDDON TWITTER FNs #################################
def tweet_random_quote():
    test_tweet = quotes.create_random_tweet()
    api.update_status(test_tweet)

def retweet_top_tweet():
    new_tweet = get_top_tweet()
    intro = """{}{} {} """.format(get_random_emoji(),get_random_emoji(),get_random_intro())
    tweet_comment(new_tweet,intro)
    # print(intro)

################################# TIME #################################
def minToSec(mins=1):
    return mins*60

def hoursToMins(hrs=1):
    return hrs*60

def hoursToSec(hrs=1):
    return hrs * 60 * 60

def randomizeInterval(t=10,randomization=100):
    spread = t*randomization/100
    t = round(random.uniform(t-spread,t+spread))
    return t

def getHour():
    return int(datetime.now().hour)

def amAwake():
    hour = getHour()
    if hour > waketime and hour < bedtime:
        return True
    else:
        return False

def getTimeInterval(mins=10,spread=1):
    if(amAwake()):
        return randomizeInterval(mins,spread)
    else: #return sleep interval to next waketime
        curr_hour = getHour()
        if(curr_hour < waketime):  #if before waketime, subtract current hour i.e., 5AM - 3AM = 2 hrs & also randomize wake time by 10%
            return hoursToMins(waketime - getHour() -1+randomizeInterval(1,spread))
        else: #if after waketime, 24 - 6AM(curr) = 18hrs + 5hrs(waketime tomorrow)
            return hoursToMins((24 - curr_hour) + waketime -1+randomizeInterval(1,spread))

########################################## MAIN ##########################################
def main():
    while(True):
        init()
        #randomize behaviors by percentages
        r = random.randrange(100)
        lower=0
        if(r < q_pct + lower):
            lower += q_pct
            print('tweet quote')
            try:
                tweet_random_quote()
            except:
                pass
        else:
            print('tweeting')
            retweet_top_tweet()
        next_intvl=getTimeInterval(min_interval,randmzn)
        print("""Sleeping for {} minutes""".format(next_intvl))
        sleep(minToSec(next_intvl))

if __name__ == "__main__":
    main()