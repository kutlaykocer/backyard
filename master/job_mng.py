"""Helper functions for jobs."""
import os
import re


def html_target(name):
    """Determine html target address."""
    key_list = list(dict(os.environ).keys())

    regex_string = r'.*' + name.upper() + r'_PORT_\d{4}_TCP_PORT'
    port_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
    _port = os.environ[port_key]

    regex_string = r'.*' + name.upper() + r'_PORT_{}_TCP_ADDR'.format(_port)
    addr_key = list(filter(lambda x: re.match(regex_string, x), key_list))[0]
    _addr = os.environ[addr_key]

    # _addr = os.environ["{}_PORT_{}_TCP_ADDR".format(name.upper(), _port)]
    return "http://{}:{}/".format(_addr, _port)
