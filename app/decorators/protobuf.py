from functools import wraps

from flask import Response, abort, g, request
from google.protobuf.message import Message


def receive_protobuf_message(model):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            protobuf_instance = model()

            try:
                protobuf_instance.ParseFromString(request.data)
            except TypeError as e:
                abort(400, e.args)

            g.request = protobuf_instance

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def response_with_protobuf(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response = fn(*args, **kwargs)

        if isinstance(response, Message):
            response_obj = Response(response.SerializeToString())
        elif isinstance(response, bytes):
            response_obj = Response(response)
        elif isinstance(response, tuple):
            response_obj = Response(response[0], *response[1:])
        else:
            response_obj = response

        response_obj.mimetype = 'application/vnd.google.protobuf'

        return response_obj

    return wrapper
