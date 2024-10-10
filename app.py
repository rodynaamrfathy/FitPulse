from flask import Flask, session, request, flash, redirect, url_for, render_template
from database import init_db  # Import the init_db function
import MySQLdb.cursors
from routes import register_routes
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail


app = Flask(__name__)

# Set the upload folder path for product images
UPLOAD_PRODUCT_FOLDER = 'static/uploads/productsimg/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the upload directory exists, if not, create it
upload_product_folder = 'static/uploads/productsimg/'
if not os.path.exists(upload_product_folder):
    os.makedirs(upload_product_folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_PRODUCT_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database by calling the init_db function
mysql = init_db(app)

# Store mysql instance in the app config
app.config['mysql'] = mysql

# Register the routes
register_routes(app)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/')
def startpage():
    # Clear the session to log the user out
    session.clear()
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('mainpage.html')


@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/startheader')
def startheader():
    return render_template('startheader.html')



@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/workoutsCategory')
def workoutsCategory():
    return render_template('workoutsCategory.html')

@app.route('/workouts')
def workouts():
    return render_template('workouts.html')

@app.route('/workout')
def workout():
    return render_template('workout.html')


@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/benchpresscalculator')
def benchpresscalculator():
    return render_template('tools/benchpresscalculator.html')


@app.route('/bmrcalculator')
def bmrcalculator():
    return render_template('tools/bmrcalculator.html')


@app.route('/signup')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
