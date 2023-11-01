import urllib.request as urllib
import json
import time
# import glowbit


from flask import Flask, render_template
from math import cos, asin, sqrt, pi


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
# https://stackoverflow.com/a/21623206
def distance(lat1, lon1, lat2, lon2):
    r = 6371  # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * \
        cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))


@app.route("/")
def getCustomPosition():
    return render_template('index.html')


if __name__ == "__main__":
    for i in range(3):
        objPosition = getISSPosition()

        time.sleep(1)
        print("Latitude: " + str(objPosition['latitude']))
        print("Longitude: " + str(objPosition['longitude']))
        print("Distance: " + str(distance(0, 0,
              float(objPosition['latitude']), float(objPosition['longitude']))))
