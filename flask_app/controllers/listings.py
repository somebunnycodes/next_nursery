from flask import request, redirect, render_template, session
from flask_app import app
from flask_app.models.brand import Brand
from flask_app.models.user import User
from flask_app.models.listing import BRAND_ID, DESCRIPTION, PRICE, TITLE, Listing 

@app.route('/home', methods=["GET"])
def show_home():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    listings = Listing.list_all_listings()

    return render_template("home.html", user=user, listings=listings)

@app.route('/listings', methods=["GET"])
def show_listings():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    listings = Listing.list_user_listings(user.id)

    return render_template("listings.html", user=user, listings=listings)

@app.route('/new_listing', methods=['GET'])
def new_listing():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])
    brands = Brand.list_all_brands()

    if not user:
        return redirect('/logout')

    # default data
    listing = {
        TITLE: "",
        BRAND_ID: 1,
        PRICE: 0,
        DESCRIPTION: "",
    }

    return render_template("new_listing.html", user=user, listing=listing, brands=brands)

@app.route('/new_listing', methods=['POST'])
def post_listing():
    if not Listing.validate_create_or_update(request.form):
        user = User.get_by_id(session['user_id'])
        return render_template('new_listing.html', user=user, listing=request.form)

    Listing.create_listing(request.form)
    return redirect('/dashboard')


