import json
import sys
import time

from tqdm import tqdm


def perform_analysis(url):
    filepath = 'data/data_{}.json'.format(url)
    outfilepath = 'data/result_{}.json'.format(url)

    print('Performing analysis ...')
    # dummy analysis
    json_data = {}
    with open(filepath) as f:
        json_data = json.load(f)
    json_data["info"] = "Everything is analyzed!"
    result = json_data
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- doing important analysis work, part {} ...'.format(i))

    print('Storing results in ' + filepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'www.analysis.backend.example.com'
    perform_analysis(url)
