import os

import flask


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def request_result():
    # get html data
    _form_data = {
        'id': flask.request.form['id'],
        'url': flask.request.form['url'],
        'domain': flask.request.form['domain'],
        'lock_file': flask.request.form['lock_file']
        }
    _id = _form_data['id']
    _url = _form_data["domain"]

    # define output files
    _result_file = "/data/{}/data_theharvester.html".format(_id)

    # define command
    _data_source = "bing"
    _cmd = "theharvester -d {} -b {} -f {}".format(_url, _data_source, _result_file)

    # create lockfile
    os.system('touch {}'.format(_form_data['lock_file']))

    # run it
    print("Executing: " + _cmd)
    os.system(_cmd)

    # once finish, remove lockfile
    os.system('rm {}'.format(_form_data['lock_file']))

    # return something
    return 'Finished: ' + _cmd


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5002.
    _port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=_port)
