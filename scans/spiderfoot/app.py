from __future__ import print_function

import os


# TODO: make it a webserver and accept url from http request


def run_sf_cid(cmd, cid):
    # get environmentals
    _master_addr = os.environ["SCAN_SPIDERFOOT_PORT_5001_TCP_ADDR"]
    _master_port = os.environ["SCAN_SPIDERFOOT_PORT_5001_TCP_PORT"]
    _target = "http://{}:{}".format(_master_addr, _master_port)
    # prepare cmd
    _cmd_file = 'sf_cmd.txt'
    with open(_cmd_file, 'w') as file:
        print(cmd, file=file)
    # prepare other input
    _log_file = '/data/scan_results/{}/log_spiderfoot.txt'.format(cid)
    # call sf
    _shell_cmd = "python sfcli.py -s {} -e {} -o {}".format(_target, _cmd_file, _log_file)
    print("Executing: " + _shell_cmd)
    print("Spiderfoot command:    " + cmd)
    os.system(_shell_cmd)


if __name__ == '__main__':

    cid = 'example'
    url = 'spiderfoot@gmail.com'

    # register modules
    modules = ['sfp_pwned']

    print("Calling the spiderfoot server to analyse {} using those modules:".format(url))
    for module in modules:
        print("- " + module)

    # define run function
    def run_sf(cmd):
        return run_sf_cid(cmd, cid)

    # run it
    _scan_name = 'test0'
    run_sf('start {} -m {} -n {}'.format(url, ','.join(modules), _scan_name))

    # wait for all scans to finish
    run_sf('scans -x')

    is_done = {module: False for module in modules}
    while not all(is_done[module] for module in modules):
        for module in modules:
            is_done[module] = True

    # download results
    _output_file = '/data/scan_results/{}/data_spiderfoot.txt'.format(cid)
