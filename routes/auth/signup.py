from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

signup_bp = Blueprint('signup',__name__)
# Create an instance of Bcrypt
bcrypt = Bcrypt()

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collecting all necessary data from the multi-step form
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        date_of_birth = request.form.get('dateOfBirth', '').strip()
        gender = request.form.get('gender', '').strip()

        # Optional data fields
        weight = request.form.get('weight', '').strip() or None
        height = request.form.get('height', '').strip() or None
        goal = request.form.get('goal', '').strip() or None
        fitnessgoal = request.form.get('fitnessgoal', '').strip() or None
        trainingExperience = request.form.get('trainingExperience', '').strip() or None
        activityLevel = request.form.get('activityLevel', '').strip() or None
        bodyFatPercentage = request.form.get('bodyFatPercentage', '').strip() or None
        muscleMass = request.form.get('muscleMass', '').strip() or None
        waistSize = request.form.get('waistSize', '').strip() or None
        hipSize = request.form.get('hipSize', '').strip() or None
        chestSize = request.form.get('chestSize', '').strip() or None
        armSize = request.form.get('armSize', '').strip() or None
        thighSize = request.form.get('thighSize', '').strip() or None
        restingHeartRate = request.form.get('restingHeartRate', '').strip() or None
        bloodPressure = request.form.get('bloodPressure', '').strip() or None
        vo2Max = request.form.get('vo2Max', '').strip() or None
        injuries = request.form.get('injuries', '').strip() or None
        chronicConditions = request.form.get('chronicConditions', '').strip() or None
        
        calories = request.form.get('caloriesgoal', '').strip() or None
        protein = request.form.get('protiengoal', '').strip() or None
        carb = request.form.get('carbgoal', '').strip() or None
        steps = request.form.get('stepsgoal', '').strip() or None
        water = request.form.get('watergoal', '').strip() or None

        # Email check
        mysql = current_app.config['mysql']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email address already exists. Please use a different email.', 'danger')
            cursor.close()
            return render_template('register.html')

        # Hash password and handle profile picture upload
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        profile_pic = request.files.get('profilepic')
        profile_pic_filename = None

        if profile_pic:
            if not profile_pic.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                flash('Only image files are allowed for the profile picture.', 'danger')
                cursor.close()
                return render_template('register.html')

            profile_pic_filename = profile_pic.filename
            upload_folder = os.path.join(current_app.root_path, 'static/uploads/userspp')
            os.makedirs(upload_folder, exist_ok=True)
            profile_pic_path = os.path.join(upload_folder, profile_pic_filename)
            profile_pic.save(profile_pic_path)

        # Insert mandatory user data
        try:
            cursor.execute(
                'INSERT INTO users (firstname, lastname, email, passwordhash, gender, dateofbirth, phone, profilepic, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (first_name, last_name, email, hashed_password, gender, date_of_birth, phone, profile_pic_filename, address)
            )
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            flash('Registration failed. Please try again.', 'danger')
            cursor.close()
            return render_template('register.html')

        user_id = cursor.lastrowid

        # Insert optional user properties (only if provided)
        cursor.execute(
            'INSERT INTO userprop (userid, weight, height, goalweight, fitnessgoal, trainingexperience, activitylevel, bodyfatpercentage, musclemass, waistsize, hipsize, chestsize, armsize, thighsize, restingheartrate, bloodpressure, vo2max, injuries, chronicconditions, caloriesgoal, protiengoal, carbgoal, stepsgoal, watergoal) VALUES (%s,%s,%s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (user_id, weight, height, goal, fitnessgoal, trainingExperience, activityLevel, bodyFatPercentage, muscleMass, waistSize, hipSize, chestSize, armSize, thighSize, restingHeartRate, bloodPressure, vo2Max, injuries, chronicConditions, calories, protein, carb, steps, water)
        )
        
        mysql.connection.commit()
        flash('Registration successful!', 'success')
        cursor.close()

        return redirect(url_for('startpage'))

    return render_template('register.html')