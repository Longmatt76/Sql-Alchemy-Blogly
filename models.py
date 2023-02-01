"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from flask_validator import ValidateLength
import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

  
    def __repr__(self):
        u= self
        return f"<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url ={u.image_url}>"
    
    

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                     nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default="https://www.seekpng.com/png/detail/245-2454602_tanni-chand-default-user-image-png.png")
    
    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True,
                               autoincrement=True)

    title = db.Column(db.String(25), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))





