from flask import request

from app.views.base import BaseResource


class Signup(BaseResource):
    def post(self):
        payload = request.json

        return payload, 201
