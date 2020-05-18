# Python script - Tokens Frequency Local

'''
SCRIPT HANDLES:

1. Tokenization and Cleaning text of tweets with NLTK:
    clean_tokens -    the function takes 'body' column from CSV file,
                      cleans whole text and splits into ONE List of tokens.
    clean_sentences - the function works in the same way as 'clean_tokens',
                      but the output is a list of lists of tweets (every list = row in column 'body')

2. Counting words in a file using Counter Object:
    count_common_words - the function counts common tokens from a list
    count_common_words_no_dup - the function counts common tokens from a list without the duplicates
'''
## Libraries
import collections
import pandas as pd
#from Lib import csv
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

## Script Functions:
def clean_tokens (body_column_list):
    global words
    tweets_string = ' '.join([str(elem) for elem in body_column_list])   # Convert a list to string using list comprehension
    tokens = word_tokenize(tweets_string)   # Split into words
    tokens = [w.lower() for w in tokens]    # Convert to lower case

    # string.punctuation - provides a great list of punctuation characters.
    # example (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    # maketrans() to create a mapping table
    table = str.maketrans('', '', string.punctuation)   # Remove punctuation from each word
    stripped = [w.translate(table) for w in tokens]     # Remove tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]   # Iterating over all tokens and only
                                                            # keeping those tokens that are all alphabetic
    stop_words = set(stopwords.words('english') + ['rt', 'via', 'http', 'https', 'co', 'like',
                                                   'amp', 'na', 'lol', 'shit', 'u', 'ca']) # Filter out stop words
    words = [w for w in words if not w in stop_words]
    # print(words[:])

def clean_sentences(body_column_list):
    sentences = []
    for el in body_column_list:
        sub = el.split(', ')
        sentences.append(sub)
    for nl in sentences:
        #print(*nl)
        tweets_string = ' '.join([str(elem) for elem in nl])
        tokens = word_tokenize(tweets_string)
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words_by_sent = [word for word in stripped if word.isalpha()]
        stop_words = set(stopwords.words('english') + ['rt', 'via', 'http', 'https', 'co', 'like',
                                                       'amp', 'na', 'lol', 'shit', 'u', 'ca'])
        words_by_sent = [w for w in words_by_sent if not w in stop_words]
        tweets_sentences.append(words_by_sent)
        # print(words_by_sent[:])
        # print()
    return (sentences)

def count_common_words (tokens):
    global word_counter
    common_words = int(input("\nHow many most common words to print: "))
    print("\nOK. The {} most common words are as follows:\n".format(common_words))
    word_counter = collections.Counter(tokens)
    for word, count in word_counter.most_common(common_words):
        print(word, ": ", count)

def count_common_words_no_dup (tokens):
    global word_counter_no_dup
    common_words = int(input("\nHow many most common words to print: "))
    print("\nDuplicates removed. The {} most common words are as follows:\n".format(common_words))
    word_counter_no_dup = collections.Counter(tokens)
    for word, count in word_counter_no_dup.most_common(common_words):
        print(word, ": ", count)


## Local Variables:
#csv_file = pd.read_csv(r'D:\Research_Assistant\DataBase\TokensFrequencyDebug\Test.csv',  delimiter=',')
path = r'D:\Research_Assistant\DataBase\TokensFrequencyDebug\Test.csv'
path_split = path.split('.')
path_new = path_split[0] + '_Report.csv'
df = pd.read_csv(path, delimiter=',')

tweets_body = df.body.tolist()
tweets_sentences = []
no_duplicates_listOfList = []

filename = 'CountReport.csv'
header = ('CommonTokens', 'RawCount', 'NoDupTokens', 'NoDupCount')

try:
    clean_tokens(tweets_body)
    print('\nDone: Tweets are cleaned and separated into list of tokens.')

    count_common_words(words)   # Raw count all most common words in 'body' column (by tokens)

    clean_sentences(tweets_body)
    print('\nDone: Tweets are cleaned and separated into list of lists of tokens.')

    # Removing duplicates:
    for nl in tweets_sentences:
        temp_list = []
        #print(nl)
        for i in range(len(nl)):
            if nl[i] not in nl[i + 1:]:
                temp_list.append(nl[i])
        no_duplicates_listOfList.append(temp_list)
        #print(temp_list)
    print('\nDone: Removing duplicates completed.')

    # Convert list of lists to flat list & count without duplicates per tweets
    no_duplicates_list = [ item for elem in no_duplicates_listOfList for item in elem]
    count_common_words_no_dup(no_duplicates_list)

    # df.to_csv(path_new)
    # print('\nDone: CSV Report saved')

except OSError as e:
    print('OS error: {0}'.format(e))
except IOError as e:
    print('I/O error({0}): {1}'.format(e.errno, e.strerror))
except ValueError as e:
    print('Value error: ' + e.args[0])
except Exception as e:
    print('Unexpected error: ' + e.args[0])