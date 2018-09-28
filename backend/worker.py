import json
import datetime
import sys
import time

from tqdm import tqdm


def gather_data(url):
    filepath = 'data/data_{}.json'.format(url)

    print('Gathering data ...')
    # gather dummy data
    result = {"time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", "URL": url}
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- finding important data, part {} ...'.format(i))

    print('Storing results in ' + filepath)
    with open(filepath, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'www.worker.backend.example.com'
    gather_data(url)
