from flask import Flask, session, request, flash, redirect, url_for, render_template
from database import init_db  # Import the init_db function
import MySQLdb.cursors
from routes import register_routes
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os

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
    trainer = {
        'name': 'John Doe',
        'specialty': 'Strength Training',
        'experience': 10,  # in years
        'rating': 4.8
    }

    water_intake = 1500  # in milliliters
    total_water_goal = 3000  # in milliliters

    protein = 150  # in grams
    carbs = 200  # in grams
    calories = 2500  # in kcal

    exercises = [
        {'name': 'Squat', 'reps': 10, 'sets': 3},
        {'name': 'Deadlift', 'reps': 8, 'sets': 3},
        {'name': 'Bench Press', 'reps': 12, 'sets': 4}
    ]

    # Data for the charts
    chart_data = {
        'water_intake': water_intake,
        'total_water_goal': total_water_goal,
        'protein': protein,
        'carbs': carbs,
        'calories': calories
    }

    return render_template(
        'mainpage.html',
        trainer=trainer,
        chart_data=chart_data,
        exercises=exercises
    )

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/startheader')
def startheader():
    return render_template('startheader.html')



@app.route('/navbar')
def navbar():
    return render_template('navbar.html')



@app.route('/workoutsCategory')
def workoutsCategory():
    return render_template('workoutsCategory.html')


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

@app.route('/workoutplan')
def workoutplan():
    return render_template('workoutplan.html')




@app.route('/chartstest')
def chartstest():
    # Define your data
    water_intake = 80  # in milliliters
    total_water_goal = 100  # in milliliters

    # Data for the charts
    chart_data = {
        'water_intake': water_intake,
        'total_water_goal': total_water_goal,
    }

    return render_template('chartstest.html', chart_data=chart_data)




if __name__ == '__main__':
    app.run(debug=True)