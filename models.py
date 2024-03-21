from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#def connect_db(app):
#   db.app = app
#    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text,nullable=False)
    last_name = db.Column(db.Text,nullable=False)
    image_url = db.Column(db.Text,nullable=False)
    posts = db.relationship('Post',backref='user')
    def __repr__(self):
        return f"<User id={self.id} First Name={self.first_name} Last Name={self.last_name} Image URL={self.image_url}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text,nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at =db.Column(db.DateTime,nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    #user_post_relation = db.relationship('User',backref='posts')
    tags = db.relationship('Tag',secondary='posts_tags',backref='posts')
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    #posts = db.relationship('Post',secondary='posts_tags',backref='tags')
class PostTag(db.Model):
    __tablename__ = "posts_tags"
    
    post_id= db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True)

def connect_db(app):
    db.app = app
    db.init_app(app)  
#def get_posts():
#    all_posts = Post.query.all()

