import json
import sys


def perform_analysis(url):
    filepath = 'storage/data_{}.json'.format(url)
    outfilepath = 'storage/result_{}.json'.format(url)

    print('Performing analysis ...')
    json_data = {}
    with open(filepath) as f:
        json_data = json.load(f)
    json_data["info"] = "Everything is analyzed!"
    result = json_data

    print('Storing results in ' + filepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'www.analysis.backend.example.com'
    perform_analysis(url)
