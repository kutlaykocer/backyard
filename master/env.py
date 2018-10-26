"""Definition of names."""


def dirs(cid):
    """Return directory names."""
    return {
        'datadir': '/data/scan_results/{}/'.format(cid),
        'resultdir': '/data/analysis_results/{}/'.format(cid),
        }


def analysis(cid, name=''):
    """Return analysis file names."""
    _dir = dirs(cid)['resultdir']
    return {
        'outfile': '{}/result_{}.json'.format(_dir, name),
        'resultfile': '{}/result.json'.format(_dir),
        'datadir': dirs(cid)['datadir'],
        'resultdir': _dir,
        }


def scan(cid):
    """Return scan file names."""
    _dir = dirs(cid)['datadir']
    return {
        'resultfile': '{}/result.json'.format(_dir),
        'datadir': _dir,
        }
