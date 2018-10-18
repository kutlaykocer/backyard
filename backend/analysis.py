import glob
import os
import pathlib
import re
import time

import requests


def perform_analysis(form_data):
    # make results directory
    _result_dir = '/data/results/{}'.format(form_data['id'])
    pathlib.Path(_result_dir).mkdir(parents=True, exist_ok=True)

    # check what data files are available
    filepath = '/data/raw/{}/data_*'.format(form_data['id'])
    data_files = glob.glob(filepath)

    # if no data, call worker
    if not data_files:
        print('[ANALYSIS] no data files available')
        return None

    print("[ANALYSIS] found those datafiles:")
    for file in data_files:
        print('[ANALYSIS] - ' + file)

    # call analyses
    _analyses = ['data_statistics']

    for analysis in _analyses:
        # check if process already runs
        _lock_file = '/data/results/{}/lock_{}.txt'.format(form_data['id'], analysis)
        if os.path.isfile(_lock_file):
            print('[ANALYSIS] process ' + analysis + ': running, wait for it to finish!')
            continue
        else:
            print('[ANALYSIS] process ' + analysis + ': start')
        # get environmentals
        key_list = list(dict(os.environ).keys())
        regex_string = analysis.upper() + r'_PORT_\d{4}_TCP_PORT'
        print('THIS IS THE STRING: ' + regex_string)
        port_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
        port = os.environ[port_key]
        _analysis_addr = os.environ["{}_PORT_{}_TCP_ADDR".format(analysis.upper(), port)]
        _analysis_port = os.environ["{}_PORT_{}_TCP_PORT".format(analysis.upper(), port)]
        _target = "http://{}:{}/".format(_analysis_addr, _analysis_port)
        # send request
        _payload = form_data
        _payload['lock_file'] = _lock_file
        _req = requests.post(_target, data=_payload)

    print("[ANALYSIS] wait before returning")
    time.sleep(5)

    return 'Check if done'
