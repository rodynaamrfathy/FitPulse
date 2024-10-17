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
        return redirect(url_for('signin.signin'))  # Redirect to login page if not logged in

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
        'Steps': {
            'goal': user_goals['stepsgoal'],
            'current': user_goals['stepscurrent']
        },
        'WaterInTake': {
            'goal': user_goals['watergoal'],
            'current': user_goals['watercurrent']
        },
        'Calories': {
            'goal': user_goals['caloriesgoal'],
            'current': user_goals['caloriescurrent']
        },
        'Protein': {
            'goal': user_goals['protiengoal'],
            'current': user_goals['protiencurrent']
        },
        'Carbs': {
            'goal': user_goals['carbgoal'],
            'current': user_goals['carbcurrent']
        }
    }

    return jsonify(dashboard_data)



@app.route('/update_water', methods=['POST'])
def update_water():
    user_id = session.get('user_id')
    if not user_id:
        print("No user ID found")
        return jsonify({"error": "Unauthorized"}), 403
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch the current water amount
    cursor.execute('SELECT watercurrent FROM userprop WHERE userid = %s', (user_id,))
    result = cursor.fetchone()
    
    if result:
        current_water = result['watercurrent']  # Fetch the value from the dictionary
        if current_water is None:
            current_water = 0.0  # Initialize to 0 if no value
        else:
            current_water = float(current_water)  # Ensure it's a float for arithmetic operations
        print(f"Current water amount for user {user_id}: {current_water}")
    else:
        print(f"No user found with id {user_id}")
        return jsonify({"error": "User not found"}), 404

    # Get water amount from the form, and convert it to a float
    water_amount = request.form.get('water_amount')
    try:
        water_amount = float(water_amount)
    except (ValueError, TypeError):
        print(f"Invalid water amount: {water_amount}")
        return jsonify({"error": "Invalid water amount"}), 400
    
    # Add the new water amount to the current water amount
    updated_water = current_water + water_amount
    print(f"Updated water amount: {updated_water}")

    # Update the database with the new value
    cursor.execute('''UPDATE userprop SET watercurrent = %s WHERE userid = %s''', (updated_water, user_id))
    mysql.connection.commit()
    cursor.close()

    print(f"Water amount {water_amount} added successfully for user {user_id}")

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
    print("Received protien:", new_protein)  # Debugging line

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        UPDATE userprop SET protiencurrent = %s WHERE userid = %s
    ''', (new_protein, user_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)