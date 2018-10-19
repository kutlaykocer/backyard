import os
import pathlib
import time

import requests

import env
import job_mng


def gather_data(form_data):
    _tools = ['THEHARVESTER']

    _cid = form_data['id']

    # make data directory
    pathlib.Path(env.worker(_cid)['datadir']).mkdir(parents=True, exist_ok=True)

    # print tools
    print("[WORKER] running these tools:")
    for tool in _tools:
        print('[WORKER] - ' + tool)
    is_done = {a: False for a in _tools}

    # call tools
    for tool in _tools:
        # check if process already runs
        _lock_file = env.worker(_cid, tool)['lockfile']
        _done_file = env.worker(_cid, tool)['donefile']
        if is_done[tool] or os.path.isfile(_done_file):
            print('[WORKER] process ' + tool + ': done!')
            is_done[tool] = True
        elif os.path.isfile(_lock_file):
            print('[WORKER] process ' + tool + ': running!')
        else:
            print('[WORKER] process ' + tool + ': start!')
            # send request
            _target = job_mng.html_target(tool)
            _payload = form_data
            _payload['lockfile'] = _lock_file
            _payload['donefile'] = _done_file
            _req = requests.post(_target, data=_payload)

    # if all analyses ready, produce final result file
    if all(is_done[x] for x in is_done):
        print("[WORKER] done!")
        for tool in _tools:
            os.system('rm ' + env.worker(_cid, tool)['donefile'])
        os.system('touch ' + env.worker(_cid)['resultfile'])
        return 'DONE'

    print("[WORKER] wait for results ...")
    time.sleep(2)

    return 'WAIT'
