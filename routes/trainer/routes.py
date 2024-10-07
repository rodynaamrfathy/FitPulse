from flask import current_app, request, redirect, session, url_for, flash, render_template, Blueprint
from werkzeug.utils import secure_filename
import os
import MySQLdb

trainer_bp = Blueprint('trainer', __name__)


@trainer_bp.route('/trainer_homepage')
def trainer_homepage():
    # Assuming trainer's information is stored in the session
    trainer_id = session.get('trainer_id')
    
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT specialty FROM trainers WHERE trainerid = %s', (trainer_id,))
    trainer = cursor.fetchone()
    cursor.close()

    return render_template('trainer_Homepage.html', firstName=session['firstName'], specialty=trainer['specialty'])
