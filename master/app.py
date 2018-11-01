"""A webapp."""
import os

import flask

import master


app = flask.Flask(__name__, template_folder='./')


@app.route('/')
def index():
    """Render the index html."""
    return flask.render_template('index.html')


@app.route('/request/', methods=['POST'])
def request_result():
    """Request results."""
    _result = master.master_get(flask.request.form.to_dict())
    return flask.jsonify(_result)


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=_port)
