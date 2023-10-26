import urllib.request as urllib
import json


req = urllib.Request("http://api.open-notify.org/iss-now.json")
response = urllib.urlopen(req)


obj = json.loads(response.read())
objPosition = obj['iss_position'] # ['latitude'] ['longitude']


