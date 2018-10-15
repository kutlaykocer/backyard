import json
import os

import analysis
import storage
import worker


def backend_get(form_data):

    print('Call for info on ' + form_data['id'] + ' ...')

    # Check if (valid, up to date) json is already there and if yes, return it
    result = storage.check_storage(form_data)
    if result:
        return result

    # Check if data for analysis is already there and if yes, perform analysis
    result = analysis.perform_analysis(form_data)
    if result:
        return result

    # Gather reconnessaince data
    worker.gather_data(form_data)
    return backend_get(form_data)
