#!/usr/bin/env python2
# -*- coding: <UTF-8> -*-
"""LambdaSpace's API"""
from sys import exit
from flask import Flask, jsonify, abort
from flask_cors import CORS, cross_origin
from urllib2 import urlopen, URLError
import json

__author__ = "Kopsacheilis Charalampos, Mpazakas Filippos"
__credits__= ["Kopsacheilis Charalampos", "Mpazakas Filippos"]
__version__ = "1.0"

LSAPI = Flask(__name__)
CORS(LSAPI)

"""Changes status depending on the number of devices connected to router """
def check_status(jsobj):
    url = 'https://www.lambdaspace.gr/hackers.txt'
    try:
        retv = urllib2.urlopen(url)
    except:
        """Bad code"""
        print 'Could not open {0}'.format(url)
    
    if int(retv.read()) > 0:
        jsobj["state"]["open"] = True
    else:
        jsobj["state"]["open"] = False

    return jsobj    

@LSAPI.errorhandler(404)
def not_found(error):
    """Return JSONified 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@LSAPI.errorhandler(400)
def not_found(error):
    """Return JSONified 400"""
    return make_response(jsonify({'error': 'Bad request'}), 400)


    
@LSAPI.route('/api/v1.0/SpaceAPI')
def change_state():
    with open('LambdaSpaceAPI.json') as jsfile:
        """Load json string from 'LambdaSpaceAPI.json' and convert to dictionary"""
        jstring = jsfile.read()
        jsonData = json.loads(jstring)

        jsonData = check_status(jsonData)       
 
    return jsonify(jsonData)




 
