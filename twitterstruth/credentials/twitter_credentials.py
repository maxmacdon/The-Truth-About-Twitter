import json
from twython import Twython


credentials = dict()
credentials['CONSUMER_KEY'] = 'iv1i1qYNCuNhNLgm2EX6Zrkj8'
credentials['CONSUMER_SECRET'] = 'X9MWGxSVgJu6ExO5dgEMikJoHDrPmrC6uDNmOVorZmVJFHsRU7'

# Connect to Twitter API and get application-only access token
twitter = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'], oauth_version=2)

credentials['ACCESS_TOKEN'] = twitter.obtain_access_token()

# Save the credentials to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)
