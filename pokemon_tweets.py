import zmq


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://10.50.0.118:6300')

from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from twython import TwythonStreamer
import time
import json
analyzer = SentimentIntensityAnalyzer()

CONSUMER_KEY = 'eqPzI987WKXoqOQcvWpbfjdGm'
CONSUMER_SECRET = 'zw1IxlWpAVG7lpPMA7aYlDRxEpGnSanQjJn4KQF51hc08WEfaT'
ACCESS_TOKEN = '925718132760678403-ozYXfaFl4a8othHQmHGqFQqc9ITNQqC'
ACCESS_TOKEN_SECRET = 'on8UY6oUKBM0hmHWQKbCnBtkCOAnnDW1sYg3bBxNfQoo8'

tweets = []
keywords = ['England','America','France','North Korea','Chile']

class MyStreamer(TwythonStreamer):   #base class
    counter = 0
    def on_success(self, data):
        if data ['lang'] == 'en':          #if it is in english
            MyStreamer.counter += 1
            #print(data['text'])
            sentiment = analyzer.polarity_scores((data['text']))['compound']
            for word in keywords:
                if word.upper() in data['text'].upper():
                    msg = ('{0} | {1}'.format(sentiment, word))
                    print(msg)
                    socket.send_string(str(msg))

            #tweets.append(data)
            #print('YES - Tweet number {c} has arrived'.format(c = MyStreamer.counter))
    def on_error(self, status_code, data):
        #print (status_code, data)
        self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#timeout = time.time() + 60
while True:
    #if time.time() > timeout:
        #break
    stream.statuses.filter(track = keywords)
    #print(tweets)