import connexion as connexion
import flask
import backyard.api.proto.api_pb2 as api
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
    if connexion.request.is_json:
        request = connexion.request.get_json()  # noqa: E501
    # Send a request to the analyzer service
    ar = api.AnalyserRequest()
    ar.domain = request.get('domain')
    ar.scanner = request.get('scanner')

    try:
        response = await nc.request("analyzer.request", ar.SerializeToString(), 0.050)
        resp = api.AnalyserResponse()
        resp.ParseFromString(response.data)
        print("Received response: {message}".format(
            message=resp))
        return MessageToJson(resp)
    except ErrTimeout:
        return flask.Response('Request timed out', 504)


def delete(id):  # noqa: E501
    """Delete analysis

    This can only be done by the logged in user. # noqa: E501

    :param id: The ID of the analysis
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def read(id):  # noqa: E501
    """Get analysis by ID

     # noqa: E501

    :param id: The ID of the analysis
    :type id: str

    :rtype: Analysis
    """
    return 'do some magic!'