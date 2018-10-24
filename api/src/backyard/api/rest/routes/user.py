from backyard.api.rest.auth import requires_auth


def login() -> str:
    # TODO return JWT
    return 'OK'


@requires_auth
def logout():
    return 'OK'