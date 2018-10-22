from __future__ import print_function

import os
import re
import time

import flask
import requests


app = flask.Flask(__name__)


def html_target():
    # get environmentals
    _master_addr = os.environ["SCAN_SPIDERFOOT_SERVER_PORT_5001_TCP_ADDR"]
    _master_port = os.environ["SCAN_SPIDERFOOT_SERVER_PORT_5001_TCP_PORT"]
    _target = "http://{}:{}".format(_master_addr, _master_port)
    return _target


def run_sf_cid(cmd, cid, log):
    # prepare cmd
    _cmd_file = 'sf_cmd.txt'
    with open(_cmd_file, 'w') as myfile:
        print(cmd, file=myfile)
    # prepare other input
    _log_file = '/data/scan_results/{}/log_spiderfoot.txt'.format(cid)
    _tmp_log_file = '/data/scan_results/{}/log_spiderfoot_tmp.txt'.format(cid)
    _shell_cmd = "python sfcli.py -s {} -e {} -o {}".format(html_target(), _cmd_file, _tmp_log_file)
    print("Executing: " + _shell_cmd + " with spiderfoot command " + cmd)
    # call sf
    os.system(_shell_cmd)
    if log:
        os.system('cat ' + _tmp_log_file + " >> " + _log_file)
    with open(_tmp_log_file, 'r') as myfile:
        output = myfile.read()
    os.system('rm ' + _tmp_log_file)
    return output


def get_scan_id(log):
    regex = re.compile("Scan ID: (.*)")
    finding = regex.search(log)
    scan_id = finding.group(1)
    # print('This is the scan id: "' + scan_id + '"')
    return scan_id


def scan_finished(log, scan_id):
    regex_string = r"{}  \|.*\|(.*)\| [0-9]*".format(scan_id)
    regex = re.compile(regex_string)
    finding = regex.search(log)
    status = finding.group(1).strip()
    if status == 'FINISHED':
        return True
    return False


@app.route('/', methods=['POST'])
def get_spiderfoot_result():
    cid = flask.request.form['id']
    url = flask.request.form['url']

    # register modules
    modules = ['sfp_pwned', 'sfp_phishtank', 'sfp_pastebin']

    print("Calling the spiderfoot server to analyse {} using those modules:".format(url))
    for module in modules:
        print("- " + module)

    # define run function wrapper
    def run_sf(cmd, log=True):
        return run_sf_cid(cmd, cid, log)

    # delete logfile if existent:
    _log_file = '/data/scan_results/{}/log_spiderfoot.txt'.format(cid)
    if os.path.isfile(_log_file):
        os.system("rm " + _log_file)

    # run it
    log = run_sf('start {} -m {}'.format(url, ','.join(modules)))
    scan_id = get_scan_id(log)

    # wait for all scans to finish
    is_done = False
    while not is_done:
        log = run_sf('scans -x', log=False)
        is_done = scan_finished(log, scan_id)
        if not is_done:
            time.sleep(2)

    # write scan status to log
    run_sf('scans -x')

    # download results
    response = requests.get(html_target() + "/scaneventresultexportmulti?ids={}".format(scan_id))
    _output_file = '/data/scan_results/{}/data_spiderfoot.txt'.format(cid)
    print('Saving scan results in ' + _output_file)
    with open(_output_file, 'w') as myfile:
        print(response.text, file=myfile)

    print("Done!")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5005.
    _port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=_port)
