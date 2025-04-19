

from serpapi import GoogleSearch
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=2)
# Format dates for API
from_date = start_date.strftime('%Y-%m-%d')
to_date = end_date.strftime('%Y-%m-%d')
SERP_API_KEY = os.getenv('SERP_API_KEY')
params = {
    "engine": "google_news",
    "q": "Trump",
    "api_key": SERP_API_KEY,
}

        
search = GoogleSearch(params)
results = search.get_dict()
print('results keys: ', results.keys())
for key, v in results.items():
    ##print
    print('key: ', key, '; v: ', v)