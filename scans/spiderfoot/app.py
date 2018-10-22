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
    with open(_cmd_file, 'w') as myfile:
        print(cmd, file=myfile)
    # prepare other input
    _log_file = '/data/scan_results/{}/log_spiderfoot.txt'.format(cid)
    _tmp_log_file = '/data/scan_results/{}/log_spiderfoot_tmp.txt'.format(cid)
    _shell_cmd = "python sfcli.py -s {} -e {} -o {}".format(_target, _cmd_file, _tmp_log_file)
    print("Executing: " + _shell_cmd)
    print("     with: " + cmd)
    # call sf
    os.system('rm ' + _tmp_log_file)
    os.system(_shell_cmd)
    os.system('cat ' + _tmp_log_file + " >> " + _log_file)
    with open(_tmp_log_file, 'r') as myfile:
        output = myfile.read()
    return output


def scan_finished(scans_output):
    return True


def get_spiderfoot_result():
    cid = 'example'
    url = 'spiderfoot@gmail.com'

    # register modules
    modules = ['sfp_pwned', 'sfp_phishtank', 'sfp_pastebin']

    print("Calling the spiderfoot server to analyse {} using those modules:".format(url))
    for module in modules:
        print("- " + module)

    # define run function wrapper
    def run_sf(cmd):
        return run_sf_cid(cmd, cid)

    # run it
    _scan_name = '{}'.format(cid)
    run_sf('start {} -m {} -n {}'.format(url, ','.join(modules), _scan_name))

    # wait for all scans to finish
    output = run_sf('scans -x')

    print('This is the output:')
    print(output)

    is_done = {module: False for module in modules}
    while not all(is_done[module] for module in modules):
        for module in modules:

            is_done[module] = True

    # download results
    _output_file = '/data/scan_results/{}/data_spiderfoot.txt'.format(cid)


if __name__ == '__main__':
    get_spiderfoot_result()
