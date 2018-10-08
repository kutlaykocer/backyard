import json
import os
import sys

import analysis
import worker


def backend_get(form_data):

    print('Call for info on ' + form_data['id'] + ' ...')

    # Check if (valid, up to date) json is already there and return it
    filepath = 'data/result_{}.json'.format(form_data['id'])
    if os.path.isfile(filepath):
        print('Returning analysis result of customer {} to FE ...'.format(form_data['id']))
        with open(filepath) as f:
            json_data = json.load(f)
        print('json data from within backend:')
        print(json_data)
        return json_data

    # Check if data for analysis is already there and perform analysis
    datapath = 'data/data_{}.json'.format(form_data['id'])
    if os.path.isfile(datapath):
        analysis.perform_analysis(form_data)
        return backend_get(form_data)

    # Gather reconnessaince data
    worker.gather_data(form_data)
    return backend_get(form_data)
