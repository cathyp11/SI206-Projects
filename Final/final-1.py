import unittest
import json
import requests_oauthlib
import requests
import facebook
import googlemaps
import gmplot
from yelpapi import YelpAPI

access_token = "EAACEdEose0cBAKw7GnslIZAxtunTV7NOemxJHN3laxhAOvEW1jxvCzUQAv4LfLHM6Dm4OuF2zSCcZAK46Rgri6p0RBwPUL5OtKzpp450woWNEWX83aEyMzOCZCOZAj1u84lIR9VEz8PmOmyuylayto0hP1EjsCf1tNy0hL7NLtCBJ78M02jrrkKJv3gHz0q60m9qMYwYMAZDZD"

CACHE_FB = 'cache_fb.json'
CACHE_YELP = 'cache_yelp.json'

try:
    cache_file_fb = open(CACHE_FB, 'r')
    cache_file_yelp = open(CACHE_YELP, 'r')
    cache_contents_fb = cache_file_fb.read()
    cache_contents_yelp = cache_file_yemp.read()
    CACHE_DICTION_fb = json.loads(cache_contents_fb)
    CACHE_DICTION_yelp = json.loads(cache_contents_yelp)
    cache_file_fb.close()
    cache_file_yelp.close()
except:
    CACHE_DICTION_fb = {}
    CACHE_DICTION_yelp = {}

client_id = "jm2vtxy3cmHonLMgUgSz_Q"
client_secret = "BIpoyU7OGn8GQtmrA2065aIC8ec29AaHpQwIZ3nZWbZzFRds3ONdwyXf3NyWywoW"


def Caching_FB(user):
	if user in CACHE_DICTION_fb:
		print('using cache')
		data = CACHE_DICTION_fb[user]
	else:
		print('fetching')
		graph = facebook.GraphAPI(access_token)
		data = graph.get_object(id=user, fields='posts')
		CACHE_DICTION_fb[user] = data
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_fb)
		fw = open(CACHE_FB,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data

# def Caching_Yelp():
# 	user = "FritaBatidos"
# 	if user in CACHE_DICTION_yelp:
# 		print('using cache')
# 		data_y = CACHE_DICTION_yelp[user]
# 	else:
# 		print('fetching')
# 		yelp_api = YelpAPI(client_id, client_secret)
# 		search_results = yelp_api.search_query(location="Ann Arbor")
# 		CACHE_DICTION_yelp[user] = data_y
# 		# dump the existing cached data
# 		dumped_json_cache = json.dumps(CACHE_DICTION_yelp)
# 		fw = open(CACHE_YELP,"w")
# 		fw.write(dumped_json_cache)
# 		fw.close() # Close the open file
# 	return data_y


posts = Caching_FB("FritaBatidos")
print(posts)
# yelp = Caching_Yelp()
# print(yelp)
yelp_api = YelpAPI(client_id, client_secret)
search_results = yelp_api.reviews_query(id = "frita-batidos-ann-arbor")
print(search_results)

gmaps = googlemaps.Client(key="AIzaSyCpatKpUmsGl2AW6NTQa1DsOah8vYwTUjY")
gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

gmap.scatter(lat,lon, 'r', 0.1, marker=False)
# gmap.plot(37.428, -122.145, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")

# frita = graph.get_object("FritaBatidos")
# print(frita)

