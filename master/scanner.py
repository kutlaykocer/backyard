import os
import pathlib

import requests
import threading

import env
import job_mng


def gather_data(form_data):
    _scanners = ['THEHARVESTER']

    _cid = form_data['id']

    # make data directory
    pathlib.Path(env.scanner(_cid)['datadir']).mkdir(parents=True, exist_ok=True)

    # print scanners
    print("[SCANNER] running these scanners:")
    for scanner in _scanners:
        print('[SCANNER] - ' + scanner)

    def _req(scanner):
        _target = job_mng.html_target(scanner)
        _payload = form_data
        return requests.post(_target, data=_payload)

    # call scanners
    threads = []
    for scanner in _scanners:
        print('[SCANNER] process ' + scanner + ': start!')
        thread = threading.Thread(target=_req, args=(scanner,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("[SCANNER] done!")
    os.system('touch ' + env.scanner(_cid)['resultfile'])
    return 'DONE'
