from flask_wtf import FlaskForm
from wtforms import StringField,TextField,SubmitField,PasswordField,ValidationError,BooleanField,RadioField
from wtforms.validators import DataRequired,Email,EqualTo,Length,InputRequired,ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username=StringField('Type Your Username:',validators=[DataRequired(),Length(min=2, max=30)])
    email=StringField('Enter Your Email Address:', validators=[Email(),DataRequired()])
    category=RadioField('Choose Your Account', validators=[DataRequired()] ,choices=[('Subscriber',"Subscriber"),('Blogger','Blogger')])
    password=PasswordField('Enter Password:',validators=[DataRequired(),EqualTo('password_confirm',message='Passwords Must Match')])
    password_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Create Account')

    def validate_username(self,data):
        if User.query.filter_by(username=data.data).first():
            raise ValidationError('This username is taken! Choose another username.')

    def validate_email(self,data):
        if User.query.filter_by(email=data.data).first():
            raise ValidationError('This email is taken! Choose another email.')

class LoginForm(FlaskForm):
    email=StringField('Enter Your Email Address:', validators=[Email(),DataRequired()])
    password=PasswordField('Enter Password:',validators=[InputRequired()])
    remember=BooleanField('Remember me:')
    submit=SubmitField('Login')
 