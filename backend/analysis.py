import datetime
import glob
import json
import time

from tqdm import tqdm


def perform_analysis(form_data):

    # check what data files are available
    filepath = 'data/{}/data_*'.format(form_data['id'])
    data_files = glob.glob(filepath)

    # if no data, call worker
    if not data_files:
        print('[ANALYSIS] no data files available')
        return None

    print("[ANALYSIS] found those datafiles:")
    for file in data_files:
        print('[ANALYSIS] - ' + file)

    # if data, perform analysis
    print('[ANALYSIS] perform analysis ...')
    outfilepath = 'results/{}/result.json'.format(form_data['id'])
    # dummy analysis
    result = {
        "id": form_data['id'],
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        "URL": form_data['url'],
        "domain": form_data['domain'],
        "info": "Everything is analyzed!",
        "data_files": data_files,
        }
    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('[ANALYSIS] - doing important analysis work, part {} ...'.format(i))

    print('[ANALYSIS] Storing results in ' + filepath)
    with open(outfilepath, 'w') as outfile:
        json.dump(result, outfile)

    return result
