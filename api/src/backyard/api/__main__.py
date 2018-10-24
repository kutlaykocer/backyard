#!/usr/bin/env python3
import sys
import signal
import backyard.api.proto.api_pb2 as api
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers
from backyard.api.rest.server import RestServer
import logging
from logging.config import dictConfig

logging.basicConfig(level=logging.DEBUG)


dictConfig({
    'version': 1,
    'keys': ['root', 'connexion'],
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
    },
    'connexion': {
        'handlers': ['console'],
        'level': logging.DEBUG,
        'qualname': 'connexion.app'
    }
})

logger = logging.getLogger(__name__)

nc = NATS()


async def run():
    logger.info('initializing nats connection')

    async def analyzer_request_handler(msg):
        r = api.AnalyserResponse()
        r.code = api.OK
        r.id = "0c5b48b2-d605-11e8-9930-c6851f433179"

        await nc.publish(msg.reply, r.SerializeToString())

    # Subscribe for status messages
    try:
        logger.debug('connecting to nats server...')
        await nc.connect("localhost:4222")
    except ErrNoServers as e:
        print(e)
        return

    await nc.subscribe("analyzer.request", cb=analyzer_request_handler)


def main():
    logger.debug('starting...')
    loop = asyncio.get_event_loop()
    task = loop.create_task(run())
    loop.run_until_complete(task)
    server = RestServer()
    server.start(port=8080)


if __name__ == "__main__":
    main()
