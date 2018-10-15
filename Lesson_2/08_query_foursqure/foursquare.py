import json, requests
import pprint

url = 'https://api.foursquare.com/v2/venues/search'

Client_ID = ""
Client_Secret = ""


def curl(ll, query):
    params = dict(
      client_id=Client_ID,
      client_secret=Client_Secret,
      v='20181014',
      ll=ll,
      query=query,
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    pprint.pprint(data)

print curl("40.768349, -73.96575", 'salad')


# https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20181014&ll=%s,%s&query=%s
