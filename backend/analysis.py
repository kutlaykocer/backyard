import datetime
import json


def perform_analysis(url='www.analysis.backend.example.com'):
    filepath = 'storage/result.json'

    print('Performing analysis ...')
    result = {"info": "Everything is analyzed!", "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", "URL": url}

    print('Storing results in ' + filepath)
    with open(filepath, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    perform_analysis()
