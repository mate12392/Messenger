from . import db
from flask_login import UserMixin
from sqlalchemy import func

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reciever_id = db.Column(db.Integer)
    like = db.relationship('Like')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    tweet = db.relationship('Message')
    follow = db.relationship('Friend')
    like = db.relationship('Like')

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_user_id = db.Column(db.Integer, unique=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like_type = db.Column(db.String(150))
    liker_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_tweet_id = db.Column(db.Integer, db.ForeignKey('message.id'))