#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, Response
from picamera import PiCamera
import io

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

def gen():
    with PiCamera() as camera:
        frame = io.BytesIO()
        camera.capture( frame, 'jpeg' )
        frame.seek(0)
        print(frame.read(1080))
        return (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame.read(1080)+b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response( gen(),
                     mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0')

    
