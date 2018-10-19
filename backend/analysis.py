import datetime
import glob
import json
import os
import pathlib
import time

import requests

import job_mng


def collect_results(analyses, form_data):

    result = {
        "id": form_data['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain'],
        "info": "Done",
        }

    for analysis in analyses:
        _file_path = '/data/results/{}/result_{}.json'.format(form_data['id'], analysis)
        with open(_file_path) as result_file:
            json_data = json.load(result_file)
            result[analysis] = json_data
        _done_file = '/data/results/{}/done_{}.txt'.format(form_data['id'], analysis)
        os.system('rm {}'.format(_done_file))

    _outfile_path = '/data/results/{}/result.json'.format(form_data['id'])
    print('[ANALYSIS] storing results in ' + _outfile_path)
    with open(_outfile_path, 'w') as outfile:
        json.dump(result, outfile)


def perform_analysis(form_data):
    _analyses = ['data_statistics', 'dummy_analysis']

    _data_dir = '/data/raw/{}/'.format(form_data['id'])
    _result_dir = '/data/results/{}/'.format(form_data['id'])

    # make results directory
    pathlib.Path(_result_dir).mkdir(parents=True, exist_ok=True)

    # check what data files are available
    _data_files = glob.glob(_data_dir + '/data_*')
    if not _data_files:
        print('[ANALYSIS] no data files available')
        return None
    print("[ANALYSIS] found those datafiles:")
    for file in _data_files:
        print('[ANALYSIS] - ' + file)

    # print analyses
    print("[ANALYSIS] running these analyses:")
    for analysis in _analyses:
        print('[ANALYSIS] - ' + analysis)
    is_done = {a: False for a in _analyses}

    # call analyses
    for analysis in _analyses:
        # define files
        _lock_file = '{}/lock_{}.txt'.format(_result_dir, analysis)
        _done_file = '{}/done_{}.txt'.format(_result_dir, analysis)
        _out_file = '{}/result_{}.json'.format(_result_dir, analysis)
        # check if process already runs
        if os.path.isfile(_lock_file):
            print('[ANALYSIS] process ' + analysis + ': running, wait for it to finish!')
            continue
        elif is_done[analysis] or os.path.isfile(_done_file):
            print('[ANALYSIS] process ' + analysis + ': done!')
            is_done[analysis] = True
            continue
        else:
            print('[ANALYSIS] process ' + analysis + ': start')

        # send request
        _target = job_mng.html_target(analysis)
        _payload = form_data
        _payload['lockfile'] = _lock_file
        _payload['donefile'] = _done_file
        _payload['outfile'] = _out_file
        _payload['datadir'] = _data_dir
        _payload['analysis'] = analysis.lower()
        _req = requests.post(_target, data=_payload)

    # if all analyses ready, produce final result file
    if all(is_done[x] for x in is_done):
        print("[ANALYSIS] everything done, create summary file ...")
        collect_results(_analyses, form_data)
        return 'Analyses done!'

    print("[ANALYSIS] wait before returning")
    time.sleep(2)

    return 'Check if done'
