from datetime import datetime
from flask import current_app, request, redirect, session, url_for, flash, render_template, Blueprint
from werkzeug.utils import secure_filename
import os
import MySQLdb

dietplans_bp = Blueprint('dietplans', __name__)

@dietplans_bp.route('/dietplans')
def dietplans():
    return render_template('dietplans.html')

@dietplans_bp.route('/dietplan')
def dietplan():
    return render_template('dietplan.html')

UPLOAD_FOLDER = 'static/uploads/dietplans'  # Define your upload folder path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed image types

def allowed_file(filename):
    """Check if the uploaded file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dietplans_bp.route('/dietplan', methods=['POST'])
def add_diet_plan():
    # Ensure the trainer is logged in
    if 'trainer_id' not in session:
        flash('You must be logged in as a trainer to add a diet plan.', 'warning')
        return redirect(url_for('signin.signin'))  # Redirect to login if not logged in

    # Get form data
    diet_name = request.form['diet_name']
    description = request.form['description']
    core_principles = request.form['core_principles']
    timing_frequency = request.form['timing_frequency']
    best_suited_for = request.form['best_suited_for']
    easy_to_follow = request.form['easy_to_follow']
    studies = request.form['studies']
    image = request.files['image']

    # Get the current logged-in trainer's ID from session (assuming it's stored in session)
    author_id = session['trainer_id']  # Ensure trainer's ID is in the session

    # Validate and save the image
    if image and allowed_file(image.filename):
        dietplans = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, dietplans))
        image_path = os.path.join(UPLOAD_FOLDER, dietplans)
    else:
        image_path = None  # If no image is uploaded

    # Insert the diet plan data into the database
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO dietplans (authorid, dietname, description, image, publishdate, coreprinciples, timingfrequency, bestsuitedfor, easytofollow, studies)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (author_id, diet_name, description, image_path, datetime.now(), core_principles, timing_frequency, best_suited_for, easy_to_follow, studies))
    
    mysql.connection.commit()
    cursor.close()

    flash('Diet plan added successfully!', 'success')
    return redirect(url_for('trainer.trainer_homepage'))  # Redirect back to trainer homepage
