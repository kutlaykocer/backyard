import logging
import backyard.supervisor.config as config
import backyard.api.proto.api_pb2 as api
from backyard.supervisor.mongo import db


async def start(a_id, scan, req):
    scanners = config.Config.get_instance().get_scanners()

    if not scan in scanners:
        logging.error('unknown scanner %s', scan)
        return api.ERROR

    scanner = scanners[scan]

    # Create a new scanner if not already there
    collection = db.scans
    res = await collection.count_documents({'$and': [{'domain': req.domain}, {'id': scan}]})
    if res == 0:
        logging.info('starting scan %s for %s' % (scan, req.domain))

        # TODO: Run docker image/kubernetes POD creation
        print('DOMAIN="%s" ANALYZER="%s" docker run -i %s' % (req.domain, a_id, scanner['image']))

        # Save this scan to the db for reference
        document = {
            'id': scan,
            'domain': req.domain,
            'progress': 0.0,
            'completed': False,
            'status': api.PENDING
        }
        result = await collection.insert_one(document)
        if result is None:
            return api.ERROR
    else:
        logging.debug('scan %s for %s already exists - not starting another one' % (scan, req.domain))

    # If successful, create entry in mongodb
    return api.OK
