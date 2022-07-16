from flask import flash, request, redirect, render_template, session
from flask_bcrypt import Bcrypt        
from flask_app import app
from flask_app.models.user import EMAIL, FIRST_NAME, LAST_NAME, USER_NAME, PASS_HASH, USER_NAME, User

bcrypt = Bcrypt(app)

@app.route('/', methods=["GET"])
def get_register():
    if 'user_id' in session:
        return redirect('/home')
    
    return render_template("registration.html", data={})

@app.route('/login', methods=["GET"])
def get_login():
    if 'user_id' in session:
        return redirect('/home')
    
    return render_template("login.html", data={})

@app.route('/register', methods=["POST"])
def post_register():
    if not User.validate_registration(request.form):
        return render_template("registration.html", data=request.form)

    pass_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        FIRST_NAME: request.form[FIRST_NAME],
        LAST_NAME: request.form[LAST_NAME],
        USER_NAME: request.form[USER_NAME],
        EMAIL: request.form[EMAIL],
        PASS_HASH: pass_hash
    }
    id = User.create(data)
    session['user_id'] = id
    return redirect(f'/home')

@app.route('/login', methods=["POST"])
def post_login():
    # Check whether the email provided is associated with a user in the database
    user_name = request.form[USER_NAME]
    user = User.get_by_user_name(user_name)
    if not user:
        flash('User name not found', 'login')
        return render_template("login.html", data=request.form)

    # If it is, check whether the password matches what's saved in the database
    if not bcrypt.check_password_hash(user.pass_hash, request.form['password']): 
        flash('Invalid password', 'login')
        return redirect('/login')
    
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')