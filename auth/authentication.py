from flask import request
from models.models import ModelUsers


def basic_auth(func):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_user(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated


def check_user(username, password):
    auth_response = ModelUsers.query.filter_by(username=username).first()
    return username == auth_response.username and password == auth_response.passwords


def authenticate():
    return {"Message": "Access Denied, Wrong username or password"}, 401
