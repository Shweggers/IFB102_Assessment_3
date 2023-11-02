import urllib.request as urllib
import json
import time
# import glowbit


from flask import Flask, render_template
from math import radians, cos, sin, asin, sqrt


app = Flask(__name__)
# stick = glowbit.stick(pin=12)


def getISSPosition():
    # retrieved from:
    # http://open-notify.org/Open-Notify-API/ISS-Location-Now/
    req = urllib.Request("http://api.open-notify.org/iss-now.json")
    response = urllib.urlopen(req)

    obj = json.loads(response.read())
    objPosition = obj['iss_position']  # ['latitude'] ['longitude']

    return objPosition


# retrieved from:
# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def getRatio(distance):
    # retrieved from:
    # https://www.quora.com/What-is-the-longest-distance-between-any-two-places-on-earth
    m = 20004  # km
    return max(distance / m, 1)



@app.route("/")
def getCustomPosition():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
    print("app runninng on 127.0. 0.1:5000")
