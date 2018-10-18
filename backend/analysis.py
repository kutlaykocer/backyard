import datetime
import glob
import json
import os
import pathlib
import re
import time

import requests


def collect_results(analyses, form_data):

    result = {
        "id": form_data['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain'],
        "info": "Done",
        }

    for analysis in analyses:
        filepath = '/data/results/{}/result_{}.json'.format(form_data['id'], analysis)
        with open(filepath) as result_file:
            json_data = json.load(result_file)
            result[analysis] = json_data

    outfilepath = '/data/results/{}/result.json'.format(form_data['id'])
    print('Storing results in ' + outfilepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)


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

    print("[ANALYSIS] running these analyses:")
    for analysis in _analyses:
        print('[ANALYSIS] - ' + analysis)
    is_done = {a: False for a in _analyses}

    for analysis in _analyses:
        # check if process already runs
        _lock_file = '/data/results/{}/lock_{}.txt'.format(form_data['id'], analysis)
        _done_file = '/data/results/{}/done_{}.txt'.format(form_data['id'], analysis)
        if os.path.isfile(_lock_file):
            print('[ANALYSIS] process ' + analysis + ': running, wait for it to finish!')
            continue
        elif is_done[analysis] or os.path.isfile(_done_file):
            print('[ANALYSIS] process ' + analysis + ': done!')
            if not is_done[analysis]:
                os.system('rm {}'.format(_done_file))
                is_done[analysis] = True
        else:
            print('[ANALYSIS] process ' + analysis + ': start')

        # get environmentals
        key_list = list(dict(os.environ).keys())
        regex_string = analysis.upper() + r'_PORT_\d{4}_TCP_PORT'
        port_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
        port = os.environ[port_key]
        _analysis_addr = os.environ["{}_PORT_{}_TCP_ADDR".format(analysis.upper(), port)]
        _analysis_port = os.environ["{}_PORT_{}_TCP_PORT".format(analysis.upper(), port)]
        _target = "http://{}:{}/".format(_analysis_addr, _analysis_port)

        # send request
        _payload = form_data
        _payload['lockfile'] = _lock_file
        _payload['donefile'] = _done_file
        _payload['outfile'] = '/data/results/{}/result_{}.json'.format(form_data['id'], analysis)
        _payload['datadir'] = '/data/raw/{}/'.format(form_data['id'])
        _payload['analysis'] = analysis.lower()
        _req = requests.post(_target, data=_payload)

    # if all analyses ready, produce final result file
    if all(is_done[x] for x in is_done):
        print("[ANALYSIS] everything done, create summary file ...")
        collect_results(_analyses, form_data)
        return 'Analyses done!'

    print("[ANALYSIS] wait before returning")
    time.sleep(5)

    return 'Check if done'
