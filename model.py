"""Models and database functions for foundation_project db."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


db = SQLAlchemy()


##############################################################################

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(110), nullable=False)
    create_date = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} fname={} lname={} email={} birthday={}>".format(self.user_id, self.fname,
                                                                                 self.lname, self.email,
                                                                                 self.birthday)
class Brand(db.Model):
    """Brand model."""

    __tablename__ = "brands"

    product_id = db.Column(db.String(30), nullable=False, primary_key=True)
    brand_name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    target_url = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Brand product_id={} brand_name={} display_name={} target_url={} rating={}>".format(self.product_id, self.brand_name,
                                                                                                    self.display_name, self.target_url,
                                                                                                    self.rating)


class Foundation(db.Model):
    """Foundation Model"""

    __tablename__ = "foundations"

    sku_id = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.String(30), db.ForeignKey("brands.product_id"), nullable=False)
    foundation_hex_code = db.Column(db.String(20))
    foundation_target_url = db.Column(db.String(150), nullable=False)
    shade_image_url = db.Column(db.String(100), nullable=False)
    hero_image_url = db.Column(db.String(100), nullable=False)

    brand = db.relationship("Brand", backref=db.backref("foundations"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Foundation sku_id={} product_id={} foundation_hex_code={} foundation_target_url={} shade_image_url={} hero_image_url={}>".format(
            self.sku_id, self.product_id, self.foundation_hex_code, self.foundation_target_url, self.shade_image_url, self.hero_image_url)


class UserImage(db.Model):
    """Image Model"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    hex_code = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    image_location = db.Column(db.String(100), nullable=False)

    user = db.relationship("User", backref=db.backref("userimages"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserImage image_id={} hex_code={} user_id={} time_stamp={} image_location={}>".format(self.image_id,
                                                                                                       self.hex_code,
                                                                                                       self.user_id,
                                                                                                       self.time_stamp,
                                                                                                       self.image_location)

class Recommendation(db.Model):
    """Recommendations Model"""

    __tablename__ = "recommendations"

    recommendation_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("images.image_id"), nullable=False)
    sku_id = db.Column(db.Integer, db.ForeignKey("foundations.sku_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    foundation = db.relationship("Foundation", backref=db.backref("recommendations"))
    userimage = db.relationship("UserImage", backref=db.backref("recommendations"))
    user = db.relationship("User", backref=db.backref("recommendations"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recommendation recommendation_id={} image_id{} sku_id={}>".format(self.recommendation_id,
                                                                                   self.image_id, self.sku_id)

class Favorite(db.Model):
    """Favorites Model"""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    sku_id = db.Column(db.Integer, db.ForeignKey("foundations.sku_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    foundation = db.relationship("Foundation", backref=db.backref("favorites"))
    user = db.relationship("User", backref=db.backref("favorites"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Favorite favorite_id={} user_id={} sku_id={}>".format(self.favorite_id, self.user_id, self.sku_id)

class Review(db.Model):
    """Reviews Model"""
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    product_id = db.Column(db.String(30), db.ForeignKey("brands.product_id"), nullable=False)
    review_content = db.Column(db.String(250))

    user = db.relationship("User", backref=db.backref("reviews"))
    product = db.relationship("Brand", backref=db.backref("reviews"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review review_id={} user_id={} product_id={} review_content={}>".format(self.review_id, self.user_id,
                                                                                         self.product_id, self.review_content)


##############################################################################
# Helper functions


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app, db_uri='postgres:///foundation_project'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    init_app()
    connect_to_db(app)
