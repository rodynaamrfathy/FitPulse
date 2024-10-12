import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app


# Define Blueprint for exercises management
workouts_bp = Blueprint('workoutscontroller', __name__)

@workouts_bp.route('/workoutplan')
def workoutplan():
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']  
    cursor = mysql.connection.cursor()

    # Execute query to retrieve workouts
    cursor.execute("SELECT * FROM workouts")
    workouts_data = []

    # Fetch all workouts and append to workouts_data list
    for workout in cursor.fetchall():
        workouts_data.append({
            'id': workout[0],  # Assuming the first column is 'id'
            'workoutname': workout[1],  # Assuming the second column is 'workoutname'
            'maingoal': workout[2],  # Adjust index according to your table structure
            'traininglevel': workout[3],
            'daysperweek': workout[4],
            'timeperworkout': workout[5],
            'equipmentrequired': workout[6],
            'targetgender': workout[7],
            'supps': workout[8],
            'image': workout[9],
            'description': workout[10]
        })

    # Close the cursor
    cursor.close()

    # Render the template and pass workouts_data to it
    return render_template('workoutplan.html', workouts=workouts_data)



# Route to handle form submission and add a new workout
@workouts_bp.route('/add_workout', methods=['POST'])
def add_workout():
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Collect form data
    workoutname = request.form['workoutname']
    maingoal = request.form['maingoal']
    traininglevel = request.form['traininglevel']
    daysperweek = request.form['daysperweek']
    timeperworkout = request.form['timeperworkout']
    equipmentrequired = request.form['equipmentrequired']
    targetgender = request.form['targetgender']
    recommendersupps = request.form['recommendersupps']
    description = request.form['description']
    
    # Handle image upload
    image = request.files['image']
    image_filename = image.filename if image else None
    if image :
        # Secure the filename and save the image to the 'static/uploads/workout_images' folder
       image.save(f"static/uploads/workouts/{image_filename}")

    try:
        # Insert the collected data into the database
        cursor.execute("""
            INSERT INTO workouts (workoutname, maingoal, traininglevel, daysperweek, timeperworkout, 
                                  equipmentrequired, targetgender, supps, image, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (workoutname, maingoal, traininglevel, daysperweek, timeperworkout, equipmentrequired, 
              targetgender, recommendersupps, image_filename, description))
        
        # Commit the changes to the database
        mysql.connection.commit()

        flash("Workout plan added successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        mysql.connection.rollback()
    finally:
        # Close the cursor
        cursor.close()

    # Redirect back to the workout plan page
    return redirect(url_for('workoutscontroller.workoutplan'))


@workouts_bp.route('/delete_workout/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']  
    cursor = mysql.connection.cursor()

    # Execute the delete query
    cursor.execute("DELETE FROM workouts WHERE id = %s", (workout_id,))
    
    # Commit the changes
    mysql.connection.commit()
    cursor.close()

    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('workoutscontroller.workoutplan'))


@workouts_bp.route('/edit_workout/<int:workout_id>', methods=['GET'])
def edit_workout(workout_id):
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Fetch the workout data for the specified ID
    cursor.execute("SELECT * FROM workouts WHERE id = %s", (workout_id,))
    workout = cursor.fetchone()

    # Check if workout exists
    if not workout:
        flash('Workout not found!', 'danger')
        return redirect(url_for('workoutscontroller.workoutplan'))

    # Prepare workout data to send to the template
    workout_data = {
        'id': workout[0],
        'workoutname': workout[1],
        'maingoal': workout[2],
        'traininglevel': workout[3],
        'daysperweek': workout[4],
        'timeperworkout': workout[5],
        'equipmentrequired': workout[6],
        'targetgender': workout[7],
        'supps': workout[8],
        'image': workout[9],
        'description': workout[10]
    }

    # Close the cursor
    cursor.close()

    # Render the edit template with the workout data
    return render_template('editworkout.html', workout=workout_data)




@workouts_bp.route('/workouts')
def workouts():
    
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']  
    cursor = mysql.connection.cursor()

    # Execute query to retrieve workouts
    cursor.execute("SELECT * FROM workouts")
    workouts_data = []

    # Fetch all workouts and append to workouts_data list
    for workout in cursor.fetchall():
        workouts_data.append({
            'id': workout[0],  # Assuming the first column is 'id'
            'workoutname': workout[1],  # Assuming the second column is 'workoutname'
            'maingoal': workout[2],  # Adjust index according to your table structure
            'traininglevel': workout[3],
            'daysperweek': workout[4],
            'timeperworkout': workout[5],
            'equipmentrequired': workout[6],
            'targetgender': workout[7],
            'supps': workout[8],
            'image': workout[9],
            'description': workout[10]
        })

    # Close the cursor
    cursor.close()
    return render_template('workouts.html', workouts=workouts_data)