import uuid
import logging
import backyard.supervisor.config as config
import backyard.api.proto.api_pb2 as api
import backyard.supervisor.scanner as scanner
from backyard.supervisor.mongo import db


async def start(req):
    analyzers = config.Config.get_instance().get_analyzers()

    analyzer = None
    for _analyzer in analyzers:
        if req.analyzer == _analyzer['id']:
            analyzer = _analyzer
            break

    if not analyzer:
        logging.error('unknown analyzer %s', req.analyzer)
        return "", api.ERROR

    a_id = str(uuid.uuid4())

    logging.info('starting scans for analysis:')
    for scan in analyzer['scanners']:
        res = await scanner.start(a_id, scan, req)
        if res != api.OK:
            logging.error('failed to start scanner %s' % scan)
            return "", api.ERROR

    # Save this analyzer run to the db for reference
    collection = db.analyzer
    document = {
        'id': a_id,
        'domain': req.domain,
        'progress': 0.0,
        'completed': False,
        'status': api.PENDING,
        'scanners': analyzer['scanners']
    }
    result = await collection.insert_one(document)
    if result is None:
        logging.error('failed to insert analyzer run')
        return "", api.ERROR

    # If successful, create entry in mongodb
    return a_id, api.OK



async def scan_status_handler(msg):
    req = api.JobStatus()
    req.ParseFromString(msg.data)

    a_id = req.id
    parts = msg.subject.split('.')
    scanner = parts[1]

    #// Current scan/analyzer status
	#Status status = 2;
    #
	#// Optional description i.e. for certain scan stages
	#string description = 3;
    #
	#// Approximated percent completed
	#uint32 completed = 4;

    # analyze id from message
    # domain from analyzer entry
    # scanner type from subject
    # extract status information

    # ready?
    # remove this scanner from mongodb
    # remove this scanner from the current analysis
    # check if all required scans for this analysis have finished

    # when we're ready:
    # logging.info('starting analyzer image %s for domain %s' % (analyzer.image, req.domain))
    # Run docker image/kubernetes POD creation
    return
