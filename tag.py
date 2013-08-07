import pygame
#import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pytagcloud import create_tag_image, make_tags, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
from requests_oauthlib import OAuth1
import requests
import operator
#import pprint as pp
import string

#import numpy as np
from collections import Counter
#from sklearn.feature_extraction.text import CountVectorizer
query = 'chicago'

f=open('configuration.txt','rb')
my_secrets = lines = [line.strip() for line in f]
my_oauth = OAuth1(my_secrets[0],
                  client_secret=my_secrets[1],
                  resource_owner_key=my_secrets[2],
                  resource_owner_secret=my_secrets[3])

complete_url = 'https://api.twitter.com/1.1/search/tweets.json?q='+query+'&count=100'

tweets_words = [query, 'http', 'amp']
stop_words = [
'a',
'about',
'above',
'after',
'again',
'against',
'all',
'am',
'an',
'and',
'any',
'are',
"aren't",
'as',
'at',
'be',
'because',
'been',
'before',
'being',
'below',
'between',
'both',
'but',
'by',
"can't",
'cannot',
'could',
"couldn't",
'did',
"didn't",
'do',
'does',
"doesn't",
'doing',
"don't",
'down',
'during',
'each',
'few',
'for',
'from',
'further',
'had',
"hadn't",
'has',
"hasn't",
'have',
"haven't",
'having',
'he',
"he'd",
"he'll",
"he's",
'her',
'here',
"here's",
'hers',
'herself',
'him',
'himself',
'his',
'how',
"how's",
'i',
"i'd",
"i'll",
"i'm",
"i've",
'if',
'in',
'into',
'is',
"isn't",
'it',
"it's",
'its',
'itself',
"let's",
'me',
'more',
'most',
"mustn't",
'my',
'myself',
'no',
'nor',
'not',
'of',
'off',
'on',
'once',
'only',
'or',
'other',
'ought',
'our',
'ours',
'ourselves',
'out',
'over',
'own',
'same',
"shan't",
'she',
"she'd",
"she'll",
"she's",
"should",
"shouldn't",
'so',
'some',
'such',
'than',
'that',
"that's",
'the',
'their',
'theirs',
'them',
'themselves',
'then',
'there',
"there's",
'these',
'they',
"they'd",
"they'll",
"they're",
"they've",
'this',
'those',
'through',
'to',
'too',
'under',
'until',
'up',
'very',
'was',
"wasn't",
'we',
"we'd",
"we'll",
"we're",
"we've",
'were',
"weren't",
'what',
"what's",
'when',
"when's",
'where',
"where's",
'which',
'while',
'who',
"who's",
'whom',
'why',
"why's",
'with',
"won't",
'would',
"wouldn't",
'you',
"you'd",
"you'll",
"you're",
"you've",
'your',
'yours',
'yourself',
'yourselves ',

]

stop_words+=tweets_words        
#plt.ion()
exclude = set(string.punctuation) 
#plt.show()
while True:
	my_text=''
	r = requests.get(complete_url, auth=my_oauth)
	tweets = r.json()
	#pp.pprint (tweets['statuses'][1]['text'])
	for tweet in tweets['statuses']:
		#print type(tweet['text'])
		text=tweet['text'].lower()
		text = ''.join(ch for ch in text if ch not in exclude)
		#print unicode(text).encode('utf-8')
		important_words = text
		my_text+=important_words
	# f = open("my_text.txt")
	# lines = f.readlines()

	# my_text = ' '.join(lines)
	words = my_text.split()
	
	counts = Counter(words)  
	for word in stop_words:
		del counts[word]

	#words = np.array(cv.get_feature_names()) 
	# normalize                                                                                                                                             
	#counts = counts / float(counts.max())
	for key in counts.keys():
		if len(key)<3 or key.startswith('http'):
			del counts[key]
	final = counts.most_common(180)
	#print final
	max_count = max(final, key=operator.itemgetter(1))[1]
	print "eccolo"
	final = [(name,count/float(max_count))for name,count in final]
	print max_count
	# for items in final:
	# 	print items[1]/float(max_count)
	#  	items[1]=items[1]/float(max_count)
	tags = make_tags(final, maxsize=80)

	create_tag_image(tags, 'cloud_large.png', size=(1280, 800), layout=3, fontname='Lobster', background = (255,255,255))
	print "created"
	
	#img=mpimg.imread('cloud_large.png')
	#imgplot = plt.imshow(img)
	#plt.draw()
	#plt.pause(5)
