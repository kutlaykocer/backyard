import connexion as connexion


def create(request):  # noqa: E501
    """Start a new analysis

     # noqa: E501

    :param request:
    :type request: dict | bytes

    :rtype: AnalyserResponse
    """
    if connexion.request.is_json:
        request = connexion.request.get_json()  # noqa: E501
    return 'do some magic!'


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