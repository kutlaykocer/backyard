#!/usr/bin/env python3
import sys
import signal
import backyard.api.proto.api_pb2 as api
import backyard.supervisor.config as config
from backyard.supervisor.nats import nc
import backyard.supervisor.analyzer as analyzer
import asyncio
import logging
from logging.config import dictConfig
from nats.aio.errors import ErrNoServers

logging.basicConfig(level=logging.DEBUG)

dictConfig({
    'version': 1,
    'keys': ['root'],
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

    def status_message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a status message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    async def analyzer_request_handler(msg):
        req = api.AnalyserRequest()
        req.ParseFromString(msg.data)

        try:
            a_id, code = await analyzer.start(req)
            resp = api.AnalyserResponse()
            resp.code = code
            resp.id = a_id
        except Exception as e:
            logging.error(e)
        await nc.publish(msg.reply, resp.SerializeToString())

    async def list_analyzer_request_handler(msg):
        r = api.ListAnalyzerResponse()
        r.analyzers = config.Config.get_instance().get_analyzers()
        await nc.publish(msg.reply, r.SerializeToString())

    # Subscribe for status messages
    try:
        logger.debug('connecting to nats server...')
        await nc.connect("localhost:4222", loop=loop)

        # Add a subscription to check for scanner status
        await nc.subscribe('scanner.*.status', cb=analyzer.scan_status_handler)
    except ErrNoServers as e:
        logger.error('failed to connect to nats', e)
        return

    logger.info('listening for analyze requests...')
    await nc.subscribe("scanner.status", cb=status_message_handler)
    await nc.subscribe("analyzer.request", cb=analyzer_request_handler)
    await nc.subscribe("analyzer.list", cb=list_analyzer_request_handler)


def ask_exit():
    for task in asyncio.Task.all_tasks():
        task.cancel()

    nc.close()
    logger.debug('shutting down...')
    sys.exit()


def main():
    config.Config.get_instance()
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, ask_exit)

    asyncio.async(run(loop))
    loop.run_forever()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.remove_signal_handler(sig)


if __name__ == "__main__":
    main()
