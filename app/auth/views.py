from . import auth
from .. import db
from ..models import User
from flask import render_template, redirect, url_for, flash, request
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required


#create routes for register and login
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', category='error')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', category='error')
            return redirect(url_for('auth.register'))
        elif len(form.password.data) < 8:
            flash('Password must be at least 7 characters', category='error')
            return redirect(url_for('auth.register'))

        else:
            user = User(email=form.email.data,username=form.username.data,password=form.password.data,name=form.name.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. Please Login', category='success')
            return redirect(url_for('auth.login'))

    title = "Create New Account"
    return render_template('auth/register.html', form=form, title=title)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.profile', username=user.username))
        flash('Invalid username or password', category='error')

    title = "Login to your account"
    return render_template('auth/login.html', form=form, title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', category='success')
    return redirect(url_for('main.index'))