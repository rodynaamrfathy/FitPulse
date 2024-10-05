from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_bcrypt import Bcrypt

signup_bp = Blueprint('signup', __name__)

# Create an instance of Bcrypt, assuming it's initialized somewhere globally in your app
bcrypt = Bcrypt()

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        date_of_birth = request.form['dateOfBirth']

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Get MySQL instance from the app context
        mysql = current_app.config['mysql']

        cursor = mysql.connection.cursor() 
        cursor.execute('INSERT INTO users (firstname, lastname, email, passwordhash, gender, dateofbirth) VALUES (%s, %s, %s, %s, %s, %s)',
                       (first_name, last_name, email, hashed_password, gender, date_of_birth))
        mysql.connection.commit()

        # Fetch the newly created user's id
        user_id = cursor.lastrowid

        # Close the cursor
        cursor.close()

        # Store user information in the session
        session['loggedin'] = True
        session['id'] = user_id
        session['email'] = email
        session['firstName'] = first_name

        flash('Registration successful!', 'success')
        return redirect(url_for('startpage'))

    return render_template('register.html')
