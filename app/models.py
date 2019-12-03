from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    bio = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic_path = db.Column(db.String(20), nullable=False,
                           default='default.png')
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='posts', lazy="dynamic")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    posted_by=db.Column(db.String(255))
    username = db.Column(db.String)
    posted_on=db.Column(db.DateTime,default=datetime.utcnow)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()


    @classmethod
    def get_comments(cls,id):       
        comments=Comment.query.filter_by(post_id=id).all()
        return comments


class Quote:
  '''
  class that defines instances for a quote
  '''
  def __init__(self,author,quote):
    self.author=author
    self.quote=quote