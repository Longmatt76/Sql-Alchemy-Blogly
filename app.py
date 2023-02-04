"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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
    tags = Tag.query.all()
    
    return render_template('post_form.html', user=user,tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """displays the posts form"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'],
    content=request.form['content'], user=user, tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    """display selected post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    return render_template('posts.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_post_edit_form(post_id):
    """displays the edit form for a selected post"""
    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """edits post and updates the db"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect('/users')



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """deletes a post and updates the db"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')


@app.route('/tags')
def show_tag_list():
    """displays list of tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """shows tag details page"""
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tag_details.html', tag=tag,tag_id=tag_id)


@app.route('/tags/new', methods=['GET'])
def show_tag_form():
    """displays form for adding tags"""
    return render_template('tag_new.html')


@app.route('/tags/new', methods=['POST'])
def create_tag():
    """creates a new tag and updates the db"""
    
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/users')


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag(tag_id):
    """displays the tag edit form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)



@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """edits tag and updates db"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['new_name']
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/users')



@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """deletes tag and updates db"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/users')







