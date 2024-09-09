from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask

login_manager = LoginManager()
login_manager.login_view = 'login'

# Define a User class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Dummy user store
users = {'admin': 'password'}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
