import unittest
import json
import requests
import urllib.request
import datetime
import sqlite3
import re
import plotly.tools as tl
import plotly.plotly as py
import plotly.graph_objs as go
from os import path
from wordcloud import WordCloud
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Cathy Park
## SI 206 Project 4

yelp_access_token = "ztsjq_LquhhLU5ABi4zWOIOISD-jy8UiWijyAzLb0yV7MChsj3pLa6ZP6yruRkTdS6M2SRvm3olECWEx6GTsE1JLEDkkHWS5oyWYYYSFfbAodGQ0-NmJFQMshTATWnYx"
places_key = "AIzaSyCytCUed9RpF5GEmMl5t4Pakx_Asp3bTs0"
geo_key = "AIzaSyCRq7G6004a_ADdAf5MFE11NUU37GCIkuY"
fb_access_token = '135756800477398|anRtlRbE9MHfxKAZ5RjfTybAP2M'
youtube_key = 'AIzaSyDBaXk0D9-fzmUuW3iZgIwLafqpK62Q6xg'
plotly_key = '18abIcoRKRsQn5hIBvDN'

tl.set_credentials_file(username='cathyy11', api_key=plotly_key)

CACHE_YELP = 'cache_yelp.json'
CACHE_PLACES = 'cache_places.json'
CACHE_Reviews = 'cache_reviews.json'
CACHE_Geo = 'cache_geo.json'
CACHE_FB = 'cache_fb.json'
CACHE_YT = 'cache_yt.json'

try:
    # cache_file_places = open(CACHE_PLACES, 'r')
    # cache_contents_places = cache_file_places.read()
    # CACHE_DICTION_places = json.loads(cache_contents_places)
    # cache_file_places.close()

    cache_file_yelp = open(CACHE_YELP, 'r')
    cache_contents_yelp = cache_file_yelp.read()
    CACHE_DICTION_yelp = json.loads(cache_contents_yelp)
    cache_file_yelp.close()
except:
    # CACHE_DICTION_places = {}
    CACHE_DICTION_yelp = {}

try:
	cache_file_geo = open(CACHE_Geo, 'r')
	cache_contents_geo = cache_file_geo.read()
	CACHE_DICTION_geo = json.loads(cache_contents_geo)
	cache_file_geo.close()
except:
	CACHE_DICTION_geo = {}

try:
	cache_file_places = open(CACHE_PLACES, 'r')
	cache_contents_places = cache_file_places.read()
	CACHE_DICTION_places = json.loads(cache_contents_places)
	cache_file_places.close()
except:
	CACHE_DICTION_places = {}

try:
	cache_file_reviews = open(CACHE_Reviews, 'r')
	cache_contents_reviews = cache_file_reviews.read()
	CACHE_DICTION_reviews = json.loads(cache_contents_reviews)
	cache_file_reviews.close()
except:
	CACHE_DICTION_reviews = {}

try:
	cache_file_fb = open(CACHE_FB, 'r')
	cache_contents_fb = cache_file_fb.read()
	CACHE_DICTION_fb = json.loads(cache_contents_fb)
	cache_file_fb.close()
except:
	CACHE_DICTION_fb = {}

try:
	cache_file_yt = open(CACHE_YT, 'r')
	cache_contents_yt = cache_file_yt.read()
	CACHE_DICTION_yt = json.loads(cache_contents_yt)
	cache_file_yt.close()
except:
	CACHE_DICTION_yt = {}


location = "ann arbor"

## Caching Data

