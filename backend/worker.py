import os
import pathlib
import re
import time

import requests


def gather_data(form_data):
    # make data directory
    _data_dir = 'data/{}'.format(form_data['id'])
    pathlib.Path(_data_dir).mkdir(parents=True, exist_ok=True)

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
        key_list = list(dict(os.environ).keys())
        regex_string = tool.upper() + r'_PORT_\d{4}_TCP_PORT'
        port_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
        port = os.environ[port_key]
        _tool_addr = os.environ["{}_PORT_{}_TCP_ADDR".format(tool.upper(), port)]
        _tool_port = os.environ["{}_PORT_{}_TCP_PORT".format(tool.upper(), port)]
        _target = "http://{}:{}/".format(_tool_addr, _tool_port)
        # send request
        _payload = form_data
        _payload['lock_file'] = _lock_file
        _req = requests.post(_target, data=_payload)

    print("[WORKER] wait before returning")
    time.sleep(5)
