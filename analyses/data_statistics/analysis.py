import datetime
import json
import os
import sys


def run(data_dir):

    result = {
        "time": f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        }

    print('Opening datafiles in ' + data_dir + ':')
    _data_files = os.listdir(data_dir)
    _data_files_info = []
    for file in _data_files:
        print('- ' + file)
        full_path = os.path.join(data_dir, file)
        size = os.path.getsize(full_path)
        info = {'file_name': file, 'size_bytes': size}
        _data_files_info.append(info)

    result['number_of_data_files'] = len(_data_files)
    result['data_files'] = _data_files_info

    with open(os.path.join(data_dir, 'result.json')) as result_file:
        result['scan_info'] = json.load(result_file)

    return result


if __name__ == '__main__':
    run(sys.argv[1])
