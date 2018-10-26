"""A basic NATS example."""
# based on https://github.com/nats-io/asyncio-nats
import asyncio

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout


async def run(loop):
    """Run the loop."""
    print("Testing NATS communication!")

    nc = NATS()
    await nc.connect("nats://localhost:4222", loop=loop)


    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject}' with reply '{reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("foo", cb=message_handler)

    # Stop receiving after 2 messages.
    await nc.auto_unsubscribe(sid, 2)
    await nc.publish("foo", b'Hello')
    await nc.publish("foo", b'World')
    await nc.publish("foo", b'!!!!!')


    async def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject}' with reply '{reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        await nc.publish(reply, b'I can help')

    # Use queue named 'workers' for distributing requests
    # among subscribers.
    sid = await nc.subscribe("help", "workers", help_request)

    # Send a request and expect a single response
    # and trigger timeout if not faster than 200 ms.
    try:
        response = await nc.request("help", b'help me', 0.2)
        print("Received response: {message}".format(
            message=response.data.decode()))
    except ErrTimeout:
        print("Request timed out")

    # Remove interest in subscription.
    await nc.unsubscribe(sid)

    # Terminate connection to NATS.
    await nc.close()


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(run(_loop))
    _loop.close()
