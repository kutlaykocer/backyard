import json
import datetime
import sys


def gather_data(url):
    filepath = 'storage/data_{}.json'.format(url)

    print('Gathering data ...')
    result = {"time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", "URL": url}

    print('Storing results in ' + filepath)
    with open(filepath, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'www.worker.backend.example.com'
    gather_data(url)
