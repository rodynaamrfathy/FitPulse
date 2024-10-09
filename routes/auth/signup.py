from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_bcrypt import Bcrypt
from datetime import datetime

signup_bp = Blueprint('signup', __name__)

# Create an instance of Bcrypt, assuming it's initialized somewhere globally in your app
bcrypt = Bcrypt()

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collecting all necessary data from the multi-step form
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        date_of_birth = request.form['dateOfBirth']
        weight = request.form['weight']  # New field from Step 2
        height = request.form['height']  # New field from Step 2
        goal = request.form['goal']  # New field from Step 3

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Get MySQL instance from the app context
        mysql = current_app.config['mysql']
        cursor = mysql.connection.cursor() 
        
        # Insert user data into the users table
        cursor.execute('INSERT INTO users (firstname, lastname, email, passwordhash, gender, dateofbirth, weight, height, fitness_goal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (first_name, last_name, email, hashed_password, gender, date_of_birth, weight, height, goal))
        mysql.connection.commit()

        # Fetch the newly created user's id
        user_id = cursor.lastrowid

        # Close the cursor
        cursor.close()

        # Calculate the age based on the date_of_birth
        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')  # Assuming date_of_birth is in 'YYYY-MM-DD' format
        age = (datetime.now() - birth_date).days // 365  # Calculate age in years

        # Store user information in the session
        session['loggedin'] = True
        session['id'] = user_id
        session['email'] = email
        session['firstName'] = first_name
        session['weight'] = weight
        session['height'] = height
        session['age'] = age
        session['fitness_goal'] = goal

        flash('Registration successful!', 'success')
        return redirect(url_for('startpage'))

    return render_template('register.html')