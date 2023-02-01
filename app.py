"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()



@app.route('/')
def redirect_users():
    """redirects to user list"""
    return redirect('/users')


@app.route('/users')
def show_user_list():
    '''displays list of all users'''
    users = User.query.all()
    posts = Post.query.all()
    return render_template('users.html', users=users, posts=posts)


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


@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def display_post_form(user_id):
    """displays the posts form"""
    user = User.query.get_or_404(user_id)
    
    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """displays the posts form"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
    content=request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    """display selected post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_post_edit_form(post_id):
    """displays the edit form for a selected post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html')


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """edits post and updates the db"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect('/users')



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')









