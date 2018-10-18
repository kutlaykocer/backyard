import time

from tqdm import tqdm


def run(data_dir):
    # dummy data for now
    result = {'ELEET': 31337,
              'some_dir_info': data_dir,
             }

    # wait dummy time
    for i in tqdm(range(0, 10)):
        time.sleep(0.2)
        print('- doing important analysis work, part {} ...'.format(i))

    return result
