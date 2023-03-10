from unittest import TestCase

from app import app
from models import db, connect_db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""

        with app.app_context():
            User.query.delete()
            Tag.query.delete()
            

            user = User( first_name='Test', last_name='User', image_url='https://www.seekpng.com/png/detail/245-2454602_tanni-chand-default-user-image-png.png')
            db.session.add(user)
            db.session.commit()

            tag  = Tag(name='Testie')
            db.session.add(tag)
            db.session.commit()


            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-2 text-center mb-5" >Blogly</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test", "last_name": "User", "image_url": 'https://www.seekpng.com/png/detail/245-2454602_tanni-chand-default-user-image-png.png'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-5 m-3">Users</h2>', html)


    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name": "rad"}
            resp = client.post('/tags/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<button  onclick="location.href=\'/tags/new\'" class="btn btn-success btn-sm m-3" >', html)

