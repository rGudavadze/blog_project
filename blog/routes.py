# pylint: disable=no-member
from blog import app, db
from flask import render_template, request, redirect, url_for, flash, session
from blog.forms import RegisterFrom, LoginForm, BlogForm, CommentForm
from blog.models import User, Post, Comment
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
            return redirect(url_for('blogs'))
        else:
            flash("Username and Password are not match!", category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for('login'))

@app.route('/blogs', methods=['GET', 'POST'])
@login_required
def blogs():
    form = BlogForm()
    if form.validate_on_submit():
        create_blog = Post(title=form.title.data,
                            post=form.post.data)

        db.session.add(create_blog)
        db.session.commit()
        
        create_blog.set_owner()
        
        return redirect(url_for('blogs'))

    q = request.args.get("q")
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.post.contains(q))
    else:
        posts = Post.query.order_by(Post.date.desc()).all()


    return render_template('blogs.html', form=form, posts=posts)

@app.route('/blogs/<int:id>', methods=['GET', 'POST'])
def individual_blog(id):
    form = CommentForm()
    blog = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(owner_post=id).all()
    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data)
        db.session.add(new_comment)
        db.session.commit()

        new_comment.set_comment_owner(id)

        return redirect(f"/blogs/{id}")
    return render_template('individual_blog.html', blog=blog, comments=comments, form=form)