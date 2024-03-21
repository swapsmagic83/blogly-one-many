from flask import Flask, render_template, request,redirect
from flask_debugtoolbar import DebugToolbarExtension
#from sqlalchemy import text
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='abcd'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug= DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('list.html',users=users)

@app.route('/users/new')
def new_user_form():
    return render_template('form.html')

@app.route('/users/new',methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    #posts = Post.query.get(user_id)
    return render_template('details.html',user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def edit_user(user_id):
    user= User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user.first_name= first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete',methods=["POST"])
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('postform.html',user=user)

@app.route('/users/<int:user_id>/posts/new',methods=["POST"])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title,content=content,user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
    

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('postedit.html',post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form["title"]
    content = request.form["content"]
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")
    
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('alltags.html',tags=tags)

@app.route('/tags/new')
def add_tag():
    posts = Post.query.all()
    return render_template('newtag.html',posts=posts)

@app.route('/tags/new',methods=["POST"])
def post_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    name= request.form["name"]
    new_tag = Tag(name=name,posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('showtag.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edittag.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def post_edittag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name= request.form["name"]
    tag.name= name
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete',methods=["POST"])
def delete_tag(tag_id):
    tag=Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
