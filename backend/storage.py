import json
import os


def check_storage(form_data):
    filepath = 'data/{}/result.json'.format(form_data['id'])

    if not os.path.isfile(filepath):
        return None

    print('[STORAGE] return analysis result of {} ...'.format(form_data['id']))
    with open(filepath) as f:
        json_data = json.load(f)
        # TODO: check if analysis result up to date, if not trigger reprocessing
        return json_data
