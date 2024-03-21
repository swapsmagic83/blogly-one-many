from app import app
from unittest import TestCase
import unittest
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_one_many_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class userTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Post.query.delete()
        user = User(first_name='userFirstName',last_name='userLastName',image_url='https://images.unsplash.com/photo-1682686581797-21ec383ead02?q=80&w=1587&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        post =Post(title='title',content='content')
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        db.session.rollback()

    def test_user_post(self):
        with app.test_post() as client:
            post = Post(title= 'Flower', content='Looks beautiful')
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id
            res = client.get(f"/posts/{self.post_id}")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Flower</h1>',html)

if __name__ == '__main__':
    unittest.main()
