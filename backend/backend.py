from typing import Dict
import tweepy
import os
import json
import asyncio
import sys

from twitter import oauth
import geocoder
from twitter import Twitter, OAuth

import pandas as pd

import csv

from processing import cleanText




#from predictor import 

# API Keys and Tokens
consumer_key = 'K3pFCtLVRhC0UmkD13INetdtd'
consumer_secret = 'POp4rBmhGgeyPVHLH0mRvl5QQAUdfLCM4BTGySGqpakFQJD3HF'
access_token = '900436394463477761-O1plQQoWGwrTyhbeWbz79Ph7SwdqSyu'
access_token_secret = 'TpMfX2IugSqrFzOsbsJU9HRd1YyGi58GjyxvyjsVSfITI'

# Authorization and Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

oauth = OAuth(access_token, access_token_secret,consumer_key,consumer_secret)
t = Twitter(auth=oauth)




def processEachTrend(trends):

    hashTagToContent = []
    for eachTrending in trends:
        for trend in eachTrending['trends']:
            if trend['tweet_volume']:
                
                content = {}
                content['tag'] = trend['name']
                content['tweet_volume'] = trend['tweet_volume']
            
                query = t.search.tweets(q=trend['query'])
                text = ""
                for s in query['statuses']:
                    text += s['text']+"\n"

                text = cleanText(text)
                content['text'] = text.encode("utf-8")
                hashTagToContent.append(content)
    
    return hashTagToContent


def generateHashTags(region):


    # Trends for Specific Country
    loc = region     # location as argument variable 
    g = geocoder.osm(loc) # getting object that has location's latitude and longitude

    closest_loc = api.trends_closest(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])

    # writing a JSON file that has the latest trends for that location
    with open("twitter_{}_trend.json".format(loc),"w") as wp:
        wp.write(json.dumps(trends, indent=1))

    hashTagToContent = processEachTrend(trends)


    f = open("hashtags.csv", "w", encoding="utf-8")
    writer = csv.DictWriter(
    f, fieldnames=["tag", "text", "tweet_volume"])
    writer.writeheader()
    writer.writerows(hashTagToContent)
    f.close()




    
