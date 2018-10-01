import json
import os

import flask


app = flask.Flask(__name__, template_folder='./')

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/request/', methods=['POST'])
def request_result():
    datadir = 'data'
    url = flask.request.form['url']
    json_data = {}
    json_data['url'] = url
    json_data['dir_content'] = {}
    if os.path.isdir(datadir):
        for filepath in os.listdir(datadir):
            with open(os.path.join(datadir, filepath)) as f:
                json_data['dir_content'].update({filepath: json.load(f)})
    json_data['info'] = "Requesting data for {}".format(url)
    json_data['result'] = 'Empty'
    return flask.jsonify(json_data)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
