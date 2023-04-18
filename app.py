from flask import Flask, render_template,request, redirect, url_for, jsonify, session
import flask_login
import json
import stripe
from flask_mail import Mail, Message
from typing_extensions import Protocol
import werkzeug.exceptions
from flask_session import Session
from pysondb import db

database = db.getDb('db.json')

app = Flask(__name__)
app.secret_key = '0N2Ung7czhpZ25miszKnIQjNnSygDHfU'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)



app = Flask(__name__)
app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


users = {'adrian@hma.tech': {'password': 'hello'}, 'tiana@hma.tech': {'password': 'hello'}, 'ub@getrevscale.com': {'password':'hello'}, 'jess@getrevscale.com': {'password': 'hello'}}


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        email = request.form['email']
        if email in users and request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('protected_app'))

    return 'Bad login'


@app.route('/app', methods=['GET','POST'])
@flask_login.login_required
def protected_app():
    if request.method == "GET":
        return '''
        <!doctype html>
<title>Site Maintenance</title>
<style>
  body { text-align: center; padding: 150px; }
  h1 { font-size: 50px; }
  body { font: 20px Helvetica, sans-serif; color: #333; }
  article { display: block; text-align: left; width: 650px; margin: 0 auto; }
  a { color: #dc8100; text-decoration: none; }
  a:hover { color: #333; text-decoration: none; }
</style>

<article>
    <h1>We&rsquo;ll be launching soon (April 13th)!</h1>
    <div>
        <p>Sorry for the inconvenience. If you need to you can always <a href="mailto:adriancravioto@ktrcapital.org">contact us</a>, otherwise we&rsquo;ll be launching shortly!</p>
        <p>&mdash; Asclepius Team</p>
    </div>
</article>
        '''

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'You are seeing this page because you are trying to access the Ascelepius service and are not logged in. Please login', 401

if __name__ == '__main__':
    app.run(debug=True)
