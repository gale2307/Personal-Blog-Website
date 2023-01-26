from datetime import datetime
from flask import Flask, jsonify, request, render_template, redirect, session, url_for, abort
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from .forms import BlogForm, SignupForm, LoginForm
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogdb.db'
db = SQLAlchemy(app)
INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'
#login = LoginManager(app) #TODO: Implement flask login
#login.login_view = 'login'

from .models import Blog, Tag, User
db.create_all()

#admin = User(id=1, email="nicholaswilliam2307@gmail.com", username = "admin", password = "admin")
#db.session.add(admin)
#try:
#    db.session.commit()
#except Exception as e:
#    print(e)
#    db.session.rollback()

#admin = User.query.first()
#sample_blog = Blog(blog_id=1, title="This is a sample", content="content")
#admin.blogs.append(sample_blog)
#sample_blog2 = Blog(blog_id=2, title="This is a second sample", content="content")
#admin.blogs.append(sample_blog2)
#db.session.add(sample_blog)
#db.session.add(sample_blog2)
#try:
#    db.session.commit()
#except Exception as e:
#    print(e)
#    db.session.rollback()

#sample_tag = Tag(tag_id=1, name="blog")
#sample_tag2 = Tag(tag_id=2, name="notes")
#db.session.add(sample_tag)
#db.session.add(sample_tag2)
#try:
#    db.session.commit()
#except Exception as e:
#    print(e)
#    db.session.rollback()



@app.route('/', methods=["GET"])
def home():
    """List of routes for this API."""
    blogs = Blog.query.all()
    return render_template("home.html", blogs = blogs)

@app.route('/create', methods=["GET", "POST"])
def create():
    """List of routes for this API."""
    form = BlogForm()
    form.tags.choices = [(tag.tag_id, tag.name) for tag in Tag.query.all()]

    if form.validate_on_submit():
        #print(form.tags.data)
        #user = User.query.get(session['user_id'])
        filename = secure_filename(form.image.data.filename)
        new_blog = Blog(title=form.title.data, content=form.content.data, feature_image=filename, created_by = session['user_id'])
        for tag_id in form.tags.data:
            new_blog_tag = Tag.query.get(tag_id)
            new_blog.tags.append(new_blog_tag)

        #user = User.query.get(session['user_id'])
        #user.blogs.append(new_blog)

        db.session.add(new_blog)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('create.html', form = form, message = 'Failed to create new blog')
        finally:
            db.session.close()

        form.image.data.save('todo/static/' + filename)
        return render_template("create_success.html", message = "New blog created") #TODO: change to redirect to prevent double submission

    print("form not filled properly")
    return render_template('create.html', form = form)

@app.route('/content/<blog_id>', methods=['GET'])
def content(blog_id):
    """Look inside the contents of a blog"""
    blog = Blog.query.get(blog_id)

    return render_template('content.html', blog=blog)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign-up page"""
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('signup.html', form = form, message = 'Failed to sign up')
        finally:
            db.session.close()

        user = User.query.filter_by(username = form.username.data, password=form.password.data).first()
        session['user_id'] = user.id
        return redirect(url_for('home'))

    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data, password=form.password.data).first()
        if user is None:
            abort(404, description="No user was found")
        else:
            session['user_id'] = user.id
            return redirect(url_for('home'))

    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET'])
def logout():
    """Logout view"""
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/user/<user_id>', methods=['GET'])
def user_page(user_id):
    """User page, contains their posts"""
    blogs = Blog.query.filter_by(created_by = user_id)
    return render_template("home.html", blogs = blogs)

@app.route('/search', methods=['GET'])
def search():
    """Search page"""
    return None

@app.route('/search/<query>', methods=['GET'])
def search_results(query):
    """Search results (for title based searches)"""
    return None