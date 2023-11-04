import urllib.request as urllib
import json
import math
import glowbit


from flask import Flask, request, render_template
from math import radians, cos, sin, asin, sqrt


app = Flask(__name__)
stick = glowbit.stick(pin=12)


stick.clear()


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

    return 1 - min(distance / m, 1)


def processData(lon1, lat1, lon2, lat2):
    distance = haversine(lon1, lat1, lon2, lat2)
    ratio = getRatio(distance)

    lights = math.floor(ratio * 8)
    remainder = ratio

    _data = {
        "distance": distance,
        "lights": lights,
        "remainder": remainder
    }

    return _data


@app.route("/")
def routeWithDefault():
    issPosition = getISSPosition()
    issLat = float(issPosition['latitude'])
    issLon = float(issPosition['longitude'])

    defLat = 37.4221
    defLon = -122.0841

    _data = processData(issLon, issLat, defLon, defLat)

    return render_template("index.html", data=_data)


@app.route("/search/")
def routeWithCustom():
    issPosition = getISSPosition()
    issLat = float(issPosition['latitude'])
    issLon = float(issPosition['longitude'])

    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    _data = processData(issLon, issLat, lon, lat)

    return render_template("index.html", data=_data)


@app.route("/glowbit" , methods=["POST"])
def routeToGlowbit():
    lights = int(request.form.get("lights"))
    remainder = float(request.form.get("remainder"))

    while lights >= 8:
        lights -= 1

    colour = glowbit.colourFunctions.rgbColour(
        255 - min(int(remainder * 255), 255),
        min(int(remainder * 255), 255), 0)

    for i in range(lights):
        stick.set_pixel(i, glowbit.colourFunctions.green())
    stick.set_pixel(lights, colour)

    stick.pixelsShow()

app.run()