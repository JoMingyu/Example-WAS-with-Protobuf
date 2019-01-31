from functools import wraps

from flask import g, abort, request


def receive_protobuf(model):
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
