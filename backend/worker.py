import os
import pathlib
import time

import requests


def gather_data(form_data):
    # make data directory
    pathlib.Path('data/{}'.format(form_data['id'])).mkdir(parents=True, exist_ok=True)

    # call tools
    _tools = ['THEHARVESTER']

    for tool in _tools:
        # check if process already runs
        _lock_file = 'data/{}/lock_{}.txt'.format(form_data['id'], tool)
        if os.path.isfile(_lock_file):
            print('[WORKER] process ' + tool + ': running, wait for it to finish!')
            continue
        else:
            print('[WORKER] process ' + tool + ': start')
        # get environmentals
        _tool_addr = os.environ["{}_PORT_5002_TCP_ADDR".format(tool)]
        _tool_port = os.environ["{}_PORT_5002_TCP_PORT".format(tool)]
        _target = "http://{}:{}/".format(_tool_addr, _tool_port)
        # send request
        _payload = form_data
        _payload['lock_file'] = _lock_file
        _req = requests.post(_target, data=_payload)

    print("[WORKER] wait before returning")
    time.sleep(5)
