#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, Response, request
import io

import RESTclient
from piScan import piScan

app = Flask(__name__)

@app.route('/')
def index():
    ipList = ['192.168.0.2','192.168.0.100']
    #ipList = piScan()
    return render_template('index.html', ipList = ipList)

@app.route('/cmd/', methods=['GET'])
def send_command():
    HOST = request.args['host']
    PORT = request.args['port']
    command = request.args['command']
    response = RESTclient.send_command(command, HOST, PORT=3000)
    print(response)
    return '', 204

# TODO: impliment video streams

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0')

