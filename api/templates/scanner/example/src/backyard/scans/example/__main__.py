import asyncio
import motor.motor_asyncio
import os
import time
import random
import backyard.api.proto.api_pb2 as api
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

nc = NATS()


async def run(loop):
    analyzer_id = os.environ['ANALYZER']
    domain = os.environ['DOMAIN']

    # Connect to nats
    try:
        print('connecting to nats server...')
        await nc.connect("localhost:4222", loop=loop)
    except ErrNoServers as e:
        print('failed to connect to nats', e)
        return

    # Connect to database
    client = motor.motor_asyncio.AsyncIOMotorClient()
    db = client['backyard']

    # start the dummy process
    runtime = 60
    now = 0

    try:
        status = api.JobStatus()
        status.id = analyzer_id
        status.status = api.SCANNING
        while status.completed < 100:
            wait_for = random.randint(1, 5)
            now += wait_for
            time.sleep(wait_for)
            status.completed = min(100, round(100/runtime * now))
            print('sending %s completed to nats topic: scanner.%s.status' % (status.completed, analyzer_id))
            nc.publish('scanner.%s.status' % analyzer_id, status.SerializeToString())

        status.completed = 100
        nc.publish('scanner.%s.status' % analyzer_id, status.SerializeToString())
    except Exception as e:
        print('Error: %s' % e)

    # write data to db


def main():
    print('starting...')
    loop = asyncio.get_event_loop()
    task = loop.create_task(run(loop))
    loop.run_until_complete(task)
    print('done')


if __name__ == "__main__":
    main()
