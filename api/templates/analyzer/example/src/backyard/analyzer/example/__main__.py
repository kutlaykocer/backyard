import asyncio
import json
import tempfile

import motor.motor_asyncio
import os
import backyard.api.proto.api_pb2 as api
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers

nc = NATS()


async def run(loop):
    analyzer_id = os.environ['ANALYZER']
    domain = os.environ['DOMAIN']

    # Connect to database
    client = motor.motor_asyncio.AsyncIOMotorClient()
    db = client['backyard']
    gfs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)

    # Use Motor to put compressed data in GridFS, with filename "my_file".
    async def put_gridfile(data, filename, folder):
        with tempfile.TemporaryFile() as tmp:
            tmp.write(data)
            tmp.seek(0)
            await gfs.upload_from_stream(filename=filename,
                                         source=tmp,
                                         metadata={'contentType': 'application/json',
                                                   'folder': folder})

    # Connect to nats
    try:
        print('connecting to nats server...')
        await nc.connect("localhost:4222", loop=loop)
    except ErrNoServers as e:
        print('failed to connect to nats', e)
        return
    except Exception as e:
        print('Error: %s' % e)

    folder = '/%s/%s' % (domain, analyzer_id)
    status_topic = 'scanner.%s.status' % analyzer_id

    status = api.JobStatus()
    status.id = analyzer_id
    status.status = api.ANALYZING
    await nc.publish(status_topic, status.SerializeToString())
    await nc.flush(0.500)

    # collect scanner result files from gridFs
    cursor = gfs.find({'metadata.folder': folder})

    aggregated_data = {}

    while await cursor.fetch_next:
        grid_data = cursor.next_object()
        if grid_data.filename == 'result.json':
            continue
        data = await grid_data.read()
        aggregated_data[grid_data.filename] = data.decode('utf-8')

    await put_gridfile(json.dumps(aggregated_data, ensure_ascii=False).encode('utf-8'), 'result.json', folder)

    status.status = api.READY
    status.completed = 100
    await nc.publish(status_topic, status.SerializeToString())
    await nc.flush(0.500)

    s = api.ScanCompleted()
    s.id = analyzer_id
    s.path = '%s/result.json' % folder
    await nc.publish('analyzer.status', s.SerializeToString())
    await nc.flush(0.500)
    await nc.drain()


def main():
    print('starting...')
    loop = asyncio.get_event_loop()
    task = loop.create_task(run(loop))
    loop.run_until_complete(task)
    print('done')


if __name__ == "__main__":
    main()
