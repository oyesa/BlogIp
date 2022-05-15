from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime





class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # search email in db
    @classmethod
    def search_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user

    # search username in db
    @staticmethod
    def search_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user

    def __repr__(self):
        return f'User {self.username}'


#comment class
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_owner_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #methods to save, get and delete comments
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls):
        comments = Comment.query.all()
        return comments

    @classmethod
    def get_comments_by_post(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id)
        return comments

    @classmethod
    def get_my_posts_comments(cls, user_id):
        comments = Comment.query.filter_by(post_owner_id=user_id)
        return comments

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

    def __repr__(self):
        return f'Comment {self.content}'


#post class
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    image_path = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    #methods to save and obtain info from post
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts

    @classmethod
    def get_user_posts(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id)
        return posts

    @classmethod
    def get_post(cls, id):
        post = Post.query.filter_by(id=id).first()
        return post

    @classmethod
    def get_post_by_category(cls, category_id):
        posts = Post.query.filter_by(category_id=category_id)
        return posts

    def get_comments(self):
        comments = Comment.query.filter_by(post_id=self.id)
        return comments

    @classmethod
    def get_posts_by_query(cls, query):
        posts = Post.query.filter(Post.title.ilike('%' + query + '%'))
        return posts

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Post {self.title}'

#category class
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'