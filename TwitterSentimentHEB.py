# Python script - Twitter Sentiment Analysis with Vader

'''
SOURCE:
https://towardsdatascience.com/almost-real-time-twitter-sentiment-analysis-with-tweep-vader-f88ed5b93b1c
https://github.com/Mjrovai/Python4DS/blob/master/Almost_Real_Time_Twitter_Sentiment_Analysis/almost_real_time_twitter_sentiment_analysis_EXT.ipynb
by Marcelo Rovai

SCRIPT HANDLES:
1. Text cleaning by removing twitter handles, Return handles (RT @xxx:, @xxx), URL links (httpxxx) etc.
2. Translating text from its original language to English by using Google Translate API
3. Sentiment analysis of any text using Vader (Valence Aware Dictionary and sEntiment Reasoner)
4. Output a CSV Report of all enqueued script handles
'''
## Libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd
import numpy as np
import re


## Script Functions:
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

def clean_tweets(lst):
    '''
    DOCSTRING:
    1. Removing twitter Return handles (RT @xxx:)
    2. Removing twitter handles (@xxx)
    3. Removing URL links (httpxxx)
    4. Removing special characters, numbers, punctuations (except for #)

    INPUT: 'Text' column from data frame + remove_pattern function
    OUTPUT: The result - new column in data frame 'clear_text'
    '''
    clean_tweets_text = []
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    clean_tweets_text.append(lst)
    return lst

def eng_translation(lst):
    for index, row in lst.iteritems():
        translator = Translator()
        try:
            translated = translator.translate(row, dest='en') # translate the 'text' column
            trans = translated.text
        except Exception as e:
            print(str(e))
        translatedList.append(trans)

def sentiment_analyzer_scores(translated_text):
    '''
    DOCSTRING:
    1. Polarity_scores() method to obtain the polarity indices for the given sentence.
    2. If-elif-else statement for getting Compound score
    '''
    score = analyser.polarity_scores(translated_text)
    sentimentScore.append(score)
    #print(score)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1

def anl_tweets(translated_text):
    '''
    DOCSTRING: For loop Runs trow Translated list of tweets.
    INPUT: Translated list of tweets + sentiment_analyzer_scores function
    OUTPUT:
    1. The result will be a dictionary {'compound': value, 'neg': value, 'neu': value, 'pos': value} per tweet
    2. Compound score Compound score has a range of [-1, 1]:
        [-1 to 0): negative
        [0]: neutral
        (0 to +1]: positive

    '''
    sents = []
    for tw in translated_text:
        try:
            st = sentiment_analyzer_scores(tw)
            sents.append(st)
        except:
            sents.append(0)
    return sents

def splitLatLong(coordinates):
    '''
    DOCSTRING:
    1. Runs in thru CSV file 'Coordinates' column and checks if value exist:
       ({'type': 'Point', 'coordinates': [34.7667, 32.0667]})
    2. If-elif-else statement executes longitude and latitude
    '''
    for value in dict(coordinates).values():
        if type(value) is float:
            lon.append(np.NaN)
            lat.append(np.NaN)
        elif type(value) is np.float64:
            lon.append(np.NaN)
            lat.append(np.NaN)
        else:
            bracketStartIndex = value.find('[')
            bracketStopIndex = value.find(']')
            values = value[bracketStartIndex+1:bracketStopIndex].split(",")
            lon.append(values[0])
            lat.append(values[1])

## Local Variables
path = r'D:\Research_Assistant\DataBase\COVID\TestHEB_8Bit.csv'
path_split = path.split('.')
path_new = path_split[0] + '_Report.csv'
df = pd.read_csv(path)
analyser = SentimentIntensityAnalyzer()

translatedList = []
sentimentScore = []
lat = []
lon = []


try:
    df['text'] = df['text'].str.replace('[^\w\s#@/:%.,_-]', '', flags=re.UNICODE)
    print('\nDone: Emojis have been removed from [text] column.')

    df['clear_text'] = clean_tweets(df['text'])
    print('\nDone: Clean Tweets function completed.')

    eng_translation(df['clear_text'])
    df['eng_text'] = translatedList
    print('\nDone: Translation completed and saved to CSV report.')

    df['sentiment'] = anl_tweets(translatedList)
    print('\nDone: The new column  [sentiment] created.')

    score_update = pd.DataFrame(sentimentScore)
    df['negative'] = (score_update['neg'])
    df['neutral'] = (score_update['neu'])
    df['positive'] = (score_update['pos'])
    df['compound'] = (score_update['compound'])
    print('\nDone: Sentiment Analysis completed. Results have been saved to the new columns [negative, neutral, positive, compound].')

    splitLatLong(df['coordinates'])
    df['longitude'] = lon
    df['latitude'] = lat
    print('\nDone: Coordinates column has been split into [longitude] and [latitude] columns.')

    df.to_csv(path_new)
    print('\nDone: CSV Report saved.')

except OSError as e:
    print('OS error: {0}'.format(e))
except IOError as e:
    print('I/O error({0}): {1}'.format(e.errno, e.strerror))
except ValueError as e:
    print('Value error: ' + e.args[0])
except Exception as e:
    print('Unexpected error: ' + e.args[0])