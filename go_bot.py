#!env/bin/python3
import os
from os import environ
#this line sets the egg unzip directory to one that is writeable
os.environ['PYTHON_EGG_CACHE'] = '/tmp' # a writable directory 
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

import bot 
import averagejoe as aj
version = "2.0"
defaults = """{
"hashtags": "#tech",
"interval": "5",
"randomization": "10",
"waketime": "10",
"bedtime": "23",
"timezone": "America/Los_Angeles",
"min_pop": "1000",
"character": "default",
"mode": "interval",
"behaviors":"chat tweet",
"username": "",
"userid": ""
}"""

class Go_Bot():
    def __init__(self,**kwargs):
        #first load defaults
        self.settings = self.load_default_config()
        self.auth = kwargs['auth']
        self.config = kwargs['config']
        self.sources = kwargs['sources']
        self.init_config()
        self.init_sources()
        self.joe = aj.Joe(self.timezone,self.waketime,self.bedtime,self.interval,self.randomization)
        self.bot = bot.Bot(auth=self.auth,source_list=self.source_list)

    ############################ Config: ############################
    def init_config(self):
        if('string' in self.config):self.load_str_config(self.config['string'])
        elif('file' in self.config):self.load_file_config(self.config['file'])
        elif('url' in self.config):self.load_url_config(self.config['url'])
        elif('env' in self.config):self.settings = self.load_env_config()
        elif('defaults' in self.config):self.load_default_config()
        else:
            try:
                print("Loading config from env")
                self.settings = load_env_config()
                self.config = {"env":True}
            except:
                print("Loading default config")
                self.config = {"defaults":True}
                print("Unable to load custom settings. Keeping defaults")
                self.load_default_config()
        print(self.config.keys())
        
    def load_default_config(self):
        print("Loading default config")
        self.load_str_config(defaults)

    def load_str_config(self,str):
        print("Loading config from string literal.")
        cfg = json.loads(str)
        self.load_settings(cfg)

    def load_file_config(self,filename):
        print("Loading config from file: "+filename)
        with open(filename) as config_file:
            cfg = json.load(config_file)
            self.load_settings(cfg)
    
    def load_url_config(self,url):
        print("Loading config from url: "+url)
        pass

    def load_env_config(self):
        print("Loading config from environment variable.")
        cfg = json.loads(environ['CONFIG'])
        self.load_settings()
    
    ############################ Settings: ############################
    def load_settings(self,settings):
        #overwrite default settings if values found in config
        if(settings['hashtags']): self.hashtags =           settings['hashtags'].lower()
        if(settings['interval']): self.interval =           int(settings['interval'])
        if(settings['randomization']): self.randomization = int(settings['randomization'])
        if(settings['waketime']): self.waketime =           int(settings['waketime'])
        if(settings['bedtime']): self.bedtime =             int(settings['bedtime'])
        if(settings['timezone']): self.timezone =           settings['timezone'].lower()
        if(settings['min_pop']): self.min_pop =             int(settings['min_pop'])
        if(settings['character']): self.character =         settings['character'].lower()
        if(settings['mode']): self.mode =                   settings['mode'].lower()
        if(settings['behaviors']): self.behaviors =         settings['behaviors'].lower()
        if(settings['username']): self.username =           settings['username'].lower()
        if(settings['userid']): self.userid =               settings['userid'].lower()

    ############################ Sources: ############################
    def init_sources(self):
        print(self.sources.keys())
        if('string' in self.sources):self.source_list = self.load_str_sources(self.sources['string'])
        elif('file' in self.sources):self.source_list = self.load_file_sources(self.sources['file'])
        elif('url' in self.sources):self.source_list = self.load_url_sources(self.sources['url'])
        elif('env' in self.sources):self.source_list = self.settings = self.load_env_sources()
        elif('defaults' in self.sources):self.source_list = self.load_default_sources()
        else:
            try:
                print("Loading sources from environment variable")
                self.sources = {"env":True}
                self.source_list = self.load_env_sources()
            except:
                print("Loading default sources")
                self.sources = {"defaults":True}
                print("Unable to load custom settings. Keeping defaults")
                self.source_list = self.load_default_sources()
        print("Sources:")
        print(self.sources.keys())
        
    def load_default_sources(self):
        print("Loading default sources")
        return self.load_file_sources("sources.json")

    def load_str_sources(self,str):
        print("Loading sources from string literal.")
        return json.loads(str)

    def load_file_sources(self,filename):
        print("Loading sources from file: "+filename)
        with open(filename) as src_file:
            return json.load(src_file)
    
    def load_url_sources(self,url):
        print("Loading sources from url: "+url)
        pass

    def load_env_sources(self):
        print("Loading sources from environment variable.")
        return json.loads(environ['CONFIG'])

    ############################ Main Loop: ############################
    def go(self):
        while(True):
            print("Updating settings")
            self.init_config()
            print("Reloading sources")
            self.init_sources()
            self.bot.load_sources(self.source_list)
            try:
                if("chat" in self.behaviors):
                    print("Chat: Responding to messages")
                    try:
                        self.bot.check_messages(True,'default') #respond to messages
                    except FunctionTimedOut:
                        print("Timed out responding to messages.")
                if("tweet" in self.behaviors):
                    print("Tweet: Sending tweet")  
                    try:              
                        self.bot.do_action()
                    except FunctionTimedOut:
                        print("Timed out sending tweet.")
                next_intvl=self.joe.get_next_interval()
                print("""Time is: {}. Sleeping for {} minutes""".format(bot.getHour(self.timezone),next_intvl))
                #convert interval to seconds for sleep
                sleep(bot.minToSec(next_intvl))
            except Exception as e:
                print(e)
                print("[Error] Failed to complete action. Sleeping for 15 minutes")
                sleep(bot.minToSec(15))

