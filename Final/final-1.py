import unittest
import json
import requests_oauthlib
import requests
import facebook

access_token = "EAACEdEose0cBABACcfO3ZAxUpgTa4g0kSTNOGzlAVrxswR3YN0zDxEvpi8XwGEYMaRqqen2g0PyDZAmV2nHz0O1KkqvXT48f3Ua0Mxg6qTUCro5fdmXkDWWkxDquxZAItXQDNdZCYadxRcwTKuKAVU0CP2Vk1Ym3RJkjnoMDOZCUk0za0ebLyLdMOzt3r5iySewZCp2e3sPQZDZD"

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def Caching_FB():
	user = "FritaBatidos"
	if user in CACHE_DICTION:
		print('using cache')
		data = CACHE_DICTION[user]
	else:
		print('fetching')
		graph = facebook.GraphAPI(access_token)
		data = graph.get_object(id="FritaBatidos", fields='posts')
		CACHE_DICTION[user] = data
		# dump the existing cached data
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	return data

posts = Caching_FB()
print(posts)
# frita = graph.get_object("FritaBatidos")
# print(frita)

