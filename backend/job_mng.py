import os
import re


def html_target(name):
    key_list = list(dict(os.environ).keys())
    regex_string = name.upper() + r'_PORT_\d{4}_TCP_PORT'
    port_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
    _port = os.environ[port_key]
    _addr = os.environ["{}_PORT_{}_TCP_ADDR".format(name.upper(), _port)]
    return "http://{}:{}/".format(_addr, _port)
