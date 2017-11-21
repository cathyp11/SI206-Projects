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

access_token = "EAACEdEose0cBAMBUqFT5vJXA6IuhbqjLTZC2WCU4hsDZAqZCrWCFFmb5E1S7hjtP2n9ZBZBzuswEfSs8Y2ZC9HTvNAHH82iOaYpmcJ8LglEHjSbMTFn0GD0GTpIr0rHnqZBKJdZCJZAuL9SaTgQJompOClJRGGhCUDvZAZCLIW6NFEmwlvVKjZC683HtARkdSnvuiM3qLsKP9Jix5QZDZD"

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

places_key = "AIzaSyCytCUed9RpF5GEmMl5t4Pakx_Asp3bTs0"

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


# posts = Caching_FB("FritaBatidos")
# print(posts)
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

baseurl_id = 'https://api.instagram.com/v1/tags/fritabatidos/media/recent?access_token=' + inst_access_token +'&min_tag_id=1387332980547'
responses = urllib.request.urlopen(baseurl_id)
jsonreads = responses.read()
reads = json.loads(jsonreads)
print(reads)

url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=51.503186,-0.126446&radius=5000&type=museum&key=' + places_key
response = urllib.request.urlopen(url)
jsonread = response.read()
read = json.loads(jsonread)
# print(read)

if __name__ == "__main__":
    unittest.main(verbosity=2)
