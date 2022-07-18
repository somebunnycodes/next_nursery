import uuid
from flask import request, redirect, render_template, session
from flask_app import app
from flask_app.models.brand import Brand
from flask_app.models.image import Image
from flask_app.models.user import User
from flask_app.models.listing import BRAND_ID, DESCRIPTION, ID, IMAGE_ID, PRICE, SELLER_ID, TITLE, Listing 

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
def home():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    listings = Listing.list_user_listings(user.id)

    return render_template("listings.html", user=user, listings=listings)

@app.route('/brands/<brand_id>/listings', methods=["GET"])
def brand_listings(brand_id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    if not user:
        return redirect('/logout')

    brand = Brand.get_by_id(brand_id)

    listings = Listing.list_brand_listings(brand_id)

    return render_template("brand_listings.html", user=user, listings=listings, brand=brand)

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
    user = User.get_by_id(session['user_id'])

    if not Listing.validate_create_or_update(request.form):
        brands = Brand.list_all_brands()
        return render_template('new_listing.html', user=user, brands=brands, listing=request.form)

    image_file_name=""
    if request.files["image"]:
        file_to_upload = request.files["image"]
        if file_to_upload: 
            image_id = str(uuid.uuid4()) 
            image_file_name = image_id + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()
            Image.upload_image_to_s3(file_to_upload, image_file_name)

    data = {
        TITLE: request.form[TITLE],
        BRAND_ID: request.form[BRAND_ID],
        PRICE: request.form[PRICE],
        IMAGE_ID: image_file_name,
        DESCRIPTION: request.form[DESCRIPTION],
        SELLER_ID: user.id
    }

    Listing.create_listing(data)
    return redirect('/listings')

@app.route('/listings/<listing_id>/edit', methods=['GET'])
def edit_listing(listing_id):
    listing=Listing.get_by_id(listing_id)
    brands = Brand.list_all_brands()
    user = User.get_by_id(session["user_id"])
    return render_template('edit_listing.html', user=user, brands=brands, listing=listing)

@app.route('/listings/<listing_id>', methods=['GET'])
def view_listing(listing_id):
    listing=Listing.get_by_id(listing_id)
    brands = Brand.list_all_brands()
    user = User.get_by_id(session["user_id"])
    return render_template('view_listing.html', user=user, brands=brands, listing=listing)

@app.route('/listings/<listing_id>', methods=['POST'])
def update_listing(listing_id):
    listing=Listing.get_by_id(listing_id)
    brands = Brand.list_all_brands()
    user = User.get_by_id(session["user_id"])
    if not Listing.validate_create_or_update(request.form):
        brands = Brand.list_all_brands()
        return render_template('edit_listing.html', user=user, brands=brands, listing=request.form)

    image_file_name=request.form['image_id']
    if request.files["image"]:
        file_to_upload = request.files["image"]
        if file_to_upload: 
            image_id = str(uuid.uuid4()) 
            image_file_name = image_id + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()
            Image.upload_image_to_s3(file_to_upload, image_file_name)

    data = {
        ID: listing_id,
        TITLE: request.form[TITLE],
        BRAND_ID: request.form[BRAND_ID],
        PRICE: request.form[PRICE],
        IMAGE_ID: image_file_name,
        DESCRIPTION: request.form[DESCRIPTION],
        SELLER_ID: user.id
    }
    Listing.update_listing(data)
    return redirect('/listings')

@app.route('/listings/<listing_id>/delete', methods=['GET'])
def delete_listing(listing_id):
    Listing.delete_listing(listing_id)
    return redirect('/listings')


