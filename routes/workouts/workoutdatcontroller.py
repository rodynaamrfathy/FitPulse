import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app


# Define Blueprint for exercises management
workouts_bp = Blueprint('workoutscontroller', __name__)

