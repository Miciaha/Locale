from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm, AddressForm
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

from models import User

app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

        if user is not NONE and user.check_password(password):
            session['email'] = form.email.data
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
            #handle form submission
            pass

    elif request.method == 'GET':
        return render_template("home.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
