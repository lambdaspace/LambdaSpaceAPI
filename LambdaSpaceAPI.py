#!/usr/bin/env python2
# -*- coding: <UTF-8> -*-
"""LambdaSpace's API"""
#from sys import exit
from urllib2 import urlopen, URLError
import json
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, abort, make_response

__author__ = "Kopsacheilis Charalampos, Mpazakas Filippos"
__credits__ = ["Kopsacheilis Charalampos", "Mpazakas Filippos", "Kolokotronis Panagiotis"]
__version__ = "1.0"

LSAPI = Flask(__name__)
CORS(LSAPI)


def check_status(jsobj):
    """Changes status depending on the number of devices connected to router."""
    url = 'https://www.lambdaspace.gr/hackers.txt'
    try:
        retv = urlopen(url)
    except URLError:
        raise URLError
    jsobj["state"]["open"] = (int(retv.read() > 0))
    return jsobj


@LSAPI.errorhandler(404)
def not_found(error):
    """Return JSONified 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@LSAPI.errorhandler(400)
def bad_request(error):
    """Return JSONified 400"""
    return make_response(jsonify({'error': 'Bad request'}), 400)


@LSAPI.errorhandler(500)
def int_serv_error(error):
    """Return JSONified 500"""
    return make_response(jsonify({'error': 'Internla Server Error'}), 500)


@LSAPI.route('/api/v1.0/SpaceAPI')
def change_state():
    """Load json string from 'LambdaSpaceAPI.json' and convert to dictionary"""
    with open('LambdaSpaceAPI.json') as jsfile:
        jstring = jsfile.read()
    json_data = json.loads(jstring)
    try:
        json_data = check_status(json_data)
    except URLError:
        abort(500)
    return jsonify(json_data)


if __name__ == '__main__':
    LSAPI.run(debug=False, threaded=True)
