"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
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
