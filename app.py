#! /usr/bin/python

import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_googlemaps import GoogleMaps, Map
import requests
from ipwhois import IPWhois
import config

app = Flask(__name__)

# initialize the extension
GoogleMaps(app, key=config.GOOGLEMAPS_API_KEY)

# headers
hdr = {
    'user-agent': 'Geo-IP-Lookup v.01',
    'content-type': 'application/json'
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

    # set the API url
    url = config.BASE_URL + str(ip) + '?access_key=' + config.IP_STACK_KEY

    try:
        # call the API with requests
        r = requests.get(url, headers=hdr)

        # check the response
        if r.status_code == 200:
            results = r.json()

            # delete the key location, not needed for the output
            if 'location' in results:
                del results['location']

            # set the IP address for the template
            ip_address = ip

            # dump mymap vars
            mymap = Map(
                identifier="view-side",
                lat=results['latitude'],
                lng=results['longitude'],
                markers=[(results['latitude'], results['longitude'])],
                style=(
                    'height:525px;'
                    'width=500px;'
                ),
            )

    # catch the exception
    except requests.exceptions.ConnectionError as err:
        flash('An API connection error occurred: {}'.format(str(err)))
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        location=results,
        ip_address=ip_address,
        mymap=mymap
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html'
    ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template(
        '500.html'
    ), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=config.DEBUG,
    )

