import os

import requests
import flask


app = flask.Flask(__name__, template_folder='./')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/request/', methods=['POST'])
def call_backend():
    # get environmentals
    _backend_addr = os.environ["BACKEND_PORT_5000_TCP_ADDR"]
    _backend_port = os.environ["BACKEND_PORT_5000_TCP_PORT"]
    _target = "http://{}:{}/request/".format(_backend_addr, _backend_port)
    # call backend
    _id = flask.request.form['id']
    _url = flask.request.form['url']
    _domain = flask.request.form['domain']
    _payload = {'id': _id, 'url': _url, 'domain': _domain}
    _req = requests.post(_target, data=_payload)
    # Return result
    print('This is the result:')
    _result = _req.json()
    return flask.jsonify(_result)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 8080.
    _port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=_port)
