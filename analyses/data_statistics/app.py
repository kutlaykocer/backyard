import datetime
import json
import os
import time

import flask
from tqdm import tqdm


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def do_analysis():

    filepath = 'data/{}/data_*'.format(flask.request.form['id'])

    print('perform analysis ...')
    outfilepath = 'data/{}/result.json'.format(flask.request.form['id'])
    # dummy analysis
    result = {
        "id": flask.request.form['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": flask.request.form['url'],
        "domain": flask.request.form['domain'],
        "info": "Everything is analyzed!",
        }
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- doing important analysis work, part {} ...'.format(i))

    print('Storing results in ' + filepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)

    # return something
    return 'Finished analysis: ' + flask.request.form['id']


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5003.
    _port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=_port)
