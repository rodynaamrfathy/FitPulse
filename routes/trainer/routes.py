from flask import current_app, request, redirect, session, url_for, flash, render_template, Blueprint
import MySQLdb

trainer_bp = Blueprint('trainer', __name__)

@trainer_bp.route('/trainer_homepage')
def trainer_homepage():
    # Ensure trainer is logged in
    if 'trainer_id' not in session:
        flash('You must be logged in as a trainer to view this page.', 'warning')
        return redirect(url_for('signin.signin'))  # Redirect to login page if not logged in

    trainer_id = session['trainer_id']

    # Fetch trainer's specialty and diet plans
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Get the trainer's specialty
        cursor.execute('SELECT specialty FROM trainers WHERE trainerid = %s', (trainer_id,))
        trainer = cursor.fetchone()

        # Fetch the diet plans created by this trainer
        cursor.execute('SELECT * FROM dietplans WHERE authorid = %s', (trainer_id,))
        diet_plans = cursor.fetchall()

        # Fetch user requests made to this trainer
        cursor.execute('''
            SELECT tua.AssignmentID, tua.StartDate, tua.EndDate, u.firstname, u.lastname, tua.request
            FROM Trainer_User_Assignment tua
            JOIN users u ON tua.userid = u.userid
            WHERE tua.trainerid = %s AND tua.request = TRUE
        ''', (trainer_id,))
        user_requests = cursor.fetchall()
        
        cursor.execute('SELECT * FROM workouts WHERE authorid = %s', (trainer_id,))
        workouts_data = []
        for workout in cursor.fetchall():
            workouts_data.append({
                'id': workout['id'],
                'workoutname': workout['workoutname'],
                'maingoal': workout['maingoal'],
                'traininglevel': workout['traininglevel'],
                'daysperweek': workout['daysperweek'],
                'timeperworkout': workout['timeperworkout'],
                'equipmentrequired': workout['equipmentrequired'],
                'targetgender': workout['targetgender'],
                'supps': workout['supps'],
                'image': workout['image'],
                'description': workout['description']
            })
        print(f"Workouts fetched: {workouts_data}")  # Debug print

                # Fetch the workouts associated with the trainer
        cursor.execute('SELECT * FROM workouts WHERE trainerid = %s', (trainer_id,))
        workout = []

        for workout in cursor.fetchall():
            workout.append({
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

    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
        return redirect(url_for('trainer.trainer_homepage'))
    finally:
        cursor.close()

    return render_template('trainer_Homepage.html', 
                           firstName=session['firstName'], 
                           specialty=trainer['specialty'], 
                           diet_plans=diet_plans,
                           user_requests=user_requests,
<<<<<<< HEAD
                           workouts = workouts_data)  # Pass user requests to the template
    
    
=======
                           workouts=workout)  # Pass user requests to the template
>>>>>>> 968dd898aa73edf43235fafcf9b1365ef032fe1a

@trainer_bp.route('/availabletrainers')
def availabletrainers():
    # Get the MySQL connection
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Fetch all approved trainers
        cursor.execute("""
            SELECT trainerid AS id, firstname, lastname, specialty, experienceyears, rating, bio, payrate 
            FROM trainers 
            WHERE is_approved = TRUE AND specialty='Online Fitness Trainer' 
        """)
        trainers = cursor.fetchall()
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
        trainers = []  # Fallback to an empty list
    finally:
        cursor.close()
    
    # Render the template and pass the list of trainers
    return render_template("online_trainers.html", trainers=trainers)

@trainer_bp.route('/request_trainer', methods=['POST'])
def request_trainer():
    # Get the trainer ID, start date, and end date from the form
    trainer_id = request.form.get('trainer_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    print("Trainer ID:", trainer_id)
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("User ID:", session.get('user_id'))

    # Add logic to handle trainer request (e.g., save to database, notify trainer, etc.)
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Insert the request into the Trainer_User_Assignment table
        cursor.execute('''
            INSERT INTO Trainer_User_Assignment (trainerid, StartDate, EndDate, userid) 
            VALUES (%s, %s, %s, %s)
        ''', (trainer_id, start_date, end_date, session['user_id'])) 

        mysql.connection.commit()
        flash('Trainer request submitted successfully for the specified date range!', 'success')
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        cursor.close()

    return redirect(url_for('trainer.availabletrainers'))


@trainer_bp.route('/handle_request', methods=['POST'])
def handle_request():
    assignment_id = request.form.get('assignment_id')
    action = request.form.get('action')

    print(f"Assignment ID: {assignment_id}, Action: {action}")  # Debugging

    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        if action == 'approve':
            print(f"Approving request with Assignment ID: {assignment_id}")
            cursor.execute('UPDATE Trainer_User_Assignment SET request = FALSE WHERE AssignmentID = %s', (assignment_id,))
            flash('Request approved successfully!', 'success')
        elif action == 'decline':
            print(f"Declining request with Assignment ID: {assignment_id}")
            cursor.execute('DELETE FROM Trainer_User_Assignment WHERE AssignmentID = %s', (assignment_id,))
            flash('Request declined and removed successfully.', 'success')

        mysql.connection.commit()
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        cursor.close()

    return redirect(url_for('trainer.trainer_homepage'))
