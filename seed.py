"""Utility file to seed foundation_project database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from model import Brand, Foundation, connect_to_db, db
from server import app
from datetime import datetime
import requests
import json
from generate_hex import get_hex_url


def load_brand():
    """Load Brands into the database."""

    Brand.query.delete()

    # set payload pageSize to 300--to query for all 226 products currently available on Sephora
    payload = {"pageSize": 300}

    r = requests.get("https://www.sephora.com/api/catalog/categories/cat60004/products?currentPage=1&content=true&includeRegionsMap=true", params=payload)

    brands_json = r.json()

    brands = brands_json["products"]

    # loop through brands list
    for product in brands:
        brand_name = product["brandName"]
        product_id = product["productId"]
        display_name = product["displayName"]
        target_url = "https://www.sephora.com" + product["targetUrl"]
        rating = float(product["rating"])

        # create brand object
        brand = Brand(brand_name=brand_name, product_id=product_id, display_name=display_name,
        target_url=target_url, rating=rating)


        # add and commit brand object to db
        db.session.add(brand)

    db.session.commit()


def load_foundation():
    """Load Foundations into the database."""

    Foundation.query.delete()

    brands = Brand.query.all()

    for brand in brands:
        product_id = brand.product_id

        r = requests.get("https://www.sephora.com/api/users/profiles/current/product/{}?skipAddToRecentlyViewed=false".format(product_id))

        foundations_json = r.json()

        # we should have try except to catch the errors for brands that do not have child skus
        try:
            child_sku = foundations_json["regularChildSkus"]
        except KeyError:
            print("Product {} Contained No Child Skus".format(product_id))
            continue

        # loop through the child skus for products that do have child skus
        for item in child_sku:
            sku_id = item["skuId"]
            foundation_target_url = "https://www.sephora.com" + item["targetUrl"]
            shade_image_url = "https://www.sephora.com/productimages/sku/s{}+sw.jpg".format(sku_id)
            hero_image_url = "https://www.sephora.com/productimages/sku/s{}-main-Lhero.jpg".format(sku_id)

            # create foundation object
            foundation = Foundation(sku_id=sku_id, product_id=product_id, foundation_target_url=foundation_target_url,
                                    shade_image_url=shade_image_url, hero_image_url=hero_image_url)

            # add and commit foundation object to db
            db.session.add(foundation)

    db.session.commit()


def get_hex_code():
    """ add hex codes for each foundation to db """
    # get all foundation objects
    foundations = Foundation.query.all()

    # for each foundation object, assign it a hex code using the get_hex_url function
    # try and except to catch the errors for the foundations that don't have a shade image
    for foundation in foundations:
        try:
            foundation.foundation_hex_code = get_hex_url(3, foundation.shade_image_url)
        except OSError:
            continue

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # create tables
    db.create_all()

    # load_brand()
    # load_foundation()
    # get_hex_code()
