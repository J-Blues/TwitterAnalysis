import collections
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

# Read a CSV file using pandas module
csv_file = pd.read_csv(r'D:\Research_Assistant\DataBase\Test.csv')
tweets_body = csv_file.body.tolist()
#print(tweets_body)

# Convert a list to string using list comprehension
tweets_string = ' '.join([str(elem) for elem in tweets_body])
#print("List to string: \n"+ tweets_string)

# Split into words
tokens = word_tokenize(tweets_string)

# Convert to lower case
tokens = [w.lower() for w in tokens]

# Remove punctuation from each word
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

# Remove tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]

# Filter out stop words
stop_words = set(stopwords.words('english') + ['rt', 'via', 'http','https','co'])
words = [w for w in words if not w in stop_words]
#print(words[:])

# Print most common word
common_words = int(input("How many most common words to print: "))
print("\nOK. The {} most common words are as follows:\n".format(common_words))

word_counter = collections.Counter(words)
for word, count in word_counter.most_common(common_words):
    print(word, ": ", count)

# Draw a Bar Chart
bar_chart = word_counter.most_common(common_words)
