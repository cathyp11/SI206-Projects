import unittest
import json


access_token = "EAACEdEose0cBAFhKsHXIFkb09KcMUNecCiHD2HeXctxHZCY4X7Qb3ZC6eOjvGX6zTrhhmKwA91m6q8yOSMbMVemgb91Ko67qJHjZB4KTWmeXP3fQvoLLNhyMHQZAzv93LIY0c4AgLABvbD5Bm4hbI9mQq1Ol85xY6rdSbu80l1XBZCkeMKAaGwEMISZBHZBgnIURBYtO362yQZDZD"

r = requests.get("https://graph.facebook.com/v2.11/me/feed",params={"limit":2, "access_token":access_token})
if r.status_code != 200:
    access_token = raw_input("Get a Facebook access token v2.11 from https://developers.facebook.com/tools/explorer and enter it here if the one saved in the file doesn't work anymore.  :\n")

url_params = {}
url_params["access_token"] = access_token
url_params["fields"] = "comments{comments{like_count,from,message,created_time},like_count,from,message,created_time},likes,message,created_time,from" # Parameter key-value so you can get post message, comments, likes, etc. as described in assignment instructions.
url_params["limit"] = 10

def requestURL_fb(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = url_params)
    prepped = req.prepare()
    return prepped.url 

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def getWithCaching(ID):
    baseurl_fb = "https://graph.facebook.com/v2.11/" + ID + "/feed"
    full_url_fb = requestURL_fb(baseurl_fb, params = url_params)

    if full_url_fb in CACHE_DICTION:
        print 'using cache'
        response_text = CACHE_DICTION[full_url_fb]
    else:
        print 'fetching'
        fb_response = requests.get(full_url_fb)
        CACHE_DICTION[full_url_fb] = fb_response.text
        response_text = fb_response.text

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return response_text
