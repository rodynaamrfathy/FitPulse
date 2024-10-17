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
    user_id = session.get('user_id')

    if not user_id:
        flash('You must be logged in to view the dashboard.', 'warning')
        return redirect(url_for('signin'))  # Redirect to login page if not logged in

    mysql = app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Fetch the user's profile and health data
        cursor.execute('''
            SELECT u.firstname, u.lastname, u.email, u.phone, u.profilepic, 
                   p.weight, p.height, p.caloriesgoal, p.caloriescurrent, p.watergoal, p.watercurrent, 
                   p.protiengoal, p.protiencurrent, p.carbgoal, p.carbcurrent, p.stepsgoal, p.stepscurrent
            FROM users u
            JOIN userprop p ON u.userid = p.userid
            WHERE u.userid = %s
        ''', (user_id,))
        user_data = cursor.fetchone()

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
        user_data=user_data,  # Pass user data to template
        assigned_workouts=assigned_workouts  # Pass assigned workouts to template
    )


@app.route('/data')
def data():
    user_id = session.get('user_id')

    mysql = app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('''
        SELECT caloriesgoal, caloriescurrent, watergoal, watercurrent, 
               protiengoal, protiencurrent, carbgoal, carbcurrent, stepsgoal, stepscurrent
        FROM userprop WHERE userid = %s
    ''', (user_id,))
    
    user_goals = cursor.fetchone()
    cursor.close()

    dashboard_data = {
        'Steps': [user_goals['stepscurrent'], user_goals['stepsgoal']],
        'calories burned': [user_goals['caloriescurrent'], user_goals['caloriesgoal']],
        'WaterInTake': {
            'labels': ['water intake', 'goal'],
            'values': [user_goals['watercurrent'], user_goals['watergoal']]
        }
    }

    return jsonify(dashboard_data)


@app.route('/update_water', methods=['POST'])
def update_water():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    water_amount = data['amount']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        UPDATE userprop SET watercurrent = watercurrent + %s WHERE userid = %s
    ''', (water_amount, user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True})

@app.route('/update_calories', methods=['POST'])
def update_calories():
    user_id = session.get('user_id')
    new_calories = request.form['calories']
    print("Received calories:", new_calories)  # Debugging line

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        UPDATE userprop SET caloriescurrent = %s WHERE userid = %s
    ''', (new_calories, user_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))

@app.route('/update_carbs', methods=['POST'])
def update_carbs():
    user_id = session.get('user_id')
    new_carbs = request.form['carbs']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        UPDATE userprop SET carbcurrent = %s WHERE userid = %s
    ''', (new_carbs, user_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))

@app.route('/update_protein', methods=['POST'])
def update_protein():
    user_id = session.get('user_id')
    new_protein = request.form['protein']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        UPDATE userprop SET protiencurrent = %s WHERE userid = %s
    ''', (new_protein, user_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)