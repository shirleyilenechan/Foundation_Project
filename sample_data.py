from model import User, Brand, Foundation, Favorite, Review, UserImage, Recommendation, db, connect_to_db
import datetime


def example_data():
    UserImage.query.delete()
    Favorite.query.delete()
    Review.query.delete()
    Brand.query.delete()
    Foundation.query.delete()
    Recommendation.query.delete()
    User.query.delete()

    new_user = User(fname="Bobby", lname="Bob", email="bobbybob@gmail.com",
                    create_date=datetime.datetime.utcnow(), birthday="1991-01-12 00:00:00")
    new_user.set_password("1234")
    db.session.add(new_user)
    db.session.commit()

    new_image = UserImage(hex_code="#BA977D", user_id=1, time_stamp=datetime.datetime.utcnow(),
                          image_location="/home/vagrant/src/Foundation_Project/static/uploads/girl-glowing-skin-blue-eyes.jpg")
    db.session.add(new_image)
    db.session.commit()

    new_brand = Brand(product_id="P87985432", brand_name="FENTY BEAUTY by Rihanna",
                      display_name="Pro Filt'r Soft Matte Longwear Foundation",
                      target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432",
                      rating=4.09740000000000038)
    db.session.add(new_brand)
    db.session.commit()

    new_brand_2 = Brand(product_id="P400888", brand_name="Black Up", display_name="Matifying Fluid Foundation",
                        target_url="www.sephora.com/product/matifying-fluid-foundation-P400888",
                        rating=4.2727)
    db.session.add(new_brand_2)
    db.session.commit()

    new_brand_3 = Brand(product_id="P432234", brand_name="Lawless", display_name="Woke Up Like This Flawless Finish Foundation",
                        target_url="www.sephora.com/product/woke-up-like-this-flawless-finish-foundation-P432234",
                        rating=3.9836)
    db.session.add(new_brand_3)
    db.session.commit()

    new_brand_4 = Brand(product_id="P427301", brand_name="NARS", display_name="Natural Radiant Longwear Foundation",
                        target_url="www.sephora.com/product/natural-radiant-longwear-foundation-P427301",
                        rating=3.6461)

    db.session.add(new_brand_4)
    db.session.commit()

    new_foundation = Foundation(sku_id=1925148, product_id="P87985432", foundation_hex_code="#F6D4C4",
                                foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925148",
                                shade_image_url="www.sephora.com/productimages/sku/s1925148+sw.jpg",
                                hero_image_url="https://www.sephora.com/productimages/sku/s1925148-main-Lhero.jpg")
    db.session.add(new_foundation)
    db.session.commit()

    new_foundation_2 = Foundation(sku_id=1925155, product_id="P87985432", foundation_hex_code="#F4D6B9",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925155",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925155+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925155-main-Lhero.jpg")
    db.session.add(new_foundation_2)
    db.session.commit()

    new_foundation_3 = Foundation(sku_id=1925163, product_id="P87985432", foundation_hex_code="#EFD1B3",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925163",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925163+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925163-main-Lhero.jpg")

    db.session.add(new_foundation_3)
    db.session.commit()

    new_foundation_4 = Foundation(sku_id=1925171, product_id="P87985432", foundation_hex_code="#E8D2BB",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925171",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925171+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925171-main-Lhero.jpg")
    db.session.add(new_foundation_4)
    db.session.commit()

    new_foundation_5 = Foundation(sku_id=1925189, product_id="P87985432", foundation_hex_code="#F2CCB2",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925189",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925189+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925189-main-Lhero.jpg")
    db.session.add(new_foundation_5)
    db.session.commit()

    new_foundation_6 = Foundation(sku_id=1925197, product_id="P87985432", foundation_hex_code="#EDC8B4",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925197",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925197+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925197-main-Lhero.jpg")
    db.session.add(new_foundation_6)
    db.session.commit()

    new_foundation_7 = Foundation(sku_id=11925205, product_id="P87985432", foundation_hex_code="#EECDB1",
                                  foundation_target_url="www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925205",
                                  shade_image_url="www.sephora.com/productimages/sku/s1925205+sw.jpg",
                                  hero_image_url="https://www.sephora.com/productimages/sku/s1925205-main-Lhero.jpg")
    db.session.add(new_foundation_7)
    db.session.commit()

    new_review = Review(user_id=1, product_id="P87985432", review_content="best brand ever ever")
    db.session.add(new_review)
    db.session.commit()

    new_recommendation = Recommendation(image_id=1, sku_id=1925148, user_id=1)
    db.session.add(new_recommendation)
    db.session.commit()

    new_recommendation_2 = Recommendation(image_id=1, sku_id=1925155, user_id=1)
    db.session.add(new_recommendation_2)
    db.session.commit()

    new_recommendation_3 = Recommendation(image_id=1, sku_id=1925163, user_id=1)
    db.session.add(new_recommendation_3)
    db.session.commit()

    new_recommendation_4 = Recommendation(image_id=1, sku_id=1925171, user_id=1)
    db.session.add(new_recommendation_4)
    db.session.commit()

    new_recommendation_5 = Recommendation(image_id=1, sku_id=1925189, user_id=1)
    db.session.add(new_recommendation_5)
    db.session.commit()

    new_recommendation_6 = Recommendation(image_id=1, sku_id=1925197, user_id=1)
    db.session.add(new_recommendation_6)
    db.session.commit()

    new_favorite = Favorite(sku_id=1925148, user_id=1)
    db.session.add(new_favorite)
    db.session.commit()


if __name__ == "__main__":
  example_data()
