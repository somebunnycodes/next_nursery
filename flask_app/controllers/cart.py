from flask import request, redirect, render_template, session
from flask_app import app
from flask_app.models.cart import Cart
from flask_app.models.user import User
from flask_app.models.listing import BRAND_ID, DESCRIPTION, ID, IMAGE_ID, PRICE, SELLER_ID, TITLE, Listing 

@app.route('/cart', methods=["GET"])
def show_cart():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    listings = Cart.list_listings_in_cart(user.id)
    print(listings)

    return render_template("cart.html", user=user, listings=listings)


@app.route('/cart/<listing_id>/add', methods=["GET"])
def add_listing(listing_id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    Cart.add_listing_to_cart(user.id, listing_id)

    return redirect("/cart")

@app.route('/cart/<listing_id>/remove', methods=["GET"])
def remove_listing(listing_id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    Cart.remove_listing_from_cart(user.id, listing_id)

    return redirect("/cart")

