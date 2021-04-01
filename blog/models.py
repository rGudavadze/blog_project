from blog import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=40), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=40), nullable=False)
    posts = db.relationship('Post', backref='owned_user', lazy=True)
    comments = db.relationship('Comment', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text):
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    post = db.Column(db.String(length=1000), nullable=False)
    rating = db.Column(db.Float(), nullable=False, default=0.0)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='owned_post', lazy=True)

    def set_owner(self):
        self.owner = current_user.id
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(length=1000), nullable=False)
    like = db.Column(db.Integer(), nullable=False, default=0)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    owner_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner_post = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def set_comment_owner(self, post_id):
        self.owner_user = current_user.id
        self.owner_post = post_id
        db.session.commit()