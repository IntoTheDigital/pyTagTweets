#import pygame
from pytagcloud import create_tag_image, make_tags, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
from requests_oauthlib import OAuth1
import requests
import operator
import string
from collections import Counter

query = 'chicago'
limit = 100

f=open('configuration.txt','rb')
my_secrets = [line.strip() for line in f]
my_oauth = OAuth1(my_secrets[0],
                  client_secret=my_secrets[1],
                  resource_owner_key=my_secrets[2],
                  resource_owner_secret=my_secrets[3])

complete_url = 'https://api.twitter.com/1.1/search/tweets.json?q='+query+'&count='+str(limit)

f=open('stopwords.txt','rb')
tweets_words = [query, 'http', 'amp']
stop_words = [line.strip() for line in f]
stop_words+=tweets_words        
exclude = set(string.punctuation.replace('#','').replace('@',''))

while True:
	my_text=''
	r = requests.get(complete_url, auth=my_oauth)
	tweets = r.json()
	for tweet in tweets['statuses']:
		text=tweet['text'].lower()
		text = ''.join(ch for ch in text if ch not in exclude)
		important_words = text
		my_text+=important_words

	words = my_text.split()
	counts = Counter(words)  
	for word in stop_words:
		del counts[word]

	for key in counts.keys():
		if len(key)<3 or key.startswith('http'):
			del counts[key]

	final = counts.most_common(180)
	max_count = max(final, key=operator.itemgetter(1))[1]
	final = [(name,count/float(max_count))for name,count in final]
	tags = make_tags(final, maxsize=80)
	create_tag_image(tags, 'cloud_large.png', size=(1280, 800), layout=3, fontname='Lobster', background = (255,255,255))
	print "new png created"