import datetime
import glob
import json
import os

import flask

import analysis


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def do_analysis():
    # create lockfile
    os.system('touch {}'.format(flask.request.form['lockfile']))

    # check what data files are available
    data_dir = flask.request.form['datadir']
    data_files = glob.glob(data_dir + "*")
    print("found those datafiles:")
    for file in data_files:
        print('- ' + file)

    print('perform analysis {} ...'.format(flask.request.form['analysis']))

    result = {
        "id": flask.request.form['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": flask.request.form['url'],
        "domain": flask.request.form['domain'],
        "analysis": flask.request.form['analysis'],
        "info": "Done",
        }

    result['result'] = analysis.run(data_dir)

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
