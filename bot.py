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
    try:
        query_string=environ['QUERY_STRING']
        hashtags=environ['HASHTAGS']
        min_interval=int(environ['INTERVAL'])
        randmzn=int(environ['RANDOMIZATION'])
        waketime=int(environ['WAKETIME'])
        bedtime=int(environ['BEDTIME'])
        q_pct=int(environ['QUOTES_PERCENT'])
        min_pop=int(environ['MIN_POP'])
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
        except:
            print("Failed to load config")
            exit(1)

#initialize api
def init():
    auth()
    config()
    load_intros()
    load_emojis()

def load_intros():
    global intros
    with open('intro.json') as f:
        intros = json.load(f)

def load_emojis():
    global emojis
    with open('emojis.json') as f:
        emojis = json.load(f)

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

def get_top_tweet():
    tweets = api.search(q=query_string,rpp=100,count=100,lang='en',RESULT_TYPE='popular')
    # print(tweets)
    pop = [t for t in tweets if int(t.user.followers_count)>min_pop]
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
    sent = sentiment.get_sentiment(top_tweet.text)
    if 'Positive' in sent:
        intro = """{} {} {} """.format(get_pos_emoji(),get_pos_intro(),get_random_emoji())
    elif 'Negative' in sent:
        intro = """{} {} {} """.format(get_neg_emoji(),get_neg_intro(),get_random_emoji())
    else:
        intro = """{} {} {} """.format(get_random_emoji(),get_random_emoji(),get_random_intro())
    print("Tweet Text is: %s"%(top_tweet.text))
    print("Sentiment is %s"%(sent))
    print("Intro: %s"%(intro))
    tweet_comment(top_tweet,intro)
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
    t = abs(round(random.uniform(t-spread,t+spread)))
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
    # init()
    # retweet_top_tweet()
    while(True):
        # print(get_random_emoji())
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
                print("Error tweeting random quote")
        else:
            print('tweeting')
            retweet_top_tweet()
            # try:
            # except:
            #     print("Error retweeting top tweet")
        next_intvl=getTimeInterval(min_interval,randmzn)
        print("""Sleeping for {} minutes""".format(next_intvl))
        sleep(minToSec(next_intvl))

if __name__ == "__main__":
    main()