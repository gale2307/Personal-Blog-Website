from .app import db
from datetime import datetime

blog_tag = db.Table('blog_tag',
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.blog_id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
    )

class Tag(db.Model):
    """Tags to describe blog content"""
    tag_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20), nullable=False)

class Blog(db.Model):
    """Blog model"""
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    feature_image= db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=blog_tag, backref='blogs')

    def __init__(self, *args, **kwargs):
        """On construction, set date of creation."""
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()

#class User(db.Model):
#    """User object that creates blogs"""
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.Unicode, nullable=False)
#    email = db.Column(db.Unicode, nullable=False)
#    password = db.Column(db.Unicode, nullable=False)
#    date_joined = db.Column(db.DateTime, nullable=False)
#    token = db.Column(db.Unicode, nullable=False)
#    tasks = db.relationship("Task", back_populates="user")

#    def __init__(self, *args, **kwargs):
#        """On construction, set date of creation."""
#        super().__init__(*args, **kwargs)
#        self.date_joined = datetime.now()
#        self.token = secrets.token_urlsafe(64)