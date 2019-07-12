'''Accept HTTP requests and push to controller'''

import flask
import controller

__PORT = 3000

app = flask.Flask(__name__, template_folder=None)


@app.route('/status')
def status():
    '''Return information about DEEPi and camera'''
    status = {'ip': 'localhost',
              'port': __PORT
    }
    return flask.jsonify(status)

@app.route('/cmd', methods=['POST'])
def cmd():
    r = flask.request.json

    try:
        res = eval("controller.{}".format(r['cmd']))
    except:
        raise

    # TODO: impliment flask.logger
    return flask.jsonify(res)

def gen(camera):
    '''Video streaming generator function.'''
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    '''Video streaming route. Put this in the src attribute of an img tag.'''
    return Response(gen(controller.deepi()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=__PORT, threaded=True)

