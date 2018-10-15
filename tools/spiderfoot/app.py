from __future__ import print_function

import os


# TODO: make it a webserver and accept url from http request

if __name__ == '__main__':
    url = 'spiderfoot@gmail.com'
    print("Calling the spiderfoot server to analyse {} ...".format(url))

    # get environmentals
    _backend_addr = os.environ["SPIDERFOOT_PORT_5001_TCP_ADDR"]
    _backend_port = os.environ["SPIDERFOOT_PORT_5001_TCP_PORT"]
    _target = "http://{}:{}".format(_backend_addr, _backend_port)

    # configure scans
    _cmd_file = 'sf_cmd.txt'
    modules = ['sfp_pwned']
    with open(_cmd_file, 'w') as f:
        print('start {} -m {}'.format(url, ','.join(modules)), file=f)

    # configure output
    _output_file = 'sf_output.txt'
    _log_file = 'sf_log.txt'

    # run it
    _cmd = "python sfcli.py -s {} -e {} -o {} -l {}".format(_target, _cmd_file, _output_file, _log_file)
    print("Executing: " + _cmd)
    os.system(_cmd)
