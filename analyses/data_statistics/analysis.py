import sys


def run(data_dir):

    print('Opening datafile in ' + data_dir)

    # dummy data for now
    result = {'number_of_host_IPs': 31337,
              'number_of_emails': 31337,
             }

    return result


if __name__ == '__main__':
    run(sys.argv[1])
