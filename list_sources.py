import requests
import os
import json

## Listing sources available in News API
API_KEY = os.getenv('NEWS_API_KEY')

response = requests.get('https://newsapi.org/v2/sources', params={'apiKey': API_KEY})

if response.status_code == 200:
    with open('sources.json','w') as f:
        json.dump(response.json(), f, indent=4)
else:
    print('error, code: ', response.status_code)

