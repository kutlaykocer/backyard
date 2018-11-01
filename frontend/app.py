"""A webapp."""
import os
import pprint

import requests
import flask


N_EMAILS = 6
N_PRODUCTS = 3

app = flask.Flask(__name__, template_folder='./')


@app.route('/')
def index():
    """Render the index html."""
    return flask.render_template('index.html')


@app.route('/request/', methods=['POST'])
def call_master():
    """Request results."""
    # get environmentals
    _master_addr = os.environ["MASTER_PORT_5000_TCP_ADDR"]
    _master_port = os.environ["MASTER_PORT_5000_TCP_PORT"]
    _target = "http://{}:{}/request/".format(_master_addr, _master_port)
    # prepare payload
    _emails = {'email' + str(i): flask.request.form['vip'+str(i)] for i in range(N_EMAILS)}
    _products = {'product' + str(i):
                 flask.request.form['vendor'+str(i)] + "/" +
                 flask.request.form['product'+str(i)] for i in range(N_PRODUCTS)}
    # call master
    _payload = {'id': flask.request.form['id'],
                'url': flask.request.form['url'],
                'domain': flask.request.form['url'].split('www.')[-1].split('http://')[-1],
                **_products,
                **_emails,
                }
    print('Sending HTML request to ' + _target)
    print('With data:')
    pprint.pprint(_payload)
    _req = requests.post(_target, data=_payload)
    # Return result
    print('This is the result:')
    _result = _req.json()
    return flask.jsonify(_result)


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=_port)
