def dirs(cid):
    return {
        'datadir': '/data/raw/{}/'.format(cid),
        'resultdir': '/data/results/{}/'.format(cid),
    }


def analysis(cid, name=''):
    _dir = dirs(cid)['resultdir']
    return {
        'outfile': '{}/result_{}.json'.format(_dir, name),
        'resultfile': '{}/result.json'.format(_dir),
        'datadir': dirs(cid)['datadir'],
        'resultdir': _dir,
    }

def worker(cid, name=''):
    _dir = dirs(cid)['datadir']
    return {
        'lockfile': '{}/lock_{}.txt'.format(_dir, name),
        'donefile': '{}/done_{}.txt'.format(_dir, name),
        'resultfile': '{}/result.txt'.format(_dir),
        'datadir': _dir,
    }
