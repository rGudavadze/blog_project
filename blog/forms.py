from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length
from blog.models import User

class RegisterFrom(FlaskForm):

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Username with this email address already exists!")

    username = StringField(label='User Name', validators=[Length(min=6), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class BlogForm(FlaskForm):
    title = StringField(label='Blog Title', validators=[DataRequired()])
    post = StringField(label='Post Here', validators=[DataRequired()])
    submit = SubmitField(label="Post")

class CommentForm(FlaskForm):
    comment = StringField(label='Write comment here', validators=[DataRequired()])
    submit = SubmitField(label='Comment')
    