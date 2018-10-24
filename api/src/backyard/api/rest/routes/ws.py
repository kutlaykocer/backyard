from backyard.api.__main__ import nc


async def subscribe():
    """Websocket endpoint to subscribe to for status updates

    :rtype: JobStatus
    """
    await nc.subscribe("analyzer.status", cb=status_message_handler)

    return 'do some magic!'


def status_message_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a status message on '{subject} {reply}': {data}".format(
        subject=subject, reply=reply, data=data))