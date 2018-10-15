import json
import os


def check_storage(form_data):
    filepath = 'data/result_{}.json'.format(form_data['id'])

    if not os.path.isfile(filepath):
        return None

    print('Returning analysis result of customer {} to FE ...'.format(form_data['id']))
    with open(filepath) as f:
        json_data = json.load(f)
        print('json data from within backend:')
        # TODO: check if up to date
        print(json_data)
        return json_data
