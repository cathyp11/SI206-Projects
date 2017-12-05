import unittest
import json
# import requests_oauthlib
import requests
import urllib.request
import facebook
import googlemaps
import gmplot
from yelpapi import YelpAPI
from instagram.client import InstagramAPI

access_token = "EAACEdEose0cBABWYcYmrXOHDowkN9sHueBgpD6KxOafhZCu9lfJRlwSykZCMBZBdYyckal3Hnp82ObwdbUoLD0C9zZCEuq2WLy8pkKvwLVI7zPp2Kkepsp2ZAB4W0cop9pQZC6g4uZCNPv0aDH7DU2ZBWBNdv4P4zpZAWCBrRLGQqNXZBta49VqtIkDFBeQSy61AKmlZBXU8GgSBwZDZD"

CACHE_FB = 'cache_fb.json'
CACHE_YELP = 'cache_yelp.json'

try:
    cache_file_fb = open(CACHE_FB, 'r')
    cache_file_yelp = open(CACHE_YELP, 'r')
    cache_contents_fb = cache_file_fb.read()
    cache_contents_yelp = cache_file_yelp.read()
    CACHE_DICTION_fb = json.loads(cache_contents_fb)
    CACHE_DICTION_yelp = json.loads(cache_contents_yelp)
    cache_file_fb.close()
    cache_file_yelp.close()
except:
    CACHE_DICTION_fb = {}
    CACHE_DICTION_yelp = {}

client_id = "jm2vtxy3cmHonLMgUgSz_Q"
client_secret = "BIpoyU7OGn8GQtmrA2065aIC8ec29AaHpQwIZ3nZWbZzFRds3ONdwyXf3NyWywoW"

inst_client_id = "c9858f0a1745445f96a68712078a9361"
inst_client_status = "946aee55e6b34980aac30f2fa44fef95"
# f38f5c54532e45febe53818643aeb766
inst_access_token = "511092312.c9858f0.d705094e52bf4ca78fc536ec117ced60"

yelp_access_token = "ztsjq_LquhhLU5ABi4zWOIOISD-jy8UiWijyAzLb0yV7MChsj3pLa6ZP6yruRkTdS6M2SRvm3olECWEx6GTsE1JLEDkkHWS5oyWYYYSFfbAodGQ0-NmJFQMshTATWnYx"
places_key = "AIzaSyCytCUed9RpF5GEmMl5t4Pakx_Asp3bTs0"
geo_key = "AIzaSyCRq7G6004a_ADdAf5MFE11NUU37GCIkuY"

def Caching_FB(user):
	if user in CACHE_DICTION_fb:
		print('using cache')
		data = CACHE_DICTION_fb[user]
	else:
		print('fetching')
		graph = facebook.GraphAPI(access_token)
		data = graph.search(type = 'page')
		CACHE_DICTION_fb[user] = data
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_fb)
		fw = open(CACHE_FB,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data

def Caching_Yelp():
	user = "FritaBatidos"
	if user in CACHE_DICTION_yelp:
		print('using cache')
		data_y = CACHE_DICTION_yelp[user]
	else:
		print('fetching')
		yelp_api = YelpAPI(client_id, client_secret)
		data_y = yelp_api.search_query(location="Ann Arbor")
		CACHE_DICTION_yelp[user] = data_y
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_yelp)
		fw = open(CACHE_YELP,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data_y


posts = Caching_FB("FritaBatidos")
print(posts)
# yelp = Caching_Yelp()
# print(yelp)

# yelp_api = YelpAPI(client_id, client_secret)
# # search_results = yelp_api.reviews_query(id = "frita-batidos-ann-arbor")
# print(search_results)

# gmaps = googlemaps.Client(key="AIzaSyC58NAR4Py-mZ0Dbj1QoZMF1sv4TP4rv6o")
# gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

# gmap.scatter(lat,lon, 'r', 0.1, marker=False)
# gmap.plot(37.428, -122.145, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

# gmap.draw("mymap.html")
# inst = InstagramAPI(access_token = inst_access_token, client_secret=inst_client_status)
# tags = inst.tag(tag_name = "FritaBatidos")
# # tags = inst.tag_recent_media(tag_name="snow")
# # tags = inst.tag("")
# print(tags)
# user = inst.media_popular(count=20)
# # user = inst.user(user_id = 'cathyyp11')
# print(user)

# baseurl_id = 'https://api.instagram.com/v1/tags/fritabatidos/media/recent?access_token=' + inst_access_token +'&min_tag_id=1387332980547'
# responses = urllib.request.urlopen(baseurl_id)
# jsonreads = responses.read()
# reads = json.loads(jsonreads)
# print(reads)
# 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city + '&key=' + places_key
# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=YOUR_API_KEY

# location = input('location: ')
# url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=' + geo_key

# url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=51.503186,-0.126446&radius=500&type=restaurant&key=' + places_key
# 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + 51.503186,-0.126446 + '&radius=500&type=restaurant&key=' + places_key

# url = "https://api.yelp.com/v3/businesses/search?term=restaurants&location=Ann+Arbor"
# response = urllib.request.urlopen(url)
# jsonread = response.read()
# read = json.loads(jsonread)
# print(read)
# print(read['results'][0]['geometry']['location'])

# url = "https://api.yelp.com/oauth2/token"
# response = requests.get(url, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
# jsonread = response.text
# print(jsonread)

#----------------------
# def Places_Reviews():
# 	placeids = []
# 	data_ids = []
# 	places = Caching_Places()
# 	if location in CACHE_DICTION_reviews:
# 		print('using cache')
# 		data_ids = CACHE_DICTION_reviews[location]
# 	else:
# 		for place in places['results']:
# 			placeids.append(place['place_id'])
# 		for placeid in placeids:
# 			places_ids_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + placeid +'&key=' + places_key
# 			places_ids_api = urllib.request.urlopen(places_ids_url)
# 			jsons = places_ids_api.read()
# 			data_ids.append(json.loads(jsons))
# 		CACHE_DICTION_reviews[location] = data_ids
# 		dumped_json_cache = json.dumps(CACHE_DICTION_reviews)
# 		fw = open(CACHE_Reviews, "w")
# 		fw.write(dumped_json_cache)
# 		fw.close()
# 	return data_ids
#-----------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
