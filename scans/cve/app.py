"""A webapp."""
import itertools
import os

import flask


app = flask.Flask(__name__)
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


@app.route('/', methods=['POST'])
def request_result():
    """Call nmap."""
    # extract products from html payload
    _products = []
    for i in itertools.count():
        _product = flask.request.form.get('product' + str(i))
        if _product is None:
            break
        _products.append(_product)
    print('Find vulns of those products:', _products)

    # define output files
    _result_file = "/data/scan_results/{}/data_cve.xml".format(flask.request.form['id'])

    # define commands
    _cmds = []
    _cmds.append('touch ' + _result_file)
    for product in _products:
        _cmds.append("curl https://cve.circl.lu/api/search/{} >> {}".format(product, _result_file))

    # run it
    for cmd in _cmds:
        print("Executing: " + cmd)
        os.system(cmd)

    # return something
    return 'Finished!'


if __name__ == '__main__':
    _port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=_port)