############################ Special pre-initialization loading functions: ############################
def load_default_auth():
    try:
        print("Trying to load auth from file")
        return load_file_auth("env.json")
    except:
        try:
            print("Trying to load auth from environment variable")
            return load_env_auth()
        except:
            print("Unable to load auth. Exiting.")
            exit(1)

def load_str_auth(str):
    return json.loads(str)

def load_file_auth(file):
    with open(file) as auth_file:
        return json.load(auth_file)

def load_env_auth():
    auth = json.loads(environ['AUTH'])
    return auth

def load_env_config(self):
    print("Loading config from environment variable.")
    return json.loads(environ['CONFIG'])

def load_env_sources(self):
    print("Loading sources from environment variable.")
    return json.loads(environ['CONFIG'])

    ############################ Accessory Functions: ############################
if __name__ == "__main__":
    global prod
    prod=True
    print("Running Twitter Bot Version %s"%(version))
    #Commandline args:
    parser = argparse.ArgumentParser(description="""Twitter bot version {}""".format(version))
    parser.add_argument("-V", "--version", help="program version", action="store_true")
    parser.add_argument("-t", "--test", help="test mode", action="store_true")
    parser.add_argument("-c", "--config", help="Set config string")
    parser.add_argument("-cf","--config_file",help="Set config filename")
    # parser.add_argument("-cu", "--config_url", help="Set config URL")
    parser.add_argument("-s", "--sources", help="Set sources filename")
    parser.add_argument("-sf", "--sources_file", help="Set sources filename")
    # parser.add_argument("-su", "--sources_url", help="Set sources URL")
    parser.add_argument("-a", "--auth", help="Set auth")
    parser.add_argument("-af", "--auth_file", help="Set auth file")
    args = parser.parse_args()
    if(args.test):
        print("Running in test mode")
        prod = False
        print("Running in prod mode")
    elif(args.version):
        print("Running Twitter Bot Version %s"%(version))

    #auth:
    if(args.auth): auth = load_str_auth(args.auth)
    elif(args.auth_file): auth = load_file_auth(args.auth_file)
    else:
        try:
            auth = load_env_auth()
        except:
            auth = load_default_auth()

    #sources
    if(args.sources):src = {"string":args.sources}
    elif(args.sources_file):src = {"file":args.sources_file}
    # elif(args.sources_url):src = {"url":args.sources_url}
    else:src = {"defaults":True}

    #config
    if(args.config):cfg = {"string":args.config}
    elif(args.config_file):cfg={"file":args.config_file}
    # elif(args.config_url):cfg={"url":args.config_url}
    else:
        #if nothing specified
        try:
            cfg = {"env":load_env_config()}
        except:
            cfg = {"defaults":True}
    go = Go_Bot(auth=auth,config = cfg,sources=src)
    go.go()
