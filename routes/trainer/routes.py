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
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", 'danger')
        return redirect(url_for('trainer.trainer_homepage'))
    finally:
        cursor.close()

    return render_template('trainer_Homepage.html', 
                           firstName=session['firstName'], 
                           specialty=trainer['specialty'], 
                           diet_plans=diet_plans)

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
            WHERE is_approved = TRUE
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
