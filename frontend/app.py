import json
import os

import flask


app = flask.Flask(__name__, template_folder='./')

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/request/', methods=['POST'])
def hello():
    datadir = 'data'
    json_data = {}
    json_data['url'] = flask.request.form['url']
    json_data['dir_content'] = {}
    if os.path.isdir(datadir):
        for filepath in os.listdir(datadir):
            with open(os.path.join(datadir, filepath)) as f:
                json_data['dir_content'].update({filepath: json.load(f)})
    json_data['info'] = "Requesting data for {}".format(json_data['url'])
    return flask.jsonify(json_data)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 8888.
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
