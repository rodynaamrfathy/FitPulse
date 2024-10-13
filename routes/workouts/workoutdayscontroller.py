import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app


# Define Blueprint for exercises management
workoutdays_bp = Blueprint('workoutdayscontroller', __name__)
@workoutdays_bp.route('/editworkout')
def editworkout():
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    try:
        cursor.execute("SELECT DayID, name FROM WorkoutDay")
        days = cursor.fetchall()

        # Log the results of the SQL query
        if not days:
            print("No days found in the WorkoutDay table.")
        else:
            print(f"Fetched days: {days}")

        days = [{'DayID': day[0], 'name': day[1]} for day in days]

    except Exception as e:
        flash(f"Error fetching workout days: {str(e)}", "danger")
        days = []  # Ensure days is defined even on error
    finally:
        cursor.close()

    return render_template('editworkout.html', days=days)



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
    return redirect(url_for('workoutscontroller.edit_workout' , workout_id=workout_id))



