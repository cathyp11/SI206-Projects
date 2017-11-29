import unittest
import json
import requests
import urllib.request

yelp_access_token = "ztsjq_LquhhLU5ABi4zWOIOISD-jy8UiWijyAzLb0yV7MChsj3pLa6ZP6yruRkTdS6M2SRvm3olECWEx6GTsE1JLEDkkHWS5oyWYYYSFfbAodGQ0-NmJFQMshTATWnYx"
places_key = "AIzaSyCytCUed9RpF5GEmMl5t4Pakx_Asp3bTs0"
geo_key = "AIzaSyCRq7G6004a_ADdAf5MFE11NUU37GCIkuY"

CACHE_YELP = 'cache_yelp.json'
CACHE_PLACES = 'cache_places.json'

try:
    cache_file_places = open(CACHE_PLACES, 'r')
    cache_file_yelp = open(CACHE_YELP, 'r')
    cache_contents_places = cache_file_places.read()
    cache_contents_yelp = cache_file_yelp.read()
    CACHE_DICTION_places = json.loads(cache_contents_places)
    CACHE_DICTION_yelp = json.loads(cache_contents_yelp)
    cache_file_places.close()
    cache_file_yelp.close()
except:
    CACHE_DICTION_places = {}
    CACHE_DICTION_yelp = {}

location = input("Enter a city: ")

def Caching_Yelp():
	url = "https://api.yelp.com/v3/businesses/search?term=restaurants&offset=100&sort_by=rating&location=" + location 
	if location in CACHE_DICTION_yelp:
		print('using cache')
		data_y = CACHE_DICTION_yelp[location]
	else:
		print('fetching')
		yelp_api = requests.get(url, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
		data_y = yelp_api.text
		CACHE_DICTION_yelp[location] = data_y
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION_yelp)
		fw = open(CACHE_YELP,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data_y

def Geocode():
	loc = location.replace(" ", "+")
	geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '&key=' + geo_key
	req = urllib.request.urlopen(geo_url)
	read = req.read()
	jsonread = json.loads(read)
	lat = str(jsonread['results'][0]['geometry']['location']['lat'])
	lng = str(jsonread['results'][0]['geometry']['location']['lng'])
	return lat,lng

def Caching_Places():
	geo = Geocode()
	places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + geo[0] + "," + geo[1] + '&radius=500&type=restaurant&key=' + places_key
	if location in CACHE_DICTION_places:
		print('using cache')
		data_p = CACHE_DICTION_places[location]
	else:
		print('fetching')
		places_api = urllib.request.urlopen(places_url)
		jsonread = response.read()
		data_p = json.loads(jsonread)
		CACHE_DICTION_places[location] = data_p
		dumped_json_cache = json.dumps(CACHE_DICTION_places)
		fw = open(CACHE_PLACES, "w")
		fw.write(dumped_json_cache)
		fw.close()
	return data_p

read = Caching_Yelp()
print(read)
places = Caching_Places()
print(places)

for place in places['results']:




if __name__ == '__main__':
    unittest.main(verbosity=2)

