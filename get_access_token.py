#!/usr/bin/python
# coding: utf-8

"""
Credit: http://stackoverflow.com/questions/3058723/programmatically-getting-an-access-token-for-using-the-facebook-graph-api
"""

import facebook
import urllib
import urlparse
import subprocess
import warnings
import sys

def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')

if __name__ == "__main__":
    print("Fetching access token...")

    # Parameters of your app and the id of the profile you want to mess with.
    FACEBOOK_APP_ID = file2string(sys.argv[1])
    FACEBOOK_APP_SECRET = file2string(sys.argv[2])
    FACEBOOK_PROFILE_ID = file2string(sys.argv[3])

    # Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
    warnings.filterwarnings('ignore', category=DeprecationWarning)

    # Trying to get an access token. Very awkward.
    oauth_args = dict(client_id=FACEBOOK_APP_ID,
                      client_secret=FACEBOOK_APP_SECRET,
                      grant_type='client_credentials')
    oauth_curl_cmd = ['curl',
                      'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
    oauth_response = subprocess.Popen(oauth_curl_cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()[0]

    try:
        oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]

        with open('access_token.txt', 'w') as outfile:
            outfile.write(oauth_access_token)
            outfile.close()
            print("Finished fetching access token.")

    except KeyError:
        print('Unable to fetch an access token!')
