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

        # Query the database to check if the email exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Check if the provided password matches the hashed password in the database
            if bcrypt.check_password_hash(user['passwordhash'], password):  # Use bcrypt to verify
                # If password matches, store user data in session
                session['loggedin'] = True
                session['userid'] = user['userid']  # Use 'userid' as per your schema
                session['email'] = user['email']
                session['firstName'] = user['firstname']

                flash('Logged in successfully!', 'success')
                return render_template('mainpage.html')
            else:
                flash('Incorrect email or password. Please try again.', 'danger')
        else:
            flash('Incorrect email or password. Please try again.', 'danger')

        return redirect(url_for('signin.signin'))

    return render_template('signin.html')
