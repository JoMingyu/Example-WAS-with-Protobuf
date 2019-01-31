from flask import abort, g
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.decorators.protobuf import receive_protobuf, response_protobuf
from app.models.user import TblUsers
from app.views.base import BaseResource
from app.views.user.user_pb2 import AuthRequest, AuthResponse


class Auth(BaseResource):
    @receive_protobuf(AuthRequest)
    @response_protobuf
    def post(self):
        payload = g.request

        id = payload.id
        pw = payload.pw

        user = TblUsers.get_or_none(
            id=id
        )

        if user is None:
            abort(401)

        if not check_password_hash(user.pw, pw):
            abort(401)

        response = AuthResponse(
            accessToken=create_access_token(identity=user.id)
        )

        return response.SerializeToString()
        # TODO 그냥 protobuf instance만 넘기면 되도록 만들자
