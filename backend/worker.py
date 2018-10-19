import os
import pathlib
import time

import requests

import job_mng


def gather_data(form_data):
    _tools = ['THEHARVESTER']

    # make data directory
    _data_dir = '/data/raw/{}'.format(form_data['id'])
    pathlib.Path(_data_dir).mkdir(parents=True, exist_ok=True)

    # call tools
    for tool in _tools:
        # check if process already runs
        _lock_file = 'storage/data/{}/lock_{}.txt'.format(form_data['id'], tool)
        if os.path.isfile(_lock_file):
            print('[WORKER] process ' + tool + ': running, wait for it to finish!')
            continue
        else:
            print('[WORKER] process ' + tool + ': start')
        # send request
        _target = job_mng.html_target(tool)
        _payload = form_data
        _payload['lockfile'] = _lock_file
        _req = requests.post(_target, data=_payload)

    print("[WORKER] wait before returning")
    time.sleep(5)
