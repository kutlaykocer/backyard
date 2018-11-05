import logging

import backyard.api.proto.api_pb2 as api
import motor.motor_asyncio
from aiohttp import web
from backyard.api import utils
from backyard.api.__main__ import nc
from google.protobuf.json_format import MessageToJson
from nats.aio.errors import ErrTimeout
from backyard.supervisor.mongo import db
from bson.json_util import dumps

logger = logging.getLogger(__name__)


async def create(request):  # noqa: E501
    """Start a new analysis

     # noqa: E501

    :param request:
    :type request: dict | bytes

    :rtype: AnalyserResponse
    """
    # Send a request to the analyzer service
    ar = api.AnalyserRequest()
    ar.domain = request.get('domain')
    ar.analyzer = request.get('analyzer')

    try:
        response = await nc.request("analyzer.request", ar.SerializeToString(), 1.0)
        resp = api.AnalyserResponse()
        resp.ParseFromString(response.data)
        print("Received response: {message}".format(
            message=resp))
        return web.json_response(MessageToJson(resp))
    except ErrTimeout:
        raise web.HTTPGatewayTimeout(reason='Request timed out')


async def delete(id):  # noqa: E501
    """Delete analysis

    This can only be done by the logged in user. # noqa: E501

    :param id: The ID of the analysis
    :type id: str

    :rtype: None
    """
    if not utils.is_uuid(id):
        raise web.HTTPBadRequest(reason='Invalid ID supplied')

    try:
        result = await db.analyzer.deleteOne({'id': id})
        if result.deleted_count == 1:
            return web.Response()
        else:
            raise web.HTTPNotFound(reason='Analysis not found')

    except Exception as e:
        logger.error('Error deleting analyzer entry: %s' % e)
        raise web.HTTPInternalServerError(reason='%s' % e)


async def read(id):  # noqa: E501
    """Get analysis by ID

     # noqa: E501

    :param id: The ID of the analysis
    :type id: str

    :rtype: Analysis
    """
    if not utils.is_uuid(id):
        raise web.HTTPBadRequest(reason='Invalid ID supplied')

    # Load analyzer entry from mongo
    collection = db.analyzer
    document = await collection.find_one({'id': id})
    if document is None:
        raise web.HTTPNotFound(reason='Analysis not found')

    return web.json_response(document, dumps=dumps)


async def listAnalyses():
    """Get a list of analyses"""
    result = []
    cursor = db.analyzer.find()
    for a in await cursor.to_list(length=100):
        result.append(a)

    return web.json_response(result, dumps=dumps)


async def read_result(id):  # noqa: E501
    """Access result.json from filesystem

    :param path: file path
    :type path: string
    """
    collection = db.analyzer
    document = await collection.find_one({'id': id})
    gfs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
    if document is None:
        raise web.HTTPNotFound(reason='Analysis not found')
    folder = "/%s/%s" % (document.domain, id)
    cursor = gfs.find({'metadata.folder': folder, 'filename': 'result.json'})

    await cursor.fetch_next
    grid_data = cursor.next_object()
    if grid_data is None:
        raise web.HTTPNotFound()
    data = await grid_data.read()

    return web.Response(body=data.decode('utf-8'), content_type=grid_data.metadata['contentType'])
