from flask_app import app

# For AWS Elastic Beanstalk
application = app

from flask_app.controllers import users, listings, carts

if __name__ == "__main__":
    application.run(debug=True)