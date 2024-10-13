import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app

# Define Blueprint for exercises management
workoutdays_bp = Blueprint('workoutdayscontroller', __name__)

@workoutdays_bp.route('/editworkout/<int:workout_id>')
def editworkout(workout_id):
    mysql = current_app.config['mysql']  
    cursor = mysql.connection.cursor()
    
    days_data = []  # Initialize an empty list to hold day data

    try:
        # Fetch days associated with the specific WorkoutID
        cursor.execute("SELECT * FROM WorkoutDay WHERE WorkoutID = %s", (workout_id,))
        for day in cursor.fetchall():
            days_data.append({
                'DayID': day[0],  # Assuming the first column is 'DayID'
                'WorkoutID': day[1],  # Assuming the second column is 'WorkoutID'
                'DayNumber': day[2],  # Assuming the third column is 'DayNumber'
                'name': day[3]  # Assuming the fourth column is 'name'
            })

        # Print the days_data to the console for debugging
        print("Fetched Days Data:", days_data)  # This will print the list of days

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()  # Always close your cursor to avoid leaks

    return render_template('editworkout.html', days=days_data, workout_id=workout_id)

@workoutdays_bp.route('/add_day/<int:workout_id>', methods=['POST'])
def add_day(workout_id):
    # Get MySQL connection from app config
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Collect form data
    dayname = request.form['dayname']
    dayweek = request.form['dayweek']

    try:
        # Insert the collected data into the WorkoutDay table
        cursor.execute("""
            INSERT INTO WorkoutDay (WorkoutID, DayNumber, name)
            VALUES (%s, %s, %s)
        """, (workout_id, dayweek, dayname))
        
        # Commit the changes to the database
        mysql.connection.commit()

        flash("Day added successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        mysql.connection.rollback()
    finally:
        # Close the cursor
        cursor.close()

    # Redirect back to the edit workout page (or another page as needed)
    return redirect(url_for('workoutdayscontroller.editworkout', workout_id=workout_id))