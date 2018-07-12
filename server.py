"""Foundation project"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug import secure_filename
from model import User, Brand, Foundation, UserImage, Recommendation, connect_to_db, db
import os
import datetime


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/vagrant/src/Foundation_Project/static/uploads"

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/registration', methods=["GET"])
def index():
    """Render Registration Form"""

    years = range(1990, 2019)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    days = range(1, 32)

    return render_template("registration_form.html", years=years, months=months, days=days)


@app.route('/registration', methods=["POST"])
def add_user_to_db():
    """Add user info from Registration Form to DB"""

    fname = request.form.get("first_name")
    print(fname)
    lname = request.form.get("last_name")
    email = request.form.get("email")

    birth_month = request.form.get("birthday_month")
    birth_day = request.form.get("birthday_day")
    birth_year = request.form.get("birthday_year")
    birthday_string = "{}-{}-{}".format(birth_month, birth_day, birth_year)
    birthday = datetime.datetime.strptime(birthday_string, "%B-%d-%Y")

    print(birthday)

    create_date = datetime.datetime.utcnow()
    print(create_date)

    user = User(fname=fname, lname=lname, email=email, birthday=birthday, create_date=create_date)

    db.session.add(user)

    db.session.commit()

    return redirect("/login")


@app.route('/login', methods=["GET"])
def display_login_form():
    return render_template("login_form.html")


@app.route('/submit_image', methods=["GET"])
def show_submission_form():
    """Render Upload Form"""

    return render_template("upload_form.html")


@app.route('/submit_image', methods=["POST"])
def upload_file():
    """Save User Image"""

    f = request.files['userimage']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'file uploaded successfully'


if __name__ == "__main__":
    # We have to set debug=True here, since it hcdas to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
