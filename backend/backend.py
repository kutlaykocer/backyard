#!/usr/bin/python

import json
import sys


def backend_get(url):
    print("Returning analysis result of {} to FE:".format(url))
    with open('storage/result.json') as f:
        json_data = json.load(f)
    return json_data


if __name__ == '__main__':
    backend_get(sys.argv[1])