def Caching_Yelp():
	# using 2 urls to gain 100 datasets because Yelp limits to 50 datasets at once
	# url2 accesses the information in 2nd page
	url = "https://api.yelp.com/v3/businesses/search?term=restaurants&limit=50&sort_by=rating&location=" + location 
	url2 = "https://api.yelp.com/v3/businesses/search?term=restaurants&limit=50&offset=100&sort_by=rating&location=" + location
	if location in CACHE_DICTION_yelp:
		print('using cache yelp')
		data_y = CACHE_DICTION_yelp[location]
	else:
		print('fetching yelp')
		yelp_api = requests.get(url, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
		yelp_api2 = requests.get(url2, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
		data_y = json.loads(yelp_api.text)
		data_y2 = json.loads(yelp_api2.text)
		# adding 2nd page data to 1st page data to make one dataset
		for d in data_y2['businesses']:
			data_y['businesses'].append(d)
		CACHE_DICTION_yelp[location] = data_y
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_yelp)
		fw = open(CACHE_YELP,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data_y


def Caching_Location():
	# Cache Google Maps data using address from Cached Yelp
	restaurants = Caching_Yelp()
	addresses = []
	data_geo = []
	if location in CACHE_DICTION_geo:
		print('using cache geolocation')
		data_geo = CACHE_DICTION_geo[location]
	else:
		print('fetching geolcation')
		# pulling street address and city from Yelp data 
		# finding latitudes and longitudes from Google Maps
		for i in restaurants['businesses']:
			addresses.append(i['location']['address1'] + ' ' + i['location']['city'])
		for ad in addresses:
			loc = ad.replace(" ", "+")
			geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '&key=' + geo_key
			req = urllib.request.urlopen(geo_url)
			read = req.read()
			data_geo.append(json.loads(read))
		CACHE_DICTION_geo[location] = data_geo
		dumped_json_cache = json.dumps(CACHE_DICTION_geo)
		fw = open(CACHE_Geo, "w")
		fw.write(dumped_json_cache)
		fw.close()
	return data_geo

def Geocode():
	g = Caching_Location()
	geocodes = []
	# save latitudes and longitudes from Google Maps in a list of tuples called geocodes 
	for l in g:
		lat = str(l['results'][0]['geometry']['location']['lat'])
		lng = str(l['results'][0]['geometry']['location']['lng'])
		geocodes.append((lat, lng))
	return geocodes

def Caching_Places():
	# Cache Google Places information about restaurants in cached Yelp data. 
	# Use the geocodes to find more information about the restaurants in Google Places.
	geo = Geocode()
	data_p = []
	if location in CACHE_DICTION_places:
		print('using cache places')
		data_p = CACHE_DICTION_places[location]
	else:
		print('fetching places')
		for g in geo:
			places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + g[0] + "," + g[1] + '&radius=500&type=restaurant&key=' + places_key
			places_api = urllib.request.urlopen(places_url)
			jsonread = places_api.read()
			data_p.append(json.loads(jsonread))
		CACHE_DICTION_places[location] = data_p
		dumped_json_cache = json.dumps(CACHE_DICTION_places)
		fw = open(CACHE_PLACES, "w")
		fw.write(dumped_json_cache)
		fw.close()
	return data_p


def Yelp_Reviews():
	# Caching reviews for 100 restaurants from cached Yelp data. 
	# Yelp API allows 3 reviews by default, thus creates 300 datasets of reviews.
	d = Caching_Yelp()
	data_reviews = []
	yelp_ids = []
	if location in CACHE_DICTION_reviews:
		print('using cache reviews from yelp')
		data_reviews = CACHE_DICTION_reviews[location]
	else:
		print('fetching reviews from yelp')
		# fetching information from Caching_Yelp() for business ids of restaurants
		for i in d['businesses']:
			yelp_ids.append(i['id'])
		for ids in yelp_ids:
			yelp_reviews_url = 'https://api.yelp.com/v3/businesses/' + ids + '/reviews' 
			yelp_reviews = requests.get(yelp_reviews_url, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
			data_reviews.append(json.loads(yelp_reviews.text))
		CACHE_DICTION_reviews[location] = data_reviews
		dumped_json_cache = json.dumps(CACHE_DICTION_reviews)
		fw = open(CACHE_Reviews, "w")
		fw.write(dumped_json_cache)
		fw.close()
	return data_reviews

def Caching_Fb(user):
	if user in CACHE_DICTION_fb:
		print('using cache facebook')
		data_fb = CACHE_DICTION_fb[user]
	else:
		print('fetching facebook')
		fb_url = 'https://graph.facebook.com/v2.11/' + user + '/feed?limit=100&access_token=' + fb_access_token
		req = urllib.request.urlopen(fb_url)
		read = req.read()
		data_fb = json.loads(read)
		CACHE_DICTION_fb[user] = data_fb
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_fb)
		fw = open(CACHE_FB,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data_fb

def Caching_Youtube(user):
	if user in CACHE_DICTION_yt:
		print('using cache youtube')
		data_youtube = CACHE_DICTION_yt[user]
	else:
		print('fetching youtube')
		you_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q=' + user + '&key=' + youtube_key
		req = urllib.request.urlopen(you_url)
		read = req.read()
		data_youtube = json.loads(read)
		CACHE_DICTION_yt[user] = data_youtube
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_yt)
		fw = open(CACHE_YT,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data_youtube


## Database 

conn = sqlite3.connect('restaurants.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Restaurants_Yelp')
cur.execute('DROP TABLE IF EXISTS Restaurants_Places')
cur.execute('DROP TABLE IF EXISTS Reviews')
cur.execute('DROP TABLE IF EXISTS Geocode')
cur.execute('DROP TABLE IF EXISTS Facebook_Posts')
cur.execute('DROP TABLE IF EXISTS Youtube_Posts')
cur.execute('''CREATE TABLE Restaurants_Yelp (id TEXT PRIMARY KEY, name TEXT, city TEXT, address TEXT, review_counts INT, rating DECIMAL, lat DECIMAL, lng DECIMAL)''')
cur.execute('''CREATE TABLE Restaurants_Places (id TEXT, name TEXT, address TEXT, lat DECIMAL, lng DECIMAL)''')
cur.execute('''CREATE TABLE Reviews (id TEXT REFERENCES Restaurant_Yelp(id), reviewer TEXT, rating DECIMAL, review TEXT, time_created DATETIME, day TEXT)''')
cur.execute('''CREATE TABLE Geocode (id TEXT REFERENCES Restaurants_Places(id), address TEXT, lat DECIMAL, lng DECIMAL)''')
cur.execute('''CREATE TABLE Facebook_Posts (post_id TEXT PRIMARY KEY, post TEXT, created_time DATETIME)''')
cur.execute('''CREATE TABLE Youtube_Posts (channel_id TEXT, channel_title TEXT, title TEXT, description TEXT, created_time DATETIME)''')


businesses = Caching_Yelp()
for business in businesses['businesses']:
	yelp_tup = (business['id'], business['name'], business['location']['city'], business['location']['address1'], business['review_count'], business['rating'], business['coordinates']['latitude'], business['coordinates']['longitude'])
	cur.execute('''INSERT INTO Restaurants_Yelp (id, name, city, address, review_counts, rating, lat, lng) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (yelp_tup[0], yelp_tup[1], yelp_tup[2], yelp_tup[3], yelp_tup[4], yelp_tup[5], yelp_tup[6], yelp_tup[7]))

places = Caching_Places()
for i in range(len(places)):
	for j in range(len(places[i]['results'])):
		place = places[i]['results'][j]
		places_tup = (place['place_id'], place['name'], place['vicinity'], place['geometry']['location']['lat'], place['geometry']['location']['lng'])
		cur.execute('''INSERT INTO Restaurants_Places (id, name, address, lat, lng) VALUES (?, ?, ?, ?, ?)''', (places_tup[0], places_tup[1], places_tup[2], places_tup[3], places_tup[4]))

reviews = Yelp_Reviews()
date_format = "%Y-%m-%d %H:%M:%S"
for i in range(len(reviews)):
	for j in reviews[i]['reviews']:
		reviews_tup = (re.findall(r'biz\/([^\?]+)', j['url'])[0], j['user']['name'], j['rating'], j['text'], j['time_created'])
		# find the day of week using datetime
		b = datetime.datetime.strptime(j['time_created'], date_format)
		s = b.strftime('%A')
		cur.execute('''INSERT INTO Reviews (id, reviewer, rating, review, time_created, day) VALUES (?, ?, ?, ?, ?, ?)''', (reviews_tup[0], reviews_tup[1], reviews_tup[2], reviews_tup[3], reviews_tup[4], s))

geo = Caching_Location()
for g in geo:
	ids = g['results'][0]['place_id']
	address = g['results'][0]['formatted_address']
	lat = g['results'][0]['geometry']['location']['lat']
	lng = g['results'][0]['geometry']['location']['lng']
	cur.execute('''INSERT INTO Geocode (id, address, lat, lng) VALUES (?,?,?,?)''', (ids, address, lat, lng))

fb = Caching_Fb('FritaBatidos')
for f in fb['data']:
	ids = f['id']
	if 'message' in f:
		posts = f['message']
	else:
		posts = f['story']
	times = f['created_time']
	cur.execute('''INSERT INTO Facebook_Posts (post_id, post, created_time) VALUES (?, ?, ?)''', (ids, posts, times))

yt = Caching_Youtube('FritaBatidos')
for i in range(len(yt['items'])):
	y = yt['items'][i]['snippet']
	yt_tup = (y['channelId'], y['channelTitle'], y['title'], y['description'], y['publishedAt'])
	cur.execute('''INSERT INTO Youtube_Posts (channel_id, channel_title, title, description, created_time) VALUES (?, ?, ?, ?, ?)''', (yt_tup[0], yt_tup[1], yt_tup[2], yt_tup[3], yt_tup[4]))

conn.commit()


## Visualization 1 - Word Cloud

# writing describing_words.txt that describes the restaurants from Yelp
ye = Caching_Yelp()
# words = []
# for r in ye['businesses']:
# 	for i in range(len(r['categories'])):
# 		words.append(r['categories'][i]['alias'])
# f = open('describing_words.txt','w')
# for word in words:
# 	f.write(word + "\n")
# f.close()

# creating a word cloud from describing_words.txt
# d = path.dirname(__file__)
# text = open(path.join(d, 'describing_words.txt')).read()
# wordcloud = WordCloud(scale=2).generate(text)
# wordcloud.to_file(path.join(d, 'describing_words.png'))
# image = wordcloud.to_image()
# image.show()
		

## Visualization 2 - Bar Graph
# plotting a bar graph of keywords that describe the restaurants from Google Places
# p = Caching_Places()
# dic = {}
# for i in range(len(p)):
# 	for j in range(len(p[i]['results'])):
# 		for k in p[i]['results'][j]['types']:
# 			if k in dic:
# 				dic[k] += 1
# 			else:
# 				dic[k] = 1
# plotting = [go.Bar(x = list(dic.keys()), y = list(dic.values()))]
# py.iplot(plotting, filename='categories')

## Visualization 3 - Boxplot
# plotting a boxplot with the ratings from Yelp Reviews
ratings = []
for r in ye['businesses']:
	ratings.append(r['rating'])
print(ratings)
with open('rating.csv', 'w') as f:
	writer = csv.writer(f, lineterminator = "\n")
	writer.writerow(['ratings'])
	for ra in ratings:
		writer.writerow([ra])
sns.set(style = "ticks")
ratings = pd.read_csv('rating.csv')
sns.boxplot(data=ratings).set_title('Ratings from Yelp')
plt.show()


cur.close()
conn.close()


########### UNIT TEST ############


class Caching(unittest.TestCase):
	def test_cache_yelp(self):
		fl = open('cache_yelp.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('ann arbor' in data)
	def test_cache_geo(self):
		fl = open('cache_geo.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('ann arbor' in data)
	def test_cache_places(self):
		fl = open('cache_places.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('ann arbor' in data)
	def test_cache_reviews(self):
		fl = open('cache_reviews.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('ann arbor' in data)
	def test_cache_fb(self):
		fl = open('cache_fb.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('FritaBatidos' in data)
	def test_cache_yt(self):
		fl = open('cache_yt.json','r')
		data = fl.read()
		fl.close()
		self.assertTrue('FritaBatidos' in data)

	

class GeocodeFuction(unittest.TestCase):
	def test_geocode1(self):
		g = Geocode()
		self.assertEqual(type(g), type([]))
	def test_geocode2(self):
		g = Geocode()
		self.assertEqual(type(g[1]), type(()))
	
						
if __name__ == '__main__':
    unittest.main(verbosity=2)

