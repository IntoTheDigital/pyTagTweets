from pytagcloud import create_tag_image, make_tags, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
from requests_oauthlib import OAuth1
import requests
import operator
from collections import Counter
import time

query = 'chicago'
limit = 200
layout = 3
background_color = (255, 255, 255)
max_word_size = 80
max_words = 180
wait_time = 10  # time interval between two tag clouds are created in seconds

f = open('stopwords.txt', 'rb')
stop_words = [line.strip() for line in f]  # loading common English stopwords from file
tweets_words = [query, '#' + query, 'http', 'amp']  # common words in tweets
stop_words += tweets_words  # add common words in tweets to stopwords
punctuation = "!\"$%&'()*+,-./:;<=>?[\]^_`{|}~'"  # characters exluded from tweets

f = open('configuration.txt', 'rb')
my_secrets = [line.strip() for line in f]

my_oauth = OAuth1(my_secrets[0],
                  client_secret=my_secrets[1],
                  resource_owner_key=my_secrets[2],
                  resource_owner_secret=my_secrets[3])

complete_url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + query + '&count=' + str(limit)

while True:
    my_text = ''
    r = requests.get(complete_url, auth=my_oauth)
    tweets = r.json()
    for tweet in tweets['statuses']:
        text = tweet['text'].lower()
        text = ''.join(ch for ch in text if ch not in punctuation)  # exclude punctuation from tweets
        important_words = text
        my_text += important_words

    words = my_text.split()
    counts = Counter(words)
    for word in stop_words:
        del counts[word]

    for key in counts.keys():
        if len(key) < 3 or key.startswith('http'):
            del counts[key]

    final = counts.most_common(max_words)
    max_count = max(final, key=operator.itemgetter(1))[1]
    final = [(name, count / float(max_count))for name, count in final]
    tags = make_tags(final, maxsize=max_word_size)
    create_tag_image(tags, 'cloud_large.png', size=(1280, 800), layout=layout, fontname='Lobster', background = background_color)
    print "new png created"
    time.sleep(wait_time)
