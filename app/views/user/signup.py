from flask import abort, g
from peewee import IntegrityError

from app.decorators.protobuf import receive_protobuf
from app.models.user import TblUsers
from app.views.base import BaseResource
from app.views.user.user_pb2 import SignupRequest


class Signup(BaseResource):
    @receive_protobuf(SignupRequest)
    def post(self):
        payload = g.request

        id = payload.id
        pw = payload.pw
        name = payload.name

        try:
            TblUsers.insert(
                id=id,
                pw=pw,
                name=name
            ).execute()
        except IntegrityError:
            abort(409)

        return {}, 201
