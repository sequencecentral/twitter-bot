import json
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
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout
import argparse

import basicbot
#widgets
from synchron import quotewidget
from synchron import twitterwidget
from synchron import newswidget
from synchron import redditwidget
from synchron import rsswidget
from synchron import udemywidget
version = "1.0"
ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"

class Bot():
    def __init__(self,auth, source_list):
        self.auth = auth
        self.load_sources(source_list)
        # self.init_actions() #moved to load_sources
        #Initialize bot
        self.re = basicbot.responder.Responder()
        self.tw = self.init_twitter(auth)
        self.tw.check_messages(False) #initialize current messages

    def load_reddit_creds(self):
        return self.auth

    ############################ Sources: ############################
    def load_default_sources(self):
        with open("./sources.json") as source_file:
            sources = json.load(source_file)
            self.load_sources(sources)

    def load_env_sources(self):
        sources = json.loads(environ['SOURCES'])
        self.load_sources(sources)

    def load_sources(self,src):
        # print("sources:   "+sources.)
        self.sources = {}
        for source in src:
            # print(source)
            self.load_source(source)
        self.normalize_source_frequencies()
        self.init_actions()

    def load_source(self,source):
        print("Loading source: "+source["name"])
        parsed={}
        parsed["name"] = source["name"]
        parsed["type"] = source["type"]
        if(source["frequency"]):
            parsed["frequency"] = int(source["frequency"])
        else:
            parsed["frequency"] = 0
        parsed["terms"] = source["terms"]
        parsed["addtags"] = source["addtags"]
        if('url' in source): 
            parsed["url"] = source["url"]
        else:
            parsed["url"] = ""
        self.sources[parsed["name"]] = parsed

    def normalize_source_frequencies(self):
        tail_length = 1000000
        #1. Normalize total to tail_length
        #tail_length is the minimum frequency that we can capture
        denom = 0
        for source in self.sources.values():
            source['frequency'] = int(source['frequency'])
            denom += source['frequency']
        scaling_factor = tail_length/denom
        #2. Apply values to each source
        for source in self.sources.values():
            source['frequency'] = int(source['frequency']*scaling_factor) #bc scaling_factor can be non-integer

    ############################ Twitter: ############################
    def init_twitter(self,auth,query="",htags=""):
        tw = twitterwidget.TwitterWidget(auth['API_KEY'], auth['API_SECRET_KEY'], auth['ACCESS_TOKEN'], auth['ACCESS_TOKEN_SECRET'],query,htags)
        return tw

    ############################ Direct Messages: ###########################
    @func_set_timeout(60)
    def check_messages(self,re=False,character='default'):
        print("Checking for DMs")
        msgs = self.tw.check_messages(True)
        if(msgs):
            print("Responding ot DMs")
            for msg in msgs:
                self.respond(tw,dm,character)
        else:
            print("No messages")        

    def respond(self, dm,character='default'):
        resp = basicbot.get_response(character,dm.text)
        print("Responding to message:")
        print("DM %s Response: %s "%(dm.text,resp))
        try:
            self.tw.respond(dm,resp)
        except Exception as e:
            print(e)
            print("Unable to send response")

    ################################# ACTIONS #################################
    def init_actions(self):
        self.actions = []
        for source in self.sources.values():
            if(source['frequency']):
                self.actions.extend([source['name']]*(int(source['frequency'])))

    def tweet_quote(self,topic,addtags):
        print("Tweeting quote")
        try:
            self.tw.tweet(quotewidget.get_update()['tweet'])
        except Exception as e:
            print(e)
            print("Unable to tweet")

    def tweet_news(self,topic,addtags):
        print("Tweeting news")
        print("topic "+topic)
        news = newswidget.get_update(topic,self.auth['BEBUKEY'])
        if(news):
            hashtags = basicbot.tag_it(' '.join(news['keywords']),addtags)
            new_tweet = """{} {} {}""".format(news['title'],news['url'], hashtags)
            print("Response: ",new_tweet)
            try:
                self.tw.tweet(new_tweet)
                return
            except Exception as e:
                print(e)
                print("Unable to tweet news.")
        else:
            print('No news is good news')
            self.tweet_top_tweet()

    def tweet_pubmed(self,feed_name,addtags):
        try:
            ref = rsswidget.get_update(feed_name,bebukey=self.auth['BEBUKEY'])
            print("Retrieved tweet from pubmed %s"%(ref['tweet']))
            hashtags = basicbot.tag_it(ref['title'],addtags)
            tweet_post = """{} {}""".format(ref['tweet'],hashtags)
            print("Tweeting post:  %s"%(tweet_post))
            self.tw.tweet(tweet_post)
        except Exception as e:
            print(e)
            print("Unable to get pubmed update")
            self.tweet_top_tweet()

    def tweet_genomics(self,topic,addtags):
        self.tweet_pubmed('genomics',addtags)

    def tweet_covid19(self,topic,addtags):
        self.tweet_pubmed('covid19',addtags)

    def tweet_techcrunch(self,topic,addtags):
        self.tweet_rss("techcrunch",addtags)

    def tweet_techstartups(self,topic,addtags):
        self.tweet_rss("startups",addtags)

    def tweet_nature_blog(self,topic,addtags):
        self.tweet_rss("nature_blog",addtags)
    
    def tweet_genomeweb(self,topic,addtags):
        self.tweet_rss("genomeweb",addtags)

    def tweet_bioitworld(self,topic,addtags):
        self.tweet_rss("bioitworld",addtags)

    def tweet_job(self,topic,addtags):
        self.tweet_rss("hot_jobs",addtags)

    def tweet_rss(self,feed_name,addtags):
        # try:
        ref = rsswidget.get_update(feed_name,bebukey=self.auth['BEBUKEY'])
        print("Retrieved tweet from RSS %s"%(ref['tweet']))
        hashtags = basicbot.tag_it(ref['title'],addtags)
        tweet_post = """{} {}""".format(ref['tweet'][0:260],hashtags)
        print("Tweeting post:  %s"%(tweet_post))
        self.tw.tweet(tweet_post)

    def tweet_reddit(self,subreddit,hashtags="#news"):
        # try:
        # creds = self.load_reddit_creds()
        creds = self.auth
        #print(get_update(env.client_id,env.client_secret,env.user_agent,"science"))
        print("Getting post")
        post = redditwidget.get_update(creds['REDDIT_CLIENT_ID'],creds['REDDIT_CLIENT_SECRET'],ua,subreddit,5,self.auth['BEBUKEY'])
        print("Tagging post")
        try:
            add_tags = basicbot.tag_it(post['title'],hashtags)
        except:
            add_tags = hashtags
        tweet_post = """{} {}""".format(post['tweet'],add_tags)
        print("Tweeting post:  %s"%(tweet_post))
        self.tw.tweet(tweet_post)
        # except Exception as e:
        #     print(e)
        #     print("Unable to tweet post")
        #     print("Tweeting top tweet instead.")
        #     self.tweet_top_tweet(hashtags)

    def tweet_udemy(self,terms,addtags):
        subreddit = "udemyfreebies"
        try:
            # creds = self.load_reddit_creds()
            creds = self.auth
            print("Getting udemy post")
            udemy = udemywidget.get_update(creds['REDDIT_CLIENT_ID'],creds['REDDIT_CLIENT_SECRET'],subreddit,self.auth['BEBUKEY'])
            print("Tweeting Udemy: %s"%(udemy['tweet']))
            #tweets come pre-tagged
            self.tw.tweet(udemy['tweet'])
        except Exception as e:
            print(e)
            print("Unable to tweet.")

    def tweet_top_tweet(self,terms="",hashtags="#news"):
        tt = self.tw.get_top_tweet()
        hashtags = basicbot.tag_it(tt.text,hashtags)
        intro = """{}""".format(self.re.get_intro(tt.text))[:278]
        print("Tweet Intro: ",intro)
        print("Tweet Text: ",tt.text)
        try:
            self.tw.tweet_comment(tt,intro,hashtags)
        except Exception as e:
            print(e)
            print("Unable to tweet.")

    def reply_top_tweet(self):
        tt = self.tw.get_top_tweet()
        resp = self.re.get_reply(tt.text)
        print("Tweet %s Response: %s "%(tt.text,resp))
        try:
            self.tw.tweet_reply(tt, resp)
        except Exception as e:
            print(e)
            print("Unable to tweet.")
    
    @func_set_timeout(60)
    def do_action(self):
        #note that self.actions is populated with actions proportional to specified frequencies
        action = random.choice(self.actions)
        print("Selected: "+action)
        if(action == "quote"): self.tweet_quote(self.sources["quote"]["terms"],self.sources["quote"]["addtags"])
        elif(action == "news"): self.tweet_news(self.sources["news"]["terms"],self.sources["news"]["addtags"])
        elif(action == "reddit"): self.tweet_reddit(self.sources["reddit"]["terms"],self.sources["reddit"]["addtags"])
        elif(action == "genomics"): self.tweet_genomics(self.sources["genomics"]["terms"],self.sources["genomics"]["addtags"])
        elif(action == "covid19"): self.tweet_covid19(self.sources["covid19"]["terms"],self.sources["covid19"]["addtags"])
        elif(action == "techcrunch"): self.tweet_techcrunch(self.sources["techcrunch"]["terms"],self.sources["techcrunch"]["addtags"])
        elif(action == "techstartups"): self.tweet_techstartups(self.sources["techstartups"]["terms"],self.sources["techstartups"]["addtags"])
        elif(action == "udemy"): self.tweet_udemy(self.sources["udemy"]["terms"],self.sources["udemy"]["addtags"])
        elif(action == "genomeweb"): self.tweet_genomeweb(self.sources["genomeweb"]["terms"],self.sources["genomeweb"]["addtags"])
        elif(action == "bioitworld"): self.tweet_bioitworld(self.sources["bioitworld"]["terms"],self.sources["bioitworld"]["addtags"])
        elif(action == "nature_blog"): self.tweet_nature_blog(self.sources["nature_blog"]["terms"],self.sources["nature_blog"]["addtags"])
        elif(action == "jobs"): self.tweet_job(self.sources["jobs"]["terms"],self.sources["jobs"]["addtags"])
        elif(action == "twitter"): self.tweet_top_tweet()
        else: 
            print("Action not found.")
            self.tweet_rss(self.sources[action]["url"],self.sources[action]["addtags"])

    ############################ Test: ############################
    def test_load_config_file(self):
        # print (config.CONFIG)
        # print(self.hashtags)
        pass

############################ Accessory Functions: ############################
def get_item(lis):
    items = lis.split(' ')
    if(len(items)==1):
        return items[0]
    else:
        return random.choice(items)

def minToSec(mins=1):
    return mins*60

def getHour(timezone):
    tzwc=pytz.timezone(timezone)
    return int(datetime.now(tzwc).hour)

def test():
    # print("test")
    c = Bot()
    c.test_load_config_file()
    # print(c.sources)
    # print(c.actions)
    # print(c.sources["quote"])
    c.do_action()

if(__name__=="__main__"):
    test()