from flask import current_app, request, redirect, session, url_for, flash, render_template, Blueprint
from werkzeug.utils import secure_filename
import os
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

    # Get the trainer's specialty
    cursor.execute('SELECT specialty FROM trainers WHERE trainerid = %s', (trainer_id,))
    trainer = cursor.fetchone()

    # Fetch the diet plans created by this trainer
    cursor.execute('SELECT * FROM dietplans WHERE authorid = %s', (trainer_id,))
    diet_plans = cursor.fetchall()

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
    
    # Fetch all approved trainers
    cursor.execute("SELECT firstname, lastname, specialty, experienceyears, rating, bio, payrate FROM trainers WHERE is_approved = TRUE")
    trainers = cursor.fetchall()
    
    cursor.close()
    
    # Render the template and pass the list of trainers
    return render_template("online_trainers.html", trainers=trainers)

@trainer_bp.route('/request_trainer', methods=['POST'])
def request_trainer():
    # Get the trainer ID, start date, and end date from the form
    trainer_id = request.form.get('trainer_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Add logic to handle trainer request (e.g., save to database, notify trainer, etc.)
    # Here you can save the trainer request with the dates in a table
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # For example, you could insert this request into a `trainer_requests` table
    cursor.execute('''
        INSERT INTO assignmentID (trainer_id, start_date, end_date, user_id) 
        VALUES (%s, %s, %s, %s)
    ''', (trainer_id, start_date, end_date, session['user_id'])) 

    mysql.connection.commit()
    cursor.close()

    # Flash a success message and redirect back to the trainers list
    flash('Trainer request submitted successfully for the specified date range!', 'success')
    return redirect(url_for('trainer.availabletrainers'))