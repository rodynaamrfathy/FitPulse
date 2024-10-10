import MySQLdb
from flask import Blueprint, render_template, session, current_app

# Define Blueprint for profile management
profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
def profile():
    # Get the user ID from the session
    user_id = session.get('user_id')  # Change 'userid' to 'user_id'
    print(f"User ID from session: {user_id}")  # Debug print statement
    
    if user_id is None:
        return "User not logged in", 403  # Or redirect to a login page

    # Fetch the MySQL connection from Flask's current_app config
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Select everything from the 'users' and 'userprop' tables for the given user ID
    query = """
        SELECT users.*, userprop.* 
        FROM users 
        JOIN userprop ON users.userid = userprop.userid
        WHERE users.userid = %s
    """
    
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()  # Fetch a single record for the user
    
    

    cursor.close()  # Close the cursor
    
    print(f"Fetched user data: {user_data}")  # Debug print statement


    # Check if user_data is empty
    if user_data is None:
        return "User not found", 404  # Handle case where user does not exist

    # Pass the data to the profile template
    return render_template('profile.html', user_data=user_data)
