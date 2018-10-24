#!/usr/bin/env python3
import sys
import signal
import backyard.api.proto.api_pb2 as api
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers
from backyard.api.rest.server import RestServer

nc = NATS()
server = RestServer()

import logging
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'handlers': {
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'console'
        }
    },
    'formatters': {
      'console': {
          'format': '%(log_color)s%(asctime)s %(levelname)s: [%(threadName)s] %(name)s - %(message)s',
          'class': 'colorlog.ColoredFormatter'
      }
    },
    'root': {
        'handlers': ['console'],
        'level': logging.DEBUG
    }
})

logger = logging.getLogger(__name__)


async def run(loop):
    logger.info('initializing nats connection')

    async def analyzer_request_handler(msg):
        r = api.AnalyserResponse()
        r.code = api.OK
        r.id = "0c5b48b2-d605-11e8-9930-c6851f433179"

        await nc.publish(msg.reply, r.SerializeToString())

    # Subscribe for status messages
    try:
        logger.debug('connecting to nats server...')
        await nc.connect("localhost:4222", loop=loop)
    except ErrNoServers as e:
        print(e)
        return

    await nc.subscribe("analyzer.request", cb=analyzer_request_handler)


def ask_exit():
    server.stop()
    
    for task in asyncio.Task.all_tasks():
        task.cancel()

    nc.close()
    logger.info("Exiting")
    sys.exit()


def main():
    logger.debug('starting...')
    server.start(port=8080)
    loop = asyncio.get_event_loop()
    asyncio.async(run(loop))


if __name__ == "__main__":
    main()
