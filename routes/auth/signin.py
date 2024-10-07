from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
import MySQLdb.cursors
from flask_bcrypt import Bcrypt  # Import Bcrypt

signin_bp = Blueprint('signin', __name__)

# Create an instance of Bcrypt (ensure this is consistent across your app)
bcrypt = Bcrypt()

@signin_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check the 'users' table first
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            # Check if the provided password matches the hashed password for users
            if bcrypt.check_password_hash(user['passwordhash'], password):
                # If password matches, store user data in session
                session['loggedin'] = True
                session['user_id'] = user['userid']  # Standardize session keys
                session['email'] = user['email']
                session['firstName'] = user['firstname']

                flash('Logged in successfully!', 'success')
                cursor.close()
                return redirect(url_for('dashboard'))  # Redirect to the mainpage

        # If user not found, check the 'trainers' table
        cursor.execute('SELECT * FROM trainers WHERE email = %s', (email,))
        trainer = cursor.fetchone()

        if trainer:
            # Check if the provided password matches the plaintext password for trainers
            if trainer['passwordhash'] == password:  # Direct plaintext comparison
                # If password matches, store trainer data in session
                session['loggedin'] = True
                session['trainer_id'] = trainer['trainerid']  # Use consistent session key
                session['email'] = trainer['email']
                session['firstName'] = trainer['firstname']

                flash('Logged in successfully as trainer!', 'success')
                cursor.close()
                return redirect(url_for('trainer.trainer_homepage'))  # Redirect to trainer homepage
            else:
                flash('Incorrect password for trainer. Please try again.', 'danger')
        else:
            flash('Account not found. Please try again or register.', 'info')

        cursor.close()
        return redirect(url_for('signin.signin'))

    return render_template('signin.html')