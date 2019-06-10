#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, Response, request
import io

import TCPclient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cmd/', methods=['GET'])
def send_command():
    HOST = request.args['host']
    PORT = request.args['port']
    command = request.args['command']
    response = TCPclient.send_command(command, HOST, PORT=3000)
    print(response)
    return '', 204


if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0')

