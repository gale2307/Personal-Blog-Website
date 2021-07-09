from datetime import datetime
from flask import Flask, jsonify, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from .forms import BlogForm
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogdb.db'
db = SQLAlchemy(app)
INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'

from .models import Blog, Tag
db.create_all()

sample_blog = Blog(blog_id=1, title="This is a sample", content="content")
sample_blog2 = Blog(blog_id=2, title="This is a second sample", content="content")
db.session.add(sample_blog)
db.session.add(sample_blog2)
try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()

sample_tag = Tag(tag_id=1, name="blog")
sample_tag2 = Tag(tag_id=2, name="notes")
db.session.add(sample_tag)
db.session.add(sample_tag2)
try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()


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
        print(form.tags.data)
        filename = secure_filename(form.image.data.filename)
        new_blog = Blog(title=form.title.data, content=form.content.data, feature_image=filename)
        for tag_id in form.tags.data:
            new_blog_tag = Tag.query.get(tag_id)
            new_blog.tags.append(new_blog_tag)
        db.session.add(new_blog)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("create.html", form = form, message = "Failed to create new blog")
        finally:
            db.session.close()

        form.image.data.save('todo/static/' + filename)
        return render_template("create.html", form = form, message = "New blog created")

    print("form not filled properly")
    return render_template("create.html", form = form)

@app.route('/content/<blog_id>', methods=["GET"])
def content(blog_id):
    """Look inside the contents of a blog"""
    blog = Blog.query.get(blog_id)

    return render_template("content.html", blog=blog)
