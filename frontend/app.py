import json
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
    backend_addr = os.environ["BACKEND_PORT_5000_TCP_ADDR"]
    backend_port = os.environ["BACKEND_PORT_5000_TCP_PORT"]
    target = "http://{}:{}/request/".format(backend_addr, backend_port)
    # call backend
    url = flask.request.form['url']
    payload = {'url': url}
    r = requests.post(target, data=payload)
    # Return result
    print('This is the result:')
    result = r.json()
    return flask.jsonify(result)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 8080.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
