from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectField,StringField
from wtforms.validators import DataRequired,Email,Length,ValidationError
from flask_wtf.file import FileField,FileAllowed

class UploadBlog(FlaskForm):
    category=SelectField('Select Blog Category',validators=[DataRequired()],choices=[('Political Blog','Political Blog'),
                                                    ('Business Blog','Business Blog'),
                                                    ('Fashion Blog','Fashion Blog'),
                                                    ('Sports Blog','Sports Blog'),
                                                    ('Entertainment Blog','Entertainment Blog'),
                                                    ('Tech & Innovation Blog','Tech & Innovation Blog'),
                                                    ('Others','None of the above')])
    blog=TextAreaField('Write Blog Here:',validators=[DataRequired()])
    submit=SubmitField('Post Blog')

class Comments(FlaskForm):
    comment=TextAreaField('Write Comment', validators=[DataRequired()])
    submit=SubmitField('Comment')

class UpdateSettings(FlaskForm):
    username=StringField('Type Your Username:')
    email=StringField('Enter Your Email Address:', validators=[Email()])
    bio=TextAreaField('Create Bio:')
    picture=FileField('Choose a Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'])])
    submit=SubmitField('Create Account')

    def validate_username(self,data):
        if data.data != current_user.username:
            if User.query.filter_by(username=data.data).first():
                raise ValidationError('This username is taken! Choose another username.')

    def validate_email(self,data):
        if data.data != current_user.email:
            if User.query.filter_by(email=data.data).first():
                raise ValidationError('This email is taken! Choose another email.')
        
