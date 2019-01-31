from flask import Response, abort, g
from peewee import IntegrityError
from werkzeug.security import generate_password_hash

from app.decorators.protobuf import receive_protobuf_message
from app.models.user import TblUsers
from app.views.base import BaseResource
from app.views.user.user_pb2 import SignupRequest


class Signup(BaseResource):
    @receive_protobuf_message(SignupRequest)
    def post(self):
        payload = g.request

        id = payload.id
        pw = payload.pw
        name = payload.name

        try:
            TblUsers.insert(
                id=id,
                pw=generate_password_hash(pw),
                name=name
            ).execute()
        except IntegrityError:
            abort(409)

        return Response(None, 201)
