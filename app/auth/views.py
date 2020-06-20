from . import auth
from flask import render_template,redirect,request,url_for,flash,abort
from .forms import RegistrationForm,LoginForm
from app.models import User
from flask_login import login_user,login_required,logout_user
from app import db
from app.email import mail_message

@auth.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,category=form.category.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account successfully created!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form,title='Create Account')

@auth.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            flash('Login successful! Welcome to Blog Arena')

    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))