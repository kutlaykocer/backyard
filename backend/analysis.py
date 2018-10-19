import datetime
import json
import os
import pathlib
import time

import requests

import env
import job_mng


def collect_results(analyses, form_data):
    _cid = form_data['id']
    result = {
        "id": _cid,
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain'],
        "info": "Done",
        }

    for ana in analyses:
        _file_path = env.analysis(_cid, ana)['outfile']
        with open(_file_path) as result_file:
            result[ana] = json.load(result_file)
        os.system('rm ' + env.analysis(_cid, ana)['donefile'])

    _outfile_path = env.analysis(_cid)['resultfile']
    print('[ANALYSIS] storing results in ' + _outfile_path)
    with open(_outfile_path, 'w') as outfile:
        json.dump(result, outfile)


def perform_analysis(form_data):
    _analyses = ['data_statistics', 'dummy_analysis']

    _cid = form_data['id']

    # make results directory
    pathlib.Path(env.analysis(_cid)['resultdir']).mkdir(parents=True, exist_ok=True)

    # check what data files are available
    if not os.path.isfile(env.worker(_cid)['alldonefile']):
        print('[ANALYSIS] no data files available')
        return None

    # print analyses
    print("[ANALYSIS] running these analyses:")
    for ana in _analyses:
        print('[ANALYSIS] - ' + ana)
    is_done = {a: False for a in _analyses}

    # call analyses
    for ana in _analyses:
        _lock_file = env.analysis(_cid, ana)['lockfile']
        _done_file = env.analysis(_cid, ana)['donefile']
        # check if process already runs
        if is_done[ana] or os.path.isfile(_done_file):
            print('[ANALYSIS] process ' + ana + ': done!')
            is_done[ana] = True
        elif os.path.isfile(_lock_file):
            print('[ANALYSIS] process ' + ana + ': running!')
        else:
            print('[ANALYSIS] process ' + ana + ': start!')
            # send request
            _target = job_mng.html_target(ana)
            _payload = form_data
            _payload['lockfile'] = _lock_file
            _payload['donefile'] = _done_file
            _payload['outfile'] = env.analysis(_cid, ana)['outfile']
            _payload['datadir'] = env.analysis(_cid)['datadir']
            _payload['analysis'] = ana.lower()
            _req = requests.post(_target, data=_payload)

    # if all analyses ready, produce final result file
    if all(is_done[x] for x in is_done):
        print("[ANALYSIS] create summary file ...")
        collect_results(_analyses, form_data)
        return 'DONE'

    print("[ANALYSIS] wait for results ...")
    time.sleep(2)

    return 'WAIT'
