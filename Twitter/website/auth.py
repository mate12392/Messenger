from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rem = request.form.get('rem')


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password. Try again!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()


        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Invalid Email', category='error')
        elif len(username) < 2:
            flash('Username must be greater then 1 characters', category='error')
        elif password1 != password2:
            flash('Your passwords don\'t match', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, name=f"{first_name} {last_name}", password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))


    return render_template("signup.html", user=current_user)
