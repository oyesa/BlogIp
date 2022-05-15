from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime




# Roles table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'

#user table

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    name = db.Column(db.String(255))
    # email = db.Column(db.String(255), unique=True, index=True)
    # password_hash = db.Column(db.String(255))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # bio = db.Column(db.String(255))
    # profile_pic_path = db.Column(db.String())
    # pass_secure = db.Column(db.String(255))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # posts = db.relationship('Post', backref='user', lazy='dynamic')
    # comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'