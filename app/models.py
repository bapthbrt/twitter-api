import uuid
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.event import listens_for
from sqlalchemy.schema import ForeignKey

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship("User", back_populates="tweets")

    def __repr__(self):
        return f"<Tweet #{self.id}>"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(200))
    api_key = db.Column(db.String(80))
    tweets = db.relationship('Tweet', back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def check_api_key(self, api_key):
        return db.session.query(User).filter_by(api_key=api_key).first()

@listens_for(User, 'before_insert')
def generate_license(mapper, connect, self):
    if not self.api_key:
        self.api_key = str(uuid.uuid4())
    return self.api_key
