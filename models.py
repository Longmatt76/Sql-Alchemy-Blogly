"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from flask_validator import ValidateLength
import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """db model for the User class"""
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
    """db model for the Post class"""
    __tablename__ = 'posts'

    def __repr__(self):
        p= self
        return f"<Post id={p.id}, title={p.title}, content={p.content}, created_at={p.created_at}, user_id={p.user_id}>"

    id = db.Column(db.Integer, primary_key=True,
                               autoincrement=True)

    title = db.Column(db.String(25), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class PostTag(db.Model):
    """model for the posts_tags table which crossrefernces Posts and Tags"""
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    



class Tag(db.Model):
    """db model for the Tag class"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True,
                               autoincrement=True)

    name = db.Column(db.Text,unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')







