'''Accept HTTP requests and push to controller'''

import flask
import controller

__PORT = 5000

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
    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=__PORT)

