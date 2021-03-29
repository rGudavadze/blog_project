from blog import app, db
from flask import render_template, request, redirect, url_for, flash
from blog.forms import RegisterFrom
from blog.models import User

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
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