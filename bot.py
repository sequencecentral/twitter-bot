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

class Bot():
    def __init__(self,auth=None,cfg=None):
        #first load defaults
        try:
            self.load_default_config()
        except:
            print("Unable to load default config file")
        #if specified, load config
        if(cfg): 
            self.load_config(cfg)
        else:
            self.load_env_config
        self.init_actions()
        #Load auth and login to twitter
        if(auth): #if auth provided in call
            auth = self.load_auth(auth)
        else:
            try:
                auth = self.load_default_auth()
            except:
                auth = self.load_env_auth()
        self.tw = self.init_twitter(auth)
        self.re = basbot.responder.Responder()

    ############################ Auth: ############################
    def load_auth(self,env):
        creds = {}
        creds['consumer_key'] = env['API_KEY']
        creds['consumer_secret_key'] = env['API_SECRET_KEY']
        creds['access_token'] = env['ACCESS_TOKEN']
        creds['access_token_secret'] = env['ACCESS_TOKEN_SECRET']
        return creds

    def load_default_auth(self):
        import env
        e = json.loads(env.AUTH)
        auth = self.load_auth(e)
        return auth

    def load_env_auth(self):
        creds = {}
        e = json.loads(environ['AUTH'])
        auth = self.load_auth(e)
        return auth

    def load_reddit_creds(self):
        creds = {}
        try:
            a = json.loads(environ['AUTH'])
            creds['client_id'] = a['REDDIT_CLIENT_ID']
            creds['client_secret'] = a['REDDIT_CLIENT_SECRET']
        except:
            print("Env not found. Attempting to load Reddit AUTH from local file.")
            try:
                import env
                a = json.loads(env.AUTH)
                creds['client_id'] = a['REDDIT_CLIENT_ID']
                creds['client_secret'] = a['REDDIT_CLIENT_SECRET']
            except:
                print("Unable to authenticate to Reddit")
                exit(1)
        return creds

    ############################ Config: ############################
    def load_config(self,cfg):
        # try:
        #     self.load_settings(cfg['settings'])
        # except Exception as e:
        #     print(e)
        #     print("Encountered issue initializing settings")
        self.load_sources(cfg['sources'])

    def load_default_config(self):
        import config
        cfg = json.loads(config.CONFIG)
        self.load_config(cfg)

    def load_env_config(self):
        cfg = environ['CONFIG']
        self.load_config(cfg)

    ############################ Settings: ############################
    def load_settings(self,settings):
        #overwrite default settings if values found in config
        if(settings['hashtags']): self.hashtags =           settings['hashtags']
        if(settings['interval']): self.interval =           settings['interval']
        if(settings['randomization']): self.randomization = settings['randomization']
        if(settings['waketime']): self.waketime =           settings['waketime']
        if(settings['bedtime']): self.bedtime =             settings['bedtime']
        if(settings['timezone']): self.timezone =           settings['timezone']
        if(settings['min_pop']): self.min_pop =             settings['min_pop']
        if(settings['character']): self.character =         settings['character']
        if(settings['mode']): self.mode =                   settings['mode']
        if(settings['username']): self.username =           settings['username']
        if(settings['userid']): self.userid =               settings['userid']

    ############################ Sources: ############################
    def load_sources(self,sources):
        self.sources = {}
        for source in sources:
            self.load_source(source)
            print(source)
        self.normalize_source_frequencies()

    def load_source(self,source):
        # print(source)
        parsed={}
        parsed["name"] = source["name"]
        parsed["type"] = source["type"]
        if(source["frequency"]):
            parsed["frequency"] = int(source["frequency"])
        else:
            parsed["frequency"] = 0
        parsed["terms"] = source["terms"]
        parsed["addtags"] = source["addtags"]
        self.sources[parsed["name"]] = parsed

    def normalize_source_frequencies(self):
        denom = 0
        #1. Normalize total to 100
        for source in self.sources.values():
            denom += int(source['frequency'])
        factor = 100/denom
        #2. Apply values to each source
        for source in self.sources.values():
            source['frequency'] = int(int(source['frequency'])*factor)

    ############################ Twitter: ############################
    def init_twitter(self,auth,query="",htags=""):
        tw = twitterwidget.TwitterWidget(auth['consumer_key'], auth['consumer_secret_key'], auth['access_token'], auth['access_token_secret'],query,htags)
        return tw

    ################################# ACTIONS #################################
    def init_actions(self):
        self.actions = []
        for source in self.sources.values():
            if(source['frequency']):
                for i in range(int(source['frequency'])):
                    self.actions.append(source['name'])

    def tweet_quote(self,tw,re,topic,addtags):
        print("Tweeting quote")
        try:
            tw.tweet(qw.get_update())
        except Exception as e:
            print(e)
            print("Unable to tweet")

    def tweet_news(self,tw,re,topic,addtags):
        print("Tweeting news")
        print("topic "+topic)
        news = newswidget.get_update(topic)
        if(news):
            htags = basbot.tag_it(' '.join(news['keywords']),addtags)
            new_tweet = """{} {} {}""".format(news['title'],news['url'], htags)
            print("Response: ",new_tweet)
            try:
                tw.tweet(new_tweet)
                return
            except Exception as e:
                print(e)
                print("Unable to tweet news.")
        else:
            print('No news is good news')
            self.tweet_top_tweet(tw,re)

    def tweet_pubmed(self,tw,re,feed_name,addtags):
        try:
            ref = rsswidget.get_update(feed_name)
            print("Retrieved tweet from pubmed %s"%(ref['tweet']))
            htags = basbot.tag_it(ref['title'],addtags)
            tweet_post = """{} {}""".format(ref['tweet'],htags)
            print("Tweeting post:  %s"%(tweet_post))
            tw.tweet(tweet_post)
        except Exception as e:
            print(e)
            print("Unable to get genomics update")
            self.tweet_top_tweet(tw,re)

    def tweet_genomics(self,tw,re,topic,addtags):
        self.tweet_pubmed(tw,re,'genomics',addtags)

    def tweet_covid19(self,tw,re,topic,addtags):
        self.tweet_pubmed(tw,re,'covid19',addtags)

    def tweet_rss(self,tw,re,feed_name,addtags):
        try:
            ref = rsswidget.get_update(feed_name)
            print("Retrieved tweet from RSS %s"%(ref['tweet']))
            htags = basbot.tag_it(ref['title'],addtags)
            tweet_post = """{} {}""".format(ref['tweet'],htags)
            print("Tweeting post:  %s"%(tweet_post))
            tw.tweet(tweet_post)
        except Exception as e:
            print(e)
            print("Unable to tweet RSS %s"%(feed_name))
            self.tweet_top_tweet(tw,re)

    def tweet_techcrunch(self,tw,re,topic,addtags):
        self.tweet_rss(tw,re,"techcrunch",addtags)

    def tweet_techstartups(self,tw,re,topic,addtags):
        self.tweet_rss(tw,re,"startups",addtags)

    def tweet_reddit(self,tw,re,subreddit,hashtags="#news"):
        rejects = ['reddit.com','redd.it','reddit','nsfw','redd','red']
        creds = self.load_reddit_creds()
        ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
        try:
            #             print(get_update(env.client_id,env.client_secret,env.user_agent,"science"))
            post = redditwidget.get_update(creds['client_id'],creds['client_secret'],ua,subreddit)
            print("Tagging post")
            add_tags = basbot.tag_it(post['title'],hashtags)
            tweet_post = """{} {}""".format(post['tweet'],add_tags)
            print("Tweeting post:  %s"%(tweet_post))
            tw.tweet(tweet_post)
        except Exception as e:
            print(e)
            print("Unable to tweet post")
            print("Tweeting top tweet instead.")
            self.tweet_top_tweet(tw,re,hashtags)

    def tweet_udemy(self,tw,re,terms,addtags):
        creds = load_reddit_creds()
        try:
            udemy = udemywidget.get_update(creds['client_id'],creds['client_secret'],"Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0","udemyfreebies")
            print("Tweeting Udemy: %s"%(udemy['tweet']))
            #tweets come pre-tagged
            tw.tweet(udemy['tweet'])
        except Exception as e:
            print(e)
            print("Unable to tweet.")

    def tweet_top_tweet(self,tw,re,terms="",hashtags="#news"):
        tt = tw.get_top_tweet()
        htags = basbot.tag_it(tt.text,hashtags)
        intro = """{}""".format(re.get_intro(tt.text))[:278]
        print("Tweet Intro: ",intro)
        try:
            tw.tweet_comment(tt,intro,htags)
        except Exception as e:
            print(e)
            print("Unable to tweet.")

    def reply_top_tweet(self,tw,re):
        tt = tw.get_top_tweet()
        resp = re.get_reply(tt.text)
        print("Tweet %s Response: %s "%(tt.text,resp))
        try:
            tw.tweet_reply(tt, resp)
        except Exception as e:
            print(e)
            print("Unable to tweet.")

    def respond(self,tw, dm):
        resp = basbot.get_response('default',dm.text)
        print("Responding to message:")
        print("DM %s Response: %s "%(dm.text,resp))
        try:
            tw.respond(dm,resp)
        except Exception as e:
            print(e)
            print("Unable to send response")

    def do_action(self):
        #note that self.actions is populated with actions proportional to specified frequencies
        action = random.choice(self.actions)
        print("Selected: "+action)
        if(action == "quote"): self.tweet_quote(self.tw,self.re,self.sources["quote"]["terms"],self.sources["quote"]["addtags"])
        elif(action == "news"): self.tweet_news(self.tw,self.re,self.sources["news"]["terms"],self.sources["news"]["addtags"])
        elif(action == "reddit"): self.tweet_reddit(self.tw,self.re,self.sources["reddit"]["terms"],self.sources["reddit"]["addtags"])
        elif(action == "genomics"): self.tweet_genomics(self.tw,self.re,self.sources["genomics"]["terms"],self.sources["genomics"]["addtags"])
        elif(action == "covid19"): self.tweet_covid19(self.tw,self.re,self.sources["covid19"]["terms"],self.sources["covid19"]["addtags"])
        elif(action == "techcrunch"): self.tweet_techcrunch(self.tw,self.re,self.sources["techcrunch"]["terms"],self.sources["techcrunch"]["addtags"])
        elif(action == "techstartups"): self.tweet_techstartups(self.tw,self.re,self.sources["techstartups"]["terms"],self.sources["techstartups"]["addtags"])
        elif(action == "udemy"): self.tweet_udemy(self.tw,self.re,self.sources["udemy"]["terms"],self.sources["udemy"]["addtags"])
        elif(action == "twitter"): self.tweet_top_tweet(tw,re)
        else: print("Action not found.")

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