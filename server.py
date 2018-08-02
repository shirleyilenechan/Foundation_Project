"""Foundation project"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug import secure_filename
from model import User, Brand, Foundation, UserImage, Recommendation, connect_to_db, db, Favorite, Review
import os
import datetime
from PIL import Image
import requests
import json
from generate_hex import get_hex, match_foundation_shade
from cropped_image import crop_face
from get_twitter_posts import load_tweets

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

    # check to see if this user already exists in our db
    check_existing_user = User.query.filter(User.email == email).first()

    # if user does not exist, then add user to db
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
        return redirect("/login")


@app.route('/login', methods=["GET"])
def display_login_form():
    """Render Login Form"""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def user_login():
    """ checks user login info against the info saved in db """

    email_address = request.form.get("user_email")
    password = request.form.get("user_password")

    #check to see if this user exists in our db
    client = User.query.filter(User.email == email_address).first()

    # if user does not exist, have user register
    if client is None:
        flash("No User Found, Please Register")
        return redirect("/registration")
    # if user exists, then check the password
    else:
        if client.check_password(password):
            session["user_id"] = client.user_id
            return redirect("/home")
        else:
            flash("Password is Incorrect, Please try Again")
            return redirect("/login")


@app.route("/home")
def show_homepage():
    """ renders the hompage """

    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return render_template("homepage.html", user=user)
    else:
        return redirect("/login")


@app.route('/submit_image', methods=["GET"])
def show_submission_form():
    """Render Upload Form"""

    if "user_id" in session:
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

    # if there are no/too many faces detected in our image, flash error and have the user resumbit an image
    if cropped_face is None:
        return "No Image Found"

    else:
        #use the get_hex function to get a hex code for the cropped face image
        face_hex_code = get_hex(20, cropped_face)

        foundations = Foundation.query.filter(Foundation.foundation_hex_code != None).all()
        foundation_hex_codes = []
        for foundation in foundations:
            foundation_hex_codes.append(foundation.foundation_hex_code)

        foundation_hex_codes = list(set(foundation_hex_codes))

        # get the top 6 hex codes of the foundations that match the face
        top_hex_matches = match_foundation_shade(face_hex_code, foundation_hex_codes)
        foundation_matches = []

        # query the database for foundations which match the top 6 hex codes
        for foundation_hex in top_hex_matches:
            foundation = Foundation.query.filter(Foundation.foundation_hex_code == foundation_hex).all()
            foundation_matches.append(foundation)

    user = User.query.get(session["user_id"])
    time_submitted = datetime.datetime.utcnow()

    # add image obj to db
    image_obj = UserImage(hex_code=face_hex_code, user_id=user.user_id,
                          time_stamp=time_submitted, image_location=file_path)

    db.session.add(image_obj)
    db.session.commit()

    #  add recommendation object to db
    for lst in foundation_matches:
        for item in lst:
            recommendation = Recommendation(image_id=image_obj.image_id, user_id=user.user_id, sku_id=item.sku_id)
            db.session.add(recommendation)
    db.session.commit()

    return "Processed Image"


@app.route("/select_image")
def display_user_image():
    """display user images as a link which allows them to select which image they would like to see matches for"""

    # query the db to get the user's images to render the template
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        user_images = user.userimages

        return render_template("display_user_images.html", user_images=user_images)
    else:
        return redirect("/login")


@app.route("/display_matches/<image_id>")
def display_matches(image_id):
    """ display the user's matches for the image user has selected to see matches for """

    if "user_id" in session:

        user = User.query.get(session["user_id"])

        # query the db to find recommendations for that image)
        recommendations = Recommendation.query.filter(Recommendation.user_id == user.user_id, Recommendation.image_id == image_id).all()

        # pass the user image so that we can use the image for the popover later
        image = UserImage.query.filter(UserImage.image_id == image_id).first()

        # pass a list of fondation recommendations
        foundation_products = []

        for recommendation in recommendations:
            sku = recommendation.sku_id
            foundation = Foundation.query.filter(Foundation.sku_id == sku).first()
            foundation_products.append(foundation)

        # pass a list of favorites so that we can display a red heart for favorites
        favorite_skus = db.session.query(Favorite.sku_id).filter(Favorite.user_id == user.user_id).all()

        favorite_skus = set(sku[0] for sku in favorite_skus)

        return render_template("display_matches.html", foundation_products=foundation_products, favorite_skus=favorite_skus, image=image)

    else:
        return redirect("/login")


@app.route("/add_favorite", methods=["POST"])
def add_favorite_db():
    """add a favorite to db"""

    if "user_id" in session:

        sku_id = request.form.get("sku_id")

        user = User.query.get(session["user_id"])

        check_favorite = Favorite.query.filter(Favorite.user_id == user.user_id, Favorite.sku_id == sku_id).first()

        # check to see if the sku that the user click heart on is already in favorites
        # if the sku does not exist, add to favorites and turn heart red
        if check_favorite is None:
            user_favorite = Favorite(sku_id=sku_id, user_id=user.user_id)
            db.session.add(user_favorite)
            db.session.commit()
            return jsonify({"status": "ok"})
        # if the sku already exists in favorites and user clicks heart, then unheart product
        # and remove the sku from favorites
        else:
            db.session.delete(check_favorite)
            db.session.commit()
            return jsonify({"status": "deleted"})

    else:
        return redirect("/login")


@app.route("/add_review", methods=["Post"])
def add_review_db():
    """add a review to db"""

    if "user_id" in session:

        brand_id = request.form.get("brandid")
        review_content = request.form.get("reviewContent")
        user = User.query.get(session["user_id"])

        review = Review(user=user, review_content=review_content, product_id=brand_id)

        db.session.add(review)
        db.session.commit()

        return jsonify({"status": "added review"})

    else:
        return redirect("/login")


@app.route("/view_favorites", methods=["GET"])
def display_favorites():
    """render template display_favorites with user favorites"""

    if "user_id" in session:
        user = User.query.get(session["user_id"])

        # query db for user's favorites and get the hex code for each favorite
        for fav in user.favorites:

            hex_code = fav.foundation.foundation_hex_code

            foundations = Foundation.query.filter(Foundation.foundation_hex_code != None).all()
            foundation_hex_codes = []
            for foundation in foundations:
                foundation_hex_codes.append(foundation.foundation_hex_code)

            # get the top 6 suggestions that most closely match each user favorite
            top_hex_matches = match_foundation_shade(hex_code, foundation_hex_codes)

            # add closest matches attribute to each of the user's favorite foundations
            fav.closest_matches = Foundation.query.filter(Foundation.foundation_hex_code.in_(top_hex_matches)).all()

        favorite_skus = []

        for fav in user.favorites:
            favorite_skus.append(fav.sku_id)

        return render_template("display_favorites.html", favorites=user.favorites, favorite_skus=favorite_skus)

    else:
        return redirect("/login")


@app.route("/brand/<product_id>")
def display_brand(product_id):
    """display brand information, including reviews and twitter carousel"""

    foundation_brand = Brand.query.filter(Brand.product_id == product_id).first()

    reviews = foundation_brand.reviews

    foundation_name = foundation_brand.brand_name

    # call the function that returns twitter media, and pass the tweet information
    # for the twitter carousel
    tweets_lst = load_tweets(foundation_name)

    return render_template("display_brand.html", foundation_brand=foundation_brand, reviews=reviews, tweets=tweets_lst)


@app.route("/logout")
def log_out():
    session.pop("user_id")
    return redirect("/login")


if __name__ == "__main__":

    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
