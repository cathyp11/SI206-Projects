import unittest
import json
import httplib2
import os
from apiclient.discovery import build
service = build('api_name', 'api_version', ...)

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import quickstart

# access_token = "EAACEdEose0cBAFhKsHXIFkb09KcMUNecCiHD2HeXctxHZCY4X7Qb3ZC6eOjvGX6zTrhhmKwA91m6q8yOSMbMVemgb91Ko67qJHjZB4KTWmeXP3fQvoLLNhyMHQZAzv93LIY0c4AgLABvbD5Bm4hbI9mQq1Ol85xY6rdSbu80l1XBZCkeMKAaGwEMISZBHZBgnIURBYtO362yQZDZD"

# r = requests.get("https://graph.facebook.com/v2.11/me/feed",params={"limit":2, "access_token":access_token})
# if r.status_code != 200:
#     access_token = raw_input("Get a Facebook access token v2.11 from https://developers.facebook.com/tools/explorer and enter it here if the one saved in the file doesn't work anymore.  :\n")

# url_params = {}
# url_params["access_token"] = access_token
# url_params["fields"] = "comments{comments{like_count,from,message,created_time},like_count,from,message,created_time},likes,message,created_time,from" # Parameter key-value so you can get post message, comments, likes, etc. as described in assignment instructions.
# url_params["limit"] = 10

# def requestURL_fb(baseurl, params = {}):
#     req = requests.Request(method = 'GET', url = baseurl, params = url_params)
#     prepped = req.prepare()
#     return prepped.url 

# CACHE_FNAME = 'cache.json'

# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()
# except:
#     CACHE_DICTION = {}

# def getWithCaching(ID):
#     baseurl_fb = "https://graph.facebook.com/v2.11/" + ID + "/feed"
#     full_url_fb = requestURL_fb(baseurl_fb, params = url_params)

#     if full_url_fb in CACHE_DICTION:
#         print 'using cache'
#         response_text = CACHE_DICTION[full_url_fb]
#     else:
#         print 'fetching'
#         fb_response = requests.get(full_url_fb)
#         CACHE_DICTION[full_url_fb] = fb_response.text
#         response_text = fb_response.text

#         cache_file = open(CACHE_FNAME, 'w')
#         cache_file.write(json.dumps(CACHE_DICTION))
#         cache_file.close()

#     return response_text
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    msgs = service.users().messages().list(userId='me', maxResults=500).execute()
    print(msgs)

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])


if __name__ == '__main__':
    main()
# service = discovery.build('gmail', 'v1', http=http)
# msgs = service.users().messages().list(userId='me', maxResults=500).execute()
# print(msgs)
