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
    json_data = {'info': 'empty'}
    json_data['dir_content'] = {}
    if os.path.isdir(datadir):
        json_data['info'] = "Folder exists!"
        for filepath in os.listdir(datadir):
            with open(os.path.join(datadir, filepath)) as f:
                json_data['dir_content'].update({filepath: json.load(f)})
    else:
        json_data['info'] = "Error: Folder doesn't exist!"
    json_data['message'] = 'Hello {}!'.format('user')
    return flask.jsonify(json_data)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
