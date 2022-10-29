from . import db
from flask_login import UserMixin
from sqlalchemy import func

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    like = db.relationship('Like')
    comment = db.relationship('Comment')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    tweet = db.relationship('Tweet')
    follow = db.relationship('Follow')
    comment = db.relationship('Comment')
    like = db.relationship('Like')

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_user_id = db.Column(db.Integer, unique=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    data = db.Column(db.String(10000))

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liker_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_tweet_id = db.Column(db.Integer, db.ForeignKey('tweer.id'))