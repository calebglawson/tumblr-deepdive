#!/usr/bin/python2
from builtins import input
from future import standard_library
from os import path
from requests_oauthlib import OAuth1Session
from __future__ import print_function
import json
import pytumblr
standard_library.install_aliases()


def retrieve_consumer_keys():
    print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
    consumer_key = input('Paste the consumer key here: ')
    consumer_secret = input('Paste the consumer secret here: ')
    return consumer_key, consumer_secret


if path.isfile("config.json"):
    print('Would you like to use your existing consumer key and secret?')
    use_existing = input('Y or N: ')

    if use_existing.upper() == "Y":
        filename = "config.json"
        f = open(filename, "r")
        read = f.read()
        load = json.loads(read)
        consumer_key = load["consumer_key"]
        consumer_secret = load["consumer_secret"]
    else:
        consumer_key, consumer_secret = retrieve_consumer_keys()
else:
    consumer_key, consumer_secret = retrieve_consumer_keys()

request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorize_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

# STEP 1: Obtain request token
oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth_session.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# STEP 2: Authorize URL + Rresponse
full_authorize_url = oauth_session.authorization_url(authorize_url)

# Redirect to authentication page
print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
redirect_response = input('Allow then paste the full redirect URL here:\n')

# Retrieve oauth verifier
oauth_response = oauth_session.parse_authorization_response(redirect_response)

verifier = oauth_response.get('oauth_verifier')

# STEP 3: Request final access token
oauth_session = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier
)
oauth_tokens = oauth_session.fetch_access_token(access_token_url)

tokens = json.dumps({
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'oauth_token': oauth_tokens.get('oauth_token'),
    'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
})

try:
    f = open("config.json", "w")
    f.write(tokens)
    f.close()
    print ("Authentication successful. File config.json created in the working directory.")
except:
    print ("File config.json failed to write.")
