"""Communication with the scans."""
import datetime
import pathlib
import json

import requests
import threading

import env
import job_mng


def gather_data(form_data):
    """Call the scans."""
    _scans = ['THEHARVESTER', 'SPIDERFOOT']

    _cid = form_data['id']

    # make data directory
    pathlib.Path(env.scan(_cid)['datadir']).mkdir(parents=True, exist_ok=True)

    # print scans
    print("[SCAN] running these scans:")
    for scan in _scans:
        print('[SCAN] - ' + scan)

    def _req(scan):
        _target = job_mng.html_target(scan)
        _payload = form_data
        return requests.post(_target, data=_payload)

    # call scans
    threads = []
    for scan in _scans:
        print('[SCAN] process ' + scan + ': start!')
        thread = threading.Thread(target=_req, args=(scan,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    _result_file = env.scan(_cid)['resultfile']
    print('[SCAN] Summarize scans in ' + _result_file)

    result = {
        "id": _cid,
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain'],
        "info": "Done",
        "scans": _scans
        }

    with open(_result_file, 'w') as myfile:
        json.dump(result, myfile)

    print("[SCAN] done!")

    return 'DONE'
