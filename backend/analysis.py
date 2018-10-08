import json
import sys
import time

from tqdm import tqdm


def perform_analysis(form_data):
    filepath = 'data/data_{}.json'.format(form_data['id'])
    outfilepath = 'data/result_{}.json'.format(form_data['id'])

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
