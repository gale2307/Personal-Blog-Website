from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import InputRequired, Email, EqualTo

class BlogForm(FlaskForm):
    title = StringField('Blog Title', validators = [InputRequired()])
    content = TextAreaField('Content', validators = [InputRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    tags = SelectMultipleField('Tags', option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), coerce=int)#assign form.tags.choices with the list of choices later in app.py
    submit = SubmitField('Submit Blog')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = StringField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    username = StringField('Username', validators = [InputRequired()])
    password = StringField('Password', validators = [InputRequired()])
    confirm = StringField('Re-enter Password', validators = [InputRequired(), EqualTo('password', message = 'Passwords must match!')])
    submit = SubmitField('Sign up')

class TitleSearchForm(FlaskForm):
    title = StringField('Blog Title', validators = [InputRequired()])
    submit = SubmitField('Search')

class TagSearchForm(FlaskForm):
    tags = SelectMultipleField('Tag Filters', option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), coerce=int, validators = [InputRequired()])
    submit = SubmitField('Search')

