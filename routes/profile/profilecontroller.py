import os
import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app,session

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
    
     # Select orders related to the user
    order_query = """
        SELECT orderid, orderdate, orderstatus, totalamount
        FROM orders
        WHERE userid = %s
        ORDER BY orderdate DESC
    """

    cursor.execute(order_query, (user_id,))
    orders = cursor.fetchall()  # Fetch all the orders for the user


    cursor.close()  # Close the cursor
    
    print(f"Fetched user data: {user_data}")  # Debug print statement


    # Check if user_data is empty
    if user_data is None:
        return "User not found", 404  # Handle case where user does not exist

    # Pass the data to the profile template
    return render_template('profile.html', user_data=user_data , orders=orders)  # Adjust this route as needed  




@profile_bp.route('/profile/update', methods=['POST'])
def update_user_profile():
    user_id = session.get('user_id')  # Ensure the user is logged in

    if user_id is None:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))  # Redirect to the login page

    # Fetch the MySQL connection from Flask's current_app config
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Fetch existing user data from the database
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    existing_user = cursor.fetchone()
    
    cursor.execute("SELECT * FROM userprop WHERE userid = %s", (user_id,))
    existing_properties = cursor.fetchone()

    # Default values from the existing user data
    first_name = request.form.get('firstName', existing_user[1]).strip()  # Assuming index 1 is firstname
    last_name = request.form.get('lastName', existing_user[2]).strip()    # Assuming index 2 is lastname
    address = request.form.get('address', existing_user[3]).strip()      # Assuming index 3 is address
    phone = request.form.get('phone', existing_user[4]).strip()          # Assuming index 4 is phone
    email = request.form.get('email', existing_user[5]).strip()          # Assuming index 5 is email
    gender = request.form.get('gender', existing_user[6]).strip()        # Assuming index 6 is gender
    profile_pic = request.files.get('profilepic')
    

    # Collect user properties
    weight = request.form.get('weight', existing_properties[1])                 # Assuming index 1 is weight
    height = request.form.get('height', existing_properties[2])                  # Assuming index 2 is height
    goalweight = request.form.get('goalweight', existing_properties[3])          # Assuming index 3 is goalweight
    fitnessgoal = request.form.get('fitnessgoal', existing_properties[4])        # Assuming index 4 is fitnessgoal
    trainingExperience = request.form.get('trainingexperience', existing_properties[5])  # Assuming index 5 is trainingexperience
    activityLevel = request.form.get('activityLevel', existing_properties[6])    # Assuming index 6 is activitylevel
    bodyFatPercentage = request.form.get('bodyfat', existing_properties[7])     # Assuming index 7 is bodyfat
    muscleMass = request.form.get('musclemass', existing_properties[8])         # Assuming index 8 is musclemass
    waistSize = request.form.get('waistsize', existing_properties[9])            # Assuming index 9 is waistsize
    hipSize = request.form.get('hipsize', existing_properties[10])                # Assuming index 10 is hipsize
    chestSize = request.form.get('chestsize', existing_properties[11])           # Assuming index 11 is chestsize
    armSize = request.form.get('armsize', existing_properties[12])             # Assuming index 12 is armsize
    thighSize = request.form.get('thighsize', existing_properties[13])          # Assuming index 13 is thighsize
    restingHeartRate = request.form.get('restingheartrate', existing_properties[14])  # Assuming index 14 is restingheartrate
    bloodPressure = request.form.get('bloodpressure', existing_properties[15])   # Assuming index 15 is bloodpressure
    vo2Max = request.form.get('vo2max', existing_properties[16])               # Assuming index 16 is vo2max
    injuries = request.form.get('injuries', existing_properties[17])              # Assuming index 17 is injuries
    chronicConditions = request.form.get('chronicConditions', existing_properties[18]) # Assuming index 18 is chronicconditions

    # Initialize profile_pic_filename as None
    profile_pic_filename = None

    # Check if the user uploaded a profile picture
    if profile_pic:
        if not profile_pic.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            flash('Only image files are allowed for the profile picture.', 'danger')
            return redirect(url_for('profile_bp.profile'))

        # If a new profile picture is uploaded, save it and update filename
        profile_pic_filename = profile_pic.filename
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/userspp')
        os.makedirs(upload_folder, exist_ok=True)
        profile_pic_path = os.path.join(upload_folder, profile_pic_filename)
        profile_pic.save(profile_pic_path)
    else:
        # If no new profile picture is uploaded, use the existing filename
        profile_pic_filename = existing_user[7]  # Assuming index 7 is profilepic

    # Update the user's profile in the 'users' table
    update_user_query = """
        UPDATE users 
        SET firstname = %s, lastname = %s, address = %s, phone = %s, email = %s, gender = %s, profilepic = %s
        WHERE userid = %s
    """

    # Prepare user properties update query
    update_user_properties_query = """
        UPDATE userprop 
        SET weight = %s, height = %s, goalweight = %s, fitnessgoal = %s,
            trainingexperience = %s, activitylevel = %s, bodyfatpercentage = %s,
            musclemass = %s, waistsize = %s, hipsize = %s,
            chestsize = %s, armsize = %s, thighsize = %s,
            restingheartrate = %s, bloodpressure = %s, vo2max = %s,
            injuries = %s, chronicconditions = %s
        WHERE userid = %s
    """

    try:
        # Update user info
        cursor.execute(update_user_query, (
            first_name, last_name, address, phone, email, gender, profile_pic_filename, user_id
        ))
       
        mysql.connection.commit()  # Commit changes to the database
        
        # Update user properties
        cursor.execute(update_user_properties_query, (
            weight, height, goalweight, fitnessgoal, trainingExperience, activityLevel,
            bodyFatPercentage, muscleMass, waistSize, hipSize, chestSize,
            armSize, thighSize, restingHeartRate, bloodPressure, vo2Max,
            injuries, chronicConditions, user_id
        ))

        mysql.connection.commit()  # Commit changes to the database

    except Exception as e:
        mysql.connection.rollback()  # Rollback on error
        print(f"Error updating profile: {str(e)}")
        flash('Error updating the profile in the database.', 'danger')

    cursor.close()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile_bp.profile'))  # Adjust this route as needed

