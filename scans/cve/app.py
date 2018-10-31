"""A webapp."""
import os

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def request_result():
    """Call nmap."""

    # TODO: analyze all tools the customer uses + the ones we detect ourselves
    _tools = ['microsoft/office']

    # define output files
    _result_file = "/data/scan_results/{}/data_cve.xml".format(flask.request.form['id'])

    # define commands
    _cmds = []
    _cmds.append('touch ' + _result_file)
    for tool in _tools:
        _cmds.append("curl https://cve.circl.lu/api/search/{} >> {}".format(tool, _result_file))

    # run it
    for cmd in _cmds:
        print("Executing: " + cmd)
        os.system(cmd)

    # return something
    return 'Finished!'


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=_port)
