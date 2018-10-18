import os

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def request_result():
    # define output files
    _result_file = "/data/raw/{}/data_theharvester.html".format(flask.request.form['id'])

    # define command
    _data_source = "bing"
    _cmd = "theharvester -d {} -b {} -f {}".format(flask.request.form['domain'], _data_source, _result_file)

    # create lockfile
    os.system('touch {}'.format(flask.request.form['lockfile']))
    # run it
    print("Executing: " + _cmd)
    os.system(_cmd)
    # remove lockfile
    os.system('rm {}'.format(flask.request.form['lockfile']))

    # return something
    return 'Finished: ' + _cmd


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5002.
    _port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=_port)
