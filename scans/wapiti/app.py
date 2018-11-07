"""A webapp."""
import os

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def request_result():
    """Call wapiti."""
    # define output files
    _result_file = "/data/scan_results/{}/data_wapiti.xml".format(flask.request.form['id'])

    # define command
    _ssl_addon = '--verify-ssl 1' if flask.request.form['url'].startswith('https') else ''
    _cmd = "wapiti -u {}/  -m \"sql,exec,permanentxss,xss,shellshock,blindsql\" -d 10 --max-links-per-page 15"\
           " --max-files-per-dir 30 -f xml --max-scan-time 15 {} -o {}".\
        format(flask.request.form['url'], _ssl_addon, _result_file)

    # run it
    print("Executing: " + _cmd)
    os.system(_cmd)

    # return something
    return 'Finished: ' + _cmd


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 5008))
    app.run(host='0.0.0.0', port=_port)
