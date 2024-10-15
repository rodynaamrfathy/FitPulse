import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app,session

# Define Blueprint for recipes management
calender_bp = Blueprint('calendercontroller', __name__)



@calender_bp.route('/calender')
def calender():
    return render_template('calender.html')