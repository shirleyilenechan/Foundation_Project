"""Foundation project"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug import secure_filename
from model import User, Brand, Foundation, UserImage, Recommendation, connect_to_db, db
import os
import datetime
from PIL import Image
import requests
import json
from generate_hex import get_hex, match_foundation_shade
from cropped_image import crop_face

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/vagrant/src/Foundation_Project/static/uploads"
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home_page():
    return redirect("/login")

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
    lname = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    check_existing_user = User.query.filter(User.email == email).first()

    if check_existing_user is None:
        birth_month = request.form.get("birthday_month")
        birth_day = request.form.get("birthday_day")
        birth_year = request.form.get("birthday_year")
        birthday_string = "{}-{}-{}".format(birth_month, birth_day, birth_year)
        birthday = datetime.datetime.strptime(birthday_string, "%B-%d-%Y")

        create_date = datetime.datetime.utcnow()

        user = User(fname=fname, lname=lname, email=email, birthday=birthday, create_date=create_date)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    else:
        flash("You have Already Registered, Please Login")
        return redirect("/login")


@app.route('/login', methods=["GET"])
def display_login_form():
    """Render Login Form"""
    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def user_login():
    email_address = request.form.get("user_email")
    password = request.form.get("user_password")

    client = User.query.filter(User.email == email_address).first()

    if client is None:
        flash("No User Found, Please Register")
        return redirect("/registration")
    else:
        if client.check_password(password):
            session["email"] = email_address
            return redirect("/submit_image")
        else:
            flash("Password is Incorrect, Please try Again")
            return redirect("/login")

@app.route('/submit_image', methods=["GET"])
def show_submission_form():
    """Render Upload Form"""

    if "email" in session:
        return render_template("upload_form.html")
    else:
        return redirect("/login")


@app.route('/submit_image', methods=["POST"])
def upload_file():
    """Saves and Processes Submitted Image"""

    # get the user's image and saves it to an upload folder
    f = request.files['userimage']
    filename = secure_filename(f.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(file_path)

    # crop the image to the user's face using the crop_face function
    cropped_face = crop_face(app.config['UPLOAD_FOLDER'], filename)

    # if there are no faces detected in our image, flash error and have the user resumbit an image
    if cropped_face is None:
        flash("No Faces Detected, Please Submit a Different Image")
        return redirect("/submit_image")

    else:
        #use the get_hex function to get a hex code for the cropped face image
        face_hex_code = get_hex(20, cropped_face)

        foundations = Foundation.query.filter(Foundation.foundation_hex_code != None).all()
        foundation_hex_codes = []
        for foundation in foundations:
            foundation_hex_codes.append(foundation.foundation_hex_code)

        # get the top 6 hex codes of the foundations that match the face
        top_hex_matches = match_foundation_shade(face_hex_code, foundation_hex_codes)
        foundation_matches = []

        # query the database for foundations which match the top 6 hex codes
        for foundation_hex in top_hex_matches:
            foundation = Foundation.query.filter(Foundation.foundation_hex_code == foundation_hex).all()
            foundation_matches.append(foundation)

    email = session["email"]
    user = User.query.filter(User.email == email).first()
    time_submitted = datetime.datetime.utcnow()

    # add image obj to db
    image_obj = UserImage(hex_code=face_hex_code, user_id=user.user_id,
                          time_stamp=time_submitted, image_location=file_path)

    db.session.add(image_obj)
    db.session.commit()

    #  add matches to our session to be used in the display matches route
    #  add recommendation object to db
    session["matches"] = []
    for lst in foundation_matches:
        for item in lst:
            session["matches"].append(item.sku_id)
            recommendation = Recommendation(image_id=image_obj.image_id, sku_id=item.sku_id)
            db.session.add(recommendation)
    db.session.commit()

    return redirect("/display_matches")


@app.route("/display_matches")
def display_matches():
    foundation_products = []

    if "matches" in session:
        for sku_id in session["matches"]:
            foundation_match = Foundation.query.filter(Foundation.sku_id == sku_id).first()
            foundation_products.append(foundation_match)

    return render_template("display_matches.html", foundation_products=foundation_products)


@app.route("/logout")
def log_out():
    session.pop("email")
    session.pop("matches")
    return redirect("/login")




if __name__ == "__main__":

    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
