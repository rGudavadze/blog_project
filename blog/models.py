from blog import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=40), unique=True, nullable=False)
    password = db.Column(db.String(length=40), nullable=False)
    posts = db.relationship('Post', backref='owned_user', lazy=True)
    comments = db.relationship('Comment', backref='owned_user', lazy=True)



class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post = db.Column(db.String(length=1000), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='owned_post', lazy=True)



class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(length=1000), nullable=False)
    like = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    owner_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner_post = db.Column(db.Integer(), db.ForeignKey('post.id'))