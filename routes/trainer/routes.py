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
    return render_template("online_trainers.html")