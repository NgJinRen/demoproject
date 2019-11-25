from django.shortcuts import render
from django.http import HttpResponse
import threading
from fusioncharts import FusionCharts
from nltk.corpus import twitter_samples
import sys, tweepy
import psycopg2
from collections import OrderedDict
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import Cursor
import os
from time import sleep
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import matplotlib.pyplot as plt
from urllib.error import HTTPError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from translate import Translator
import functools
from .models import Tweet


# def translate_text(tweet):
#     translator= Translator(to_lang="en")
#     try: 
#         if detect(tweet.full_text) == "en":
#             trans = tweet.full_text
#         else:
#             trans = translator.translate(tweet.full_text)
#     except ValueError:
#         trans = "Decoding JSON has failed"
#     return (trans)    

def my_function(x):
    return list(dict.fromkeys(x))

def detect_full_text(tweet):
    if 'retweeted_status' in tweet._json:
        analysis_tweet = tweet._json['retweeted_status']['full_text']
    else:
        analysis_tweet = tweet.full_text
    return str(analysis_tweet)


# Create your views here.
def home(request):

    # twitter api and access token 

    auth = tweepy.OAuthHandler('itKVsbXzVlQlmCrBPGnHcG0rC', 'XYcZdqh8YxtT4PQNCyOtcZu6EWally225pEVlAVyCwUqMp0bFM')
    auth.set_access_token('846849179800391685-Dl8gpJQtOyK1D8F1NLVom8akn4saXmK', 'KAZIymXjxCckfB8QxOfi8bivHEDDi67ttt4aPf8J4PtPD')

    api = tweepy.API(auth, wait_on_rate_limit=True)


    sentiment_house_tweet = tweepy.Cursor(api.search, q="perak water", tweet_mode="extended").items(50)

   

    sentiment_bus_tweet = tweepy.Cursor(api.search, q="perak bus", tweet_mode="extended").items(50)

   
    sentiment_school_tweet = tweepy.Cursor(api.search, q="perak school", tweet_mode="extended").items(50)


    sentiment_food_tweet = tweepy.Cursor(api.search, q="perak food", tweet_mode="extended").items(50)

    sentiment_safety_tweet = tweepy.Cursor(api.search, q="perak police", tweet_mode="extended").items(50)

    sentiment_health_tweet = tweepy.Cursor(api.search, q="perak health", tweet_mode="extended").items(50)
    # sentiment_school_tweet = tweepy.Cursor(api.search, q=('perak AND water OR perak AND bus'), tweet_mode="extended").items(50)

    
    tz = pytz.timezone('Etc/GMT+8')
    
    # tweetCriteria = got.manager.TweetCriteria().setUntil("2016-01-31").setQuerySearch("bitcoin").setMaxTweets(3)
    # new_tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

    my_analysis = []
    my_analysis_bus = []
    my_analysis_school = []
    positive_analysis_food = []
    positive_analysis_safety = []
    positive_analysis_health = []
    negative_analysis_water = []
    negative_analysis_bus = []
    negative_analysis_school = []
    negative_analysis_food = []
    negative_analysis_safety = []
    negative_analysis_health = []
    neutral_analysis_water = []
    neutral_analysis_bus = []
    neutral_analysis_school = []
    neutral_analysis_food = []
    neutral_analysis_safety = []
    neutral_analysis_health = []

    status = 0
    positive = 0
    negative = 0
    neutral = 0
    positive_bus = 0
    negative_bus = 0
    neutral_bus = 0
    positive_school = 0
    negative_school = 0
    neutral_school = 0
    positive_food = 0
    negative_food = 0
    neutral_food = 0
    positive_safety = 0
    negative_safety = 0
    neutral_safety = 0
    positive_health = 0
    negative_health = 0
    neutral_health = 0

    total_positive = 0
    total_negative = 0
    total_neutral = 0 
    
    x=0

    negative_water_retweet = []
    negative_school_retweet = []
    negative_bus_retweet = []
    positive_water_retweet = []
    positive_school_retweet = []
    positive_bus_retweet = []

    analyser = SentimentIntensityAnalyzer()
   
    # water
    for tweet in sentiment_house_tweet:
       
        # detect_tweet = detect_full_text(tweet) 
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        if lb >= 0.05:
            status = "Positive"
            positive += 1
            print(status)
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.positive = 1
            # tweet_table.negative = 0
            # tweet_table.neutral = 0
            # tweet_table.search_title_status = "water"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            positive_water_retweet.append(tweet.retweet_count)   
            my_analysis.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral += 1   
            print(status) 
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.neutral = 1
            # tweet_table.positive = 0
            # tweet_table.negative = 0
            # tweet_table.search_title_status = "water"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_water.append({
                                'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative += 1  
            print(status)
            negative_water_retweet.append(tweet.retweet_count)  
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.negative = 1
            # tweet_table.neutral = 0
            # tweet_table.positive = 0
            # tweet_table.search_title_status = "water"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_water.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })

    # bus
    for tweet in sentiment_bus_tweet:
       
        # detect_bus_tweet = detect_full_text(tweet)  
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        
        if lb >= 0.05:
            status = "Positive"
            positive_bus += 1
            positive_bus_retweet.append(tweet.retweet_count) 
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.positive = 1
            # tweet_table.negative = 0
            # tweet_table.neutral = 0
            # tweet_table.search_title_status = "bus"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            my_analysis_bus.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral_bus += 1
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.neutral = 1
            # tweet_table.positive = 0
            # tweet_table.negative = 0
            # tweet_table.search_title_status = "bus"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_bus.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative_bus += 1
            negative_bus_retweet.append(tweet.retweet_count)
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.negative = 1
            # tweet_table.neutral = 0
            # tweet_table.positive = 0
            # tweet_table.search_title_status = "bus"
            # tweet_table.save()  
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_bus.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })

    # school
    for tweet in sentiment_school_tweet:
       
        # detect_school_tweet = detect_full_text(tweet) 
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        
        if lb >= 0.05:
            status = "Positive"
            positive_school += 1
            positive_school_retweet.append(tweet.retweet_count)  
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.positive = 1
            # tweet_table.negative = 0
            # tweet_table.neutral = 0
            # tweet_table.search_title_status = "school"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            my_analysis_school.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral_school += 1
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.neutral = 1
            # tweet_table.positive = 0
            # tweet_table.negative = 0
            # tweet_table.search_title_status = "school"
            # tweet_table.save()
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_school.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative_school += 1
            negative_school_retweet.append(tweet.retweet_count)  
            # tweet_table.tweet_id = tweet.id
            # tweet_table.title = tweet.full_text
            # tweet_table.created_on = tweet.created_at
            # tweet_table.negative = 1
            # tweet_table.neutral = 0
            # tweet_table.positive = 0
            # tweet_table.search_title_status = "school"
            # tweet_table.save()  
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_school.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
    # food
    for tweet in sentiment_food_tweet:
       
        # detect_food_tweet = detect_full_text(tweet) 
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        
        if lb >= 0.05:
            status = "Positive"
            positive_food += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            positive_analysis_food.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral_food += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_food.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative_food += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_food.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
            })
    # safety
    for tweet in sentiment_safety_tweet:
       
        # detect_safety_tweet = detect_full_text(tweet) 
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        
        if lb >= 0.05:
            status = "Positive"
            positive_safety += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            positive_analysis_safety.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral_safety += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_safety.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative_safety += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_safety.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
            })

    # health
    for tweet in sentiment_health_tweet:
       
        # detect_health_tweet = detect_full_text(tweet) 
        # translator= Translator(from_lang="id", to_lang="en")
        # if detect(tweet.full_text) == "en":
        #     trans = tweet.full_text
        # else:
        #     trans = translator.translate(tweet.full_text)
        score = analyser.polarity_scores(tweet.full_text)
        lb = score['compound']
        
        if lb >= 0.05:
            status = "Positive"
            positive_health += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            positive_analysis_health.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        elif (lb > -0.05) and (lb < 0.05):
            status = "Neutral"
            neutral_health += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            neutral_analysis_health.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
                           })
        else:
            status = "Negative"
            negative_health += 1
            if(tweet.place is not None):
                tweet_location = tweet.place.full_name
            else:
                tweet_location = "None"
            negative_analysis_health.append({'tweet_title': tweet.full_text, 
                                'date': tz.localize(tweet.created_at),
                                'retweet_count': tweet.retweet_count,
                                'user_location': tweet_location
            })
    
    


    most_positive_tweet = max(positive_bus_retweet+positive_school_retweet+positive_water_retweet)
    most_negative_tweet = max(negative_bus_retweet+negative_school_retweet+negative_water_retweet)
   
    #Total of sentiment analysis
    total_positive = positive + positive_bus + positive_school + positive_food + positive_safety + positive_health
    total_negative = negative + negative_bus + negative_school + negative_food + negative_safety + negative_health
    total_neutral = neutral + neutral_bus + neutral_school + neutral_food + neutral_safety + neutral_health

    all_total_positive = total_positive + total_negative + total_neutral 
    total_positive_percent = float(str(round((total_positive / all_total_positive) * 100, 2)))
    total_negative_percent = float(str(round((total_negative / all_total_positive) * 100, 2)))
    total_neutral_percent = float(str(round((total_neutral / all_total_positive) * 100, 2)))


    # percentage of water 
    total_water_num = positive + negative + neutral 
    percent_positive = (positive / total_water_num) * 100
    percent_negative = (negative / total_water_num) * 100
    percent_neutral = (neutral / total_water_num) * 100

    # percentage of bus 
    total_bus_num = positive_bus + negative_bus + neutral_bus 
    percent_positive_bus = (positive_bus / total_bus_num) * 100
    percent_negative_bus = (negative_bus / total_bus_num) * 100
    percent_neutral_bus = (neutral_bus / total_bus_num) * 100

    # percentage of school 
    total_school_num = positive_school + negative_school + neutral_school 
    percent_positive_school = (positive_school / total_school_num) * 100
    percent_negative_school = (negative_school / total_school_num) * 100
    percent_neutral_school = (neutral_school / total_school_num) * 100

    # percentage of food 
    total_food_num = positive_food + negative_food + neutral_food 
    percent_positive_food = (positive_food / total_food_num) * 100
    percent_negative_food = (negative_food / total_food_num) * 100
    percent_neutral_food = (neutral_food / total_food_num) * 100

    # percentage of safety 
    total_safety_num = positive_safety + negative_safety + neutral_safety
    percent_positive_safety = (positive_safety / total_safety_num) * 100
    percent_negative_safety = (negative_safety / total_safety_num) * 100
    percent_neutral_safety = (neutral_safety / total_safety_num) * 100

    # percentage of health 
    total_health_num = positive_health + negative_health + neutral_health
    percent_positive_health = (positive_health / total_health_num) * 100
    percent_negative_health = (negative_health / total_health_num) * 100
    percent_neutral_health = (neutral_health / total_health_num) * 100


    # sortedArray = sorted(
    #     total_positive_sentiment,
    #     key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True
    # )
    # print(sortedArray)
    
    #Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Sentiment Analysis with number of tweets"
    chartConfig["showlegend"] = "1",
    chartConfig["showpercentvalues"] = "1",
    chartConfig["usedataplotcolorforlabels"] = "1",
   

    # The `chartData` dict contains key-value pairs of data
    chartData = OrderedDict()
    chartData["Positive"] = positive
    chartData["Negative"] = negative
    chartData["Neutral"] = neutral
    

    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    #The data for the chart should be in an array wherein each element of the array
    #is a JSON object# having the `label` and `value` as keys.

    #Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("pie2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)


    #bus chart
    #Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource_bus = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig_bus = OrderedDict()
    chartConfig_bus["caption"] = "Sentiment Analysis with number of tweets"
    chartConfig_bus["showlegend"] = "1",
    chartConfig_bus["showpercentvalues"] = "1",
    chartConfig_bus["usedataplotcolorforlabels"] = "1",
   

    # The `chartData` dict contains key-value pairs of data
    chartData_bus = OrderedDict()
    chartData_bus["Positive"] = positive_bus
    chartData_bus["Negative"] = negative_bus
    chartData_bus["Neutral"] = neutral_bus
    

    dataSource_bus["chart"] = chartConfig_bus
    dataSource_bus["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    #The data for the chart should be in an array wherein each element of the array
    #is a JSON object# having the `label` and `value` as keys.

    #Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData_bus.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource_bus["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D_bus = FusionCharts("pie2d", "myBusChart", "600", "400", "myBuschart-container", "json", dataSource_bus)


    #school chart
    #Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource_school = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig_school = OrderedDict()
    chartConfig_school["caption"] = "Sentiment Analysis with number of tweets"
    chartConfig_school["showlegend"] = "1",
    chartConfig_school["showpercentvalues"] = "1",
    chartConfig_school["usedataplotcolorforlabels"] = "1",
   

    # The `chartData` dict contains key-value pairs of data
    chartData_school = OrderedDict()
    chartData_school["Positive"] = positive_school
    chartData_school["Negative"] = negative_school
    chartData_school["Neutral"] = neutral_school
    
    dataSource_school["chart"] = chartConfig_school
    dataSource_school["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    #The data for the chart should be in an array wherein each element of the array
    #is a JSON object# having the `label` and `value` as keys.

    #Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData_school.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource_school["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D_school = FusionCharts("pie2d", "myschoolChart", "600", "400", "myschoolchart-container", "json", dataSource_school)

    total_positive_sentiment =  my_analysis_bus + my_analysis + my_analysis_school + positive_analysis_food + positive_analysis_safety + positive_analysis_health
    total_negative_sentiment =  negative_analysis_water + negative_analysis_bus + negative_analysis_school + negative_analysis_food + negative_analysis_safety + negative_analysis_health
    total_neutral_sentiment =  neutral_analysis_water + neutral_analysis_bus + neutral_analysis_school + neutral_analysis_food + neutral_analysis_health + neutral_analysis_safety

    context = {'num': x, 'water_pos_analysis': my_analysis, 'my_analysis_bus': my_analysis_bus,
    'my_analysis_school': my_analysis_school, 'negative_analysis_water': negative_analysis_water, 
    'negative_analysis_bus': negative_analysis_bus, 'negative_analysis_school': negative_analysis_school,
    'neutral_analysis_water': neutral_analysis_water, 'neutral_analysis_bus': neutral_analysis_bus,
    'neutral_analysis_school': neutral_analysis_school, 'positive_analysis_food': positive_analysis_food,
    'positive_analysis_safety': positive_analysis_safety, 'positive_analysis_health': positive_analysis_health,
    'negative_analysis_food': negative_analysis_food, 'negative_analysis_safety': negative_analysis_safety,
    'negative_analysis_health': negative_analysis_health, 'neutral_analysis_food': neutral_analysis_food,
    'neutral_analysis_health': neutral_analysis_health, 'neutral_analysis_safety': neutral_analysis_safety,
    'analyser': analyser, 'pos': positive, 'neg': negative, 'neu':neutral, 'positive_bus': positive_bus, 
    'negative_bus': negative_bus, 'neutral_bus':neutral_bus, 'positive_school': positive_school, 'negative_school': negative_school, 'neutral_school':neutral_school, 
    'positive_food': positive_food, 'negative_food': negative_food, 'neutral_food':neutral_food,
    'positive_safety': positive_safety, 'negative_safety': negative_safety, 'neutral_safety':neutral_safety,
    'positive_health': positive_health, 'negative_health': negative_health, 
    'neutral_health':neutral_health, 'total_positive':total_positive, 'total_negative':total_negative, 
    'total_neutral': total_neutral, 'total_positive_sentiment':total_positive_sentiment, 'total_negative_sentiment':total_negative_sentiment, 
    'total_neutral_sentiment':total_neutral_sentiment, 'output': column2D.render(), 'output_bus': column2D_bus.render(), 
    'output_school': column2D_school.render(), 'most_negative_tweet': most_negative_tweet, 
    'most_positive_tweet': most_positive_tweet, 'percent_positive': percent_positive, 'percent_negative': percent_negative,
    'percent_neutral': percent_neutral, 'percent_positive_bus': percent_positive_bus, 'percent_negative_bus': percent_negative_bus,
    'percent_neutral_bus': percent_neutral_bus, 'percent_positive_school': percent_positive_school, 'percent_negative_school': percent_negative_school,
    'percent_neutral_school': percent_neutral_school, 'percent_positive_food': percent_positive_food, 'percent_negative_food': percent_negative_food,
    'percent_neutral_food': percent_neutral_food, 'percent_positive_safety': percent_positive_safety, 'percent_negative_safety': percent_negative_safety,
    'percent_neutral_safety': percent_neutral_safety, 'percent_positive_health': percent_positive_health, 
    'percent_negative_health': percent_negative_health, 'percent_neutral_health': percent_neutral_health,
    'total_positive_percent': total_positive_percent, 'total_negative_percent': total_negative_percent,
    'total_neutral_percent': total_neutral_percent}

    return render(request, 'home.html', context)


