"""A dummy analysis to provide dummy info until required analyses are available."""
import time
import sys

from tqdm import tqdm


def run(data_dir):
    """Call the analysis."""
    print('Opening datafile in ' + data_dir)

    # dummy data for now
    result = {'interesting_info0': 0,
              'interesting_info1': 1,
              'interesting_info2': 2,
              'interesting_info3': 3,
              }

    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.7)
        print('- doing important analysis work, part {} ...'.format(i))

    return result


if __name__ == '__main__':
    run(sys.argv[1])
