from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length

class RegisterFrom(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=6), DataRequired()])
    email = StringField(label='Email Adress', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo(password), DataRequired()])
    submit = SubmitField(label='Create Account')