#! /usr/bin/python

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_googlemaps import GoogleMaps, Map
import requests
import config

app = Flask(__name__)

#initialize the extension
GoogleMaps(app, key=config.GOOGLEMAPS_API_KEY)

# headers
hdr = {
    'user-agent': 'Mozilla 5.0/Linux'
}

# base url
base_url = 'http://freegeoip.net/'


def get_client_ip():
    client_ip = request.remote_addr
    return client_ip


@app.route('/', methods=['GET', 'POST'])
def index():
    location = None

    if request.method == 'POST':
        ip = request.form['ip_add']
        format = request.form['format']
    else:
        ip = get_client_ip()
        format = 'json'

    url = base_url + format + '/' + ip

    try:
        r = requests.get(url, headers=hdr)
        if r.status_code == 200:
            location = r.json()
    except requests.exceptions.ConnectionError as e:
        return str(e)

    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )

    return render_template(
            'index.html',
            location=location,
            mymap=mymap
    )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5055,
        debug=True,
    )

