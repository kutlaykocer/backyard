import json
import datetime
import sys
import time

from tqdm import tqdm


def gather_data(id, url, domain):
    filepath = 'data/data_{}.json'.format(id)

    print('Gathering data ...')
    # gather dummy data
    result = {"time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", "URL": url, "domain": domain}
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- finding important data, part {} ...'.format(i))

    print('Storing results in ' + filepath)
    with open(filepath, 'w') as outfile:
        json.dump(result, outfile)
