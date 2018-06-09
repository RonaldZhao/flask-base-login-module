import os

from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm
from flask_login import LoginManager, login_user, login_required, current_user,\
    logout_user
from flask_wtf import CsrfProtect

from models import User

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


csrf = CsrfProtect()
csrf.init_app(app)


@app.route('/')
@app.route('/main')
@login_required
def main():
    return render_template('main.html', username=current_user.username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(username, password)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or
                            url_for('main', current_user=current_user))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
