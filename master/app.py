import os

import flask

import master


app = flask.Flask(__name__, template_folder='./')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/request/', methods=['POST'])
def request_result():
    _form_data = {
        'id': flask.request.form['id'],
        'url': flask.request.form['url'],
        'domain': flask.request.form['domain']
        }
    _result = master.master_get(_form_data)
    return flask.jsonify(_result)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    _port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=_port)
