import time
import sys

from tqdm import tqdm


def run(data_dir):

    print('Opening datafile in ' + data_dir)

    # dummy data for now
    result = {'number_of_host_IPs': 31337,
              'number_of_emails': 31337,
             }

    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- doing important analysis work, part {} ...'.format(i))

    return result


if __name__ == '__main__':
    run(sys.argv[1])
