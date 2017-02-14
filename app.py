#! /usr/bin/python

import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_googlemaps import GoogleMaps, Map
import requests
from ipwhois import IPWhois
import config

app = Flask(__name__)

#initialize the extension
GoogleMaps(app, key=config.GOOGLEMAPS_API_KEY)

# headers
hdr = {
    'user-agent': 'Mozilla 5.0/Linux'
}


def get_client_ip():
    client_ip = request.remote_addr
    if request.remote_addr == '127.0.0.1' or request.remote_addr == '':
        client_ip = '71.43.49.234'
    else:
        client_ip = client_ip
    return client_ip


@app.route('/', methods=['GET', 'POST'])
def index():
    location = None

    if request.method == 'POST':
        ip = request.form['ip_add'].strip()
        format = 'json'
    else:
        ip = get_client_ip()
        format = 'json'

    url = config.BASE_URL + format + '/' + ip

    try:
        r = requests.get(url, headers=hdr)
        if r.status_code == 200:
            location = r.json()
            ip_address = ip
            mymap = Map(
                identifier="view-side",
                lat=location['latitude'],
                lng=location['longitude'],
                markers=[(location['latitude'], location['longitude'])],
                style=(
                    'height:525px;'
                    'width=500px;'
                ),
            )

            # whois lookup
            # obj = IPWhois(ip)
            # results = obj.lookup_rdap(depth=1)
            # entity = results['entities'][0]

    except requests.exceptions.ConnectionError as e:
        return str(e)

    return render_template(
        'index.html',
        location=location,
        ip_address=ip_address,
        #results=results,
        #entity=entity,
        mymap=mymap
    )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=config.DEBUG,
    )

