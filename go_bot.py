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

import bot 
from BotStreamListener import BotStreamListener
import averagejoe as aj
version = "2.0"

class Go_Bot():
    def __init__(self,cfg=None):
        #first load defaults
        try:
            print("Loading default config values")
            self.load_default_config()
        except:
            print("Unable to load default config file")
        #if specified, load config and overwrite default values
        if(cfg): 
            print("Loading config from parameter")
            self.load_config(cfg)
        else: #else try loading from environment variables
            try:
                print("Loading config from environment variables")
                self.load_env_config()
            except Exception as e:
                print(e)
                print("Unable to load config from env variables.")
        #Load auth and login to twitter
        self.joe = aj.Joe(self.timezone,self.waketime,self.bedtime,self.interval,self.randomization)
        self.bot = bot.Bot()

    ############################ Config: ############################
    def load_default_config(self):
        # import config
        with open("./config.json") as config_file:
            cfg = json.load(config_file)
            self.load_settings(cfg)

    def load_env_config(self):
        cfg = json.loads(environ['CONFIG'])
        self.load_settings(cfg)
    
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

    #main run loop
    def go(self):
        while(True):
            try:
                if("chat" in self.behaviors):
                    print("Chat: Responding to messages")
                    self.bot.check_messages(True,'default') #respond to messages
                if("tweet" in self.behaviors):
                    print("Tweet: Sending tweet")                
                    self.bot.do_action()
                next_intvl=self.joe.get_next_interval()
                print("""Time is: {}. Sleeping for {} minutes""".format(bot.getHour(self.timezone),next_intvl))
                #convert interval to seconds for sleep
                sleep(bot.minToSec(next_intvl))
            except Exception as e:
                print(e)
                print("[Error] Failed to complete action. Sleeping for 15 minutes")
                sleep(bot.minToSec(15))

    ############################ Accessory Functions: ############################
if __name__ == "__main__":
    print("Running Twitter Bot Version %s"%(version))
    global prod
    prod = True
    if(len(sys.argv)>1):
        if('t' in sys.argv[1].lower()):
            prod=False
            print("Running in test mode")
            test()
    else:
        print("Running in prod mode")
        go = Go_Bot()
        go.go()
