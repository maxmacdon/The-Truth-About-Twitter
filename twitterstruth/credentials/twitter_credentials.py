import json

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'iv1i1qYNCuNhNLgm2EX6Zrkj8'
credentials['CONSUMER_SECRET'] = 'X9MWGxSVgJu6ExO5dgEMikJoHDrPmrC6uDNmOVorZmVJFHsRU7'
credentials['ACCESS_TOKEN'] = '3330453371-53qtrIFDcygzzO0f3wg4yVSjo7ACtzESMhSHOPv'
credentials['ACCESS_SECRET'] = 'THGzrqUaPgr1pNPubudNBGj92s1ibYfO1hM2CwmNJgZ6U'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)