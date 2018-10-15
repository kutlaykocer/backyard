import os


if __name__ == '__main__':
    print "Calling the spiderfoot server ..."
    _backend_addr = os.environ["SPIDERFOOT_PORT_5001_TCP_ADDR"]
    _backend_port = os.environ["SPIDERFOOT_PORT_5001_TCP_PORT"]
    _target = "http://{}:{}".format(_backend_addr, _backend_port)
    os.system("python sfcli.py -s {}".format(_target))
