import os

import flask

import master


app = flask.Flask(__name__, template_folder='./')

@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/request/', methods=['POST'])
def request_result():
    url = flask.request.form['url']
    result = master.backend_get(url)
    return flask.jsonify(result)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
