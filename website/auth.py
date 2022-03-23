from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if(len(email) < 4):
            flash('Email must be greater than 4 caracters', category = 'error')
        elif(len(first_name)< 2):
            flash('Name must be longer than two letters', category = 'error')
        elif(password1 != password2):
            flash('Passwords do not match.', category='error')
        elif(len(password1) < 7):
            flash('Password must have at least 8 characters.', category='error')
        else:
            flash('You are signed up!', category='success')
            new_user = User(email=email, first_name = first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.seesion.commit()
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")