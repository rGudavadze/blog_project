from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SECRET_KEY'] = 'ffcdc129ed8cf399d71b15bd5a5f68e3'
db = SQLAlchemy(app)


from blog import routes