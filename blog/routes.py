from blog import app
from flask import render_template, request, redirect, url_for
from blog.forms import RegisterFrom

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    RegisterFrom()