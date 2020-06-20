from . import auth
from flask import render_template,redirect,request,url_for,flash
from .forms import RegistrationForm,LoginForm
from app.models import User
from flask_login import login_user,login_required,logout_user
from .. import db
# from ..send_mail import mail_message

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,username = form.username.data,category = form.category.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        
        flash('Account successfully created!')
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',form=form,title='Create Account')

@auth.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            
            flash('Invalid username or Password')

    title = "blog login"
    return render_template('auth/login.html',title=title,form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))