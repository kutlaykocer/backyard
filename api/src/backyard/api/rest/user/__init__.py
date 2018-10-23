import connexion
import flask
from decorator import decorator


def check_auth(username: str, password: str):
    '''This function is called to check if a username /
    password combination is valid.'''
    return username == 'admin' and password == 'secret'


def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return flask.Response('You have to login with proper credentials', 401,
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})


@decorator
def requires_auth(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f(*args, **kwargs)


@requires_auth
def login() -> str:
    # TODO return JWT
    return 'OK'


@requires_auth
def logout():
    return 'OK'