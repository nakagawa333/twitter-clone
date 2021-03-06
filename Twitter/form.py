from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from Twitter.models import User,Post
class RegistrationForm(FlaskForm):
  username = StringField("Username",validators=[DataRequired(),Length(min=4, max=25)])
  email = StringField('Email',validators=[DataRequired(),
  Email()])
  password = PasswordField('Password',validators=[DataRequired()])
  
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
  
  submit = SubmitField('sign in')

class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('login')

class UpdateAccountForm(FlaskForm):
  username=StringField('username',validators=[DataRequired(),Length(min=2,max=30)])
  email = StringField('mail address',validators=[DataRequired(),Email()])
  picture = FileField('picture apdate',validators=[FileAllowed('jpg','png')])
  submit = SubmitField('Update')

  def validate_username(self,username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError("error")
  
  def validate_email(self,email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError("error")

class PostForm(FlaskForm):
  content = TextAreaField('content',validators=[DataRequired])
  submit = SubmitField('Post')
      