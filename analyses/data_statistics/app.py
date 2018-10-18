import datetime
import json
import glob
import os
import time

import flask
from tqdm import tqdm


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def do_analysis():
    # create lockfile
    os.system('touch {}'.format(flask.request.form['lockfile']))

    # check what data files are available
    filepath = flask.request.form['datafiles']
    data_files = glob.glob(filepath)
    print("found those datafiles:")
    for file in data_files:
        print('- ' + file)

    print('perform analysis ...')
    # dummy analysis
    result = {
        "id": flask.request.form['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": flask.request.form['url'],
        "domain": flask.request.form['domain'],
        "analysis": flask.request.form['analysis'],
        "info": "Done",
        }
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- doing important analysis work, part {} ...'.format(i))

    # save results
    outfilepath = flask.request.form['outfile']
    print('Storing results in ' + outfilepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)

    # remove lockfile
    os.system('rm {}'.format(flask.request.form['lockfile']))
    # create donefile
    os.system('touch {}'.format(flask.request.form['donefile']))

    # return something
    return 'Finished analysis: ' + flask.request.form['id']


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5003.
    _port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=_port)
