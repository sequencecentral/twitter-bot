from rx import interval
from rx.subject import Subject
import time

class Scanner:
    def __init__(self,api,intvl=1,query=""):
        self.api = api
        self.interval=interval
        self.query=query
        print('Started scanner')
        while True:
            self.getTopTweet()
            time.sleep(intvl)
        self.twSubject = Subject()
        self.twSubject.subscribe(
            lambda x: print("Value: {0}".format(x))
        )
        self.twSubject.on_next('Tweet!')

    def getTopTweet(self):
        print('get top tweet')
        self.api.search()
        pass

    def onTweet(self,fn):
        self.twSubject.subscribe(fn)