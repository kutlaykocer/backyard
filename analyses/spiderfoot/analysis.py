"""A dummy analysis to provide dummy info until required analyses are available."""
import json
import time
import sys


def run(data_dir):
    """Call the analysis."""
    print('Opening datafile in ' + data_dir)

    # dummy data for now
    cyber_risk = {'general': 8}
    cyber_risk_change_history = {'general': [5, 5, 4, 8, 8, 9, 8]}
    result = {
        'top': {
            'cyber_risk': cyber_risk,
            'cyber_risk_change_history': cyber_risk_change_history,
            },
        'mid': {
            'statistics': {
                'unique_emails': 23,
                'unique_emails_last': 26,
                'certificate_warnings': 3,
                'risk_high': 8,
                'risk_mid': 20,
                'risk_low': 128,
            },
        },
        'low': {
            'findings':
                [
                    {'cat': 'email', 'fnd': 'hans.dampf@test.de', 'rel': 5, 'src': ['OWA', 'mail_leak'], 'risk': 6, 'mtg': 'change password, update '},
                    {'cat': 'email', 'fnd': 'franz.dampf@test.de', 'rel': 3, 'src': ['mail_leak'], 'risk': 2, 'mtg': 'change password'},
                    {'cat': 'email', 'fnd': 'heinz.dampf@test.de', 'rel': 9, 'src': ['mail_leak'], 'risk': 4, 'mtg': 'change password'},
                ],
            },
        }

    time.sleep(2)
    print(json.dumps(result, indent=4))


    return result


if __name__ == '__main__':
    run(sys.argv[1])
