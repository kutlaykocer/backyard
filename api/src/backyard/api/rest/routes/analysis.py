import backyard.api.proto.api_pb2 as api
from aiohttp import web
from backyard.api.__main__ import nc
from google.protobuf.json_format import MessageToJson
from nats.aio.errors import ErrTimeout


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
    return web.Response(text='OK')


async def read(id):  # noqa: E501
    """Get analysis by ID

     # noqa: E501

    :param id: The ID of the analysis
    :type id: str

    :rtype: Analysis
    """
    return web.Response(text='OK')
