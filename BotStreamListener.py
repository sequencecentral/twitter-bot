import tweepy
#override tweepy.StreamListener to add logic to on_status
class BotStreamListener(tweepy.StreamListener):
    def __init__(self,_callback=None,_errorHandler=None):
        super(BotStreamListener,self).__init__()
        self._callback=_callback
        self._errorHandler=_errorHandler

    def on_status(self, status):
        print(status.text)
        if self._callback:
            self._callback(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            if self._errorHandler:
                self._errorHandler(status_code)
            return False
    
    # def on_status(self, status):
    #     print (status.author.screen_name, status.created_at, status.text)
