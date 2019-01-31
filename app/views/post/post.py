from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.decorators.protobuf import receive_protobuf, response_protobuf
from app.models.post import TblPosts
from app.views.base import BaseResource
from app.views.post.post_pb2 import (
    PostCreateRequest, PostCreateResponse,
    PostListResponse
)


class Post(BaseResource):
    @receive_protobuf(PostCreateRequest)
    @response_protobuf
    @jwt_required
    def post(self):
        payload = g.request

        content = payload.content

        id = TblPosts.insert(content=content, author_id=get_jwt_identity()).execute()

        response = PostCreateResponse(
            id=id
        )

        return response.SerializeToString()

    @response_protobuf
    def get(self):
        posts = TblPosts.select().execute()

        response = PostListResponse(
            posts=[PostListResponse.Post(id=post.id, content=post.content) for post in posts]
        )

        return response.SerializeToString()
