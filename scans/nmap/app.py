"""A webapp."""
import os

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def request_result():
    """Call nmap."""
    # define output files
    _result_file = "/data/scan_results/{}/data_nmap.xml".format(flask.request.form['id'])

    # define command
    _cmd = "nmap {} -oX {}".format(flask.request.form['domain'], _result_file)

    # run it
    print("Executing: " + _cmd)
    os.system(_cmd)

    # return something
    return 'Finished: ' + _cmd


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=_port)
