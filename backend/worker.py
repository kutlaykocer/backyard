import json
import datetime
import time

from tqdm import tqdm


def gather_data(form_data):
    filepath = 'data/data_{}.json'.format(form_data['id'])

    print('Gathering data ...')
    # gather dummy data
    result = {
        "id": form_data['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain']
        }
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- finding important data, part {} ...'.format(i))

    print('Storing results in ' + filepath)
    with open(filepath, 'w') as outfile:
        json.dump(result, outfile)
