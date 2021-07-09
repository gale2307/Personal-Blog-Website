from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import InputRequired

class BlogForm(FlaskForm):
    title = StringField('Blog Title', validators = [InputRequired()])
    content = TextAreaField('Content', validators = [InputRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    #image = FileField('Image')
    tags = SelectMultipleField('Tags', coerce=int)#assign form.tags.choices with the list of choices later in app.py
    submit = SubmitField('Submit Blog')