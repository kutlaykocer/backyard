import os
import pathlib

import requests
import threading

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

    def _req(tool):
        _target = job_mng.html_target(tool)
        _payload = form_data
        return requests.post(_target, data=_payload)

    # call tools
    threads = []
    for tool in _tools:
        print('[WORKER] process ' + tool + ': start!')
        thread = threading.Thread(target=_req, args=(tool,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("[WORKER] done!")
    os.system('touch ' + env.worker(_cid)['resultfile'])
    return 'DONE'
