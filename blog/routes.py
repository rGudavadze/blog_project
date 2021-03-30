# pylint: disable=no-member
from blog import app, db
from flask import render_template, request, redirect, url_for, flash
from blog.forms import RegisterFrom, LoginForm
from blog.models import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterFrom()
    if form.validate_on_submit():
        create_user = User(username=form.username.data,
                            email=form.email.data,
                            password=form.password.data)
        db.session.add(create_user)
        db.session.commit()
        flash(f"Account created successfully! You are now logged in as {create_user.username}", category="success")
        return redirect(url_for('home'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"There was an error with creating a user: {err}", category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_attempt = User.query.filter_by(email=form.email.data).first()
        if user_attempt and user_attempt.check_password(form.password.data):
            login_user(user_attempt)
            flash(f'Success! You are logged in as {user_attempt.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash("Username and Password are not match!", category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for('login'))