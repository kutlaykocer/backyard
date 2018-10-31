import logging

import motor.motor_asyncio
from aiohttp import web
from backyard.supervisor.mongo import db

logger = logging.getLogger(__name__)


async def read_file(path):  # noqa: E501
    """Access filesystem

    :param path: file path
    :type path: string
    """
    gfs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
    parts = path.split('/')
    file = parts.pop()
    folder = "/".join(parts)
    cursor = gfs.find({'metadata.folder': folder, 'filename': file})

    await cursor.fetch_next
    grid_data = cursor.next_object()
    if grid_data is None:
        raise web.HTTPNotFound()
    data = await grid_data.read()

    return web.Response(body=data.decode('utf-8'), content_type=grid_data.metadata['contentType'])
