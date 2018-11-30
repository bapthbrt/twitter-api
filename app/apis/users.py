import uuid

from flask_restplus import Namespace, Resource, fields
from flask import abort
from app.models import Tweet, User
from app import db

api = Namespace('users')

# json_user = api.model('User', {
#     'id': fields.Integer,
#     'username': fields.String,
#     'token': fields.String,
#     'tweets': fields.List(Tweet)
# })

json_user = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'api_key': fields.String
})

json_new_user = api.model('New user', {
    'username': fields.String(required=True)
})


@api.route('/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user unique identifier')
class UserResource(Resource):
    @api.marshal_with(json_user)
    def get(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            return user

    @api.marshal_with(json_user, code=200)
    @api.expect(json_new_user, validate=True)
    def patch(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            user.username = api.payload["username"]
            db.session.commit()
            return user

    def delete(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            db.session.delete(user)
            db.session.commit()
            return None


@api.route('')
@api.response(422, 'Invalid user')
class UsersResource(Resource):
    @api.marshal_with(json_user, code=201)
    @api.expect(json_new_user, validate=True)
    def post(self):
        username = api.payload["username"]
        if len(username) > 0:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            return user, 201
        else:
            return abort(422, "Username can't be empty")

    @api.marshal_with(json_user)
    def get(self):
        users = db.session.query(User).all()
        return users, 200
