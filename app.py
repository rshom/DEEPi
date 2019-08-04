import time
import datetime

from flask import Flask, render_template, Response
from deepi import DEEPi

camera = DEEPi()

app = Flask(__name__)


def genName():
    '''Create a new filename to save files with clear time stamps'''
    while True:
        timeStamp = datetime.datetime.utcnow().isoformat()
        yield timeStamp[:-7].replace('-','').replace(':','')


def genFrame(camera=camera):
    '''Access last frame saved by camera. Frame should be updated continuously while camera is streaming'''
    camera.start_stream()
    while True:
        camera.last_access = time.time()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + camera.last_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(genFrame(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

#TODO: implement commands to send to camera

if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
