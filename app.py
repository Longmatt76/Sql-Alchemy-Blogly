"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


@app.route('/')
def redirect_users():
    """redirects to user list"""
    return redirect('/users')


@app.route('/users')
def show_user_list():
    '''displays list of all users'''
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details of a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user, user_id=user_id)


@app.route('/users/new', methods=['GET'])
def show_form():
    """displays create user form"""
    return render_template('form.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """creates a new user and sends the user data to the db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name or None, last_name=last_name or None,
                    image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_page(user_id):
    """displays the edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """updates user info and sends it to db"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] 


    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes a user and posts to the db"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')









