import json
import os
import sys

import analysis


def backend_get(url):
    filepath = 'storage/result.json'
    if os.path.isfile(filepath):
        print("Returning analysis result of {} to FE ...".format(url))
        with open(filepath) as f:
            json_data = json.load(f)
        print('json data from within backend:')
        print(json_data)
        return json_data
    else:
        analysis.perform_analysis(url)
        return backend_get(url)


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'www.script.backend.example.com'
    backend_get(url)
