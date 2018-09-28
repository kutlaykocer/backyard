import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    message = ""
    datadir = 'data'
    if os.path.isdir(datadir):
        message += "Folder exists!"
        message += str(os.listdir(datadir))
    else:
        message += "Error: Folder doesn't exist!"
    provider = str(os.environ.get('PROVIDER', 'world'))
    return 'Hello ' + provider + '!\n' + message

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
