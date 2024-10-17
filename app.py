from flask import Flask, session, request, flash, redirect, url_for, render_template, jsonify
from database import init_db  # Import the init_db function
import MySQLdb.cursors
from routes import register_routes
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/data')
def data():
    dashboard_data = {
        'Steps': [150, 200, 250, 300],
        'calories burned': [120, 180, 210, 280],
        'WaterInTake': {
            'labels': ['water intake', 'goal'],
            'values': [1000, 3000]
        }
    }
    return jsonify(dashboard_data)

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


@app.route('/')
def startpage():
    # Clear the session to log the user out
    session.clear()
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Assume user ID is stored in the session
    user_id = session.get('user_id')

    if not user_id:
        flash('You must be logged in to view the dashboard.', 'warning')
        return redirect(url_for('signin.signin'))  # Redirect to login page if not logged in

    mysql = app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Fetch the assigned trainer for the user
        cursor.execute('''
            SELECT t.trainerid, t.firstname, t.lastname, t.specialty
            FROM Trainer_User_Assignment tua
            JOIN trainers t ON tua.trainerid = t.trainerid
            WHERE tua.userid = %s
        ''', (user_id,))
        
        assigned_trainer = cursor.fetchone()

        # Fetch the assigned workouts for the user
        cursor.execute('''
            SELECT w.*
            FROM Trainer_User_Assignment tua
            JOIN workouts w ON tua.workoutid = w.id
            WHERE tua.userid = %s
        ''', (user_id,))
        
        assigned_workouts = cursor.fetchall()


    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
        return redirect(url_for('dashboard'))  # Redirect back to dashboard in case of error
    finally:
        cursor.close()

    return render_template(
        'mainpage.html',
        assigned_trainer=assigned_trainer,  # Pass assigned trainer to template
        assigned_workouts=assigned_workouts,  # Pass assigned workouts to template
    )
















if __name__ == '__main__':
    app.run(debug=True)