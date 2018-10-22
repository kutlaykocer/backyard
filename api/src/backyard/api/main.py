#!/usr/bin/env python3
import sys
import signal
import backyard.api.proto.api_pb2 as api
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

nc = NATS()

async def run(loop):

    def status_message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a status message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    async def analyzer_request_handler(msg):
        r = api.AnalyserResponse()
        r.code = api.OK
        r.id = "0c5b48b2-d605-11e8-9930-c6851f433179"

        await nc.publish(msg.reply, r.SerializeToString())

    # Subscribe for status messages
    try:
        await nc.connect("localhost:4222", loop=loop)
    except ErrNoServers as e:
        print(e)
        return

    await nc.subscribe("analyzer.status", cb=status_message_handler)
    await nc.subscribe("analyzer.request", cb=analyzer_request_handler)

    # Send a request to the analyzer service
    ar = api.AnalyserRequest()
    ar.domain = "bash.org"
    ar.scanner = api.HARVESTER | api.SPIDERFOOT

    try:
        response = await nc.request("analyzer.request", ar.SerializeToString(), 0.050)
        resp = api.AnalyserResponse()
        resp.ParseFromString(response.data)
        print("Received response: {message}".format(
            message=resp))
    except ErrTimeout:
        print("Request timed out")


def ask_exit():
    for task in asyncio.Task.all_tasks():
        task.cancel()

    nc.close()
    print("Exiting")
    sys.exit()


def main():
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, ask_exit)

    asyncio.async(run(loop))
    loop.run_forever()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.remove_signal_handler(sig)

if __name__ == "__main__":
    main()
