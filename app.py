from flask import Flask, session, request, flash, redirect, url_for, render_template
from database import init_db  # Import the init_db function
import MySQLdb.cursors
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Set the upload folder path for product images
UPLOAD_PRODUCT_FOLDER = 'static/uploads/productsimg/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the upload directory exists, if not, create it
upload_product_folder = 'static/uploads/productsimg/'
if not os.path.exists(upload_product_folder):
    os.makedirs(upload_product_folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_PRODUCT_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database by calling the init_db function
mysql = init_db(app)

# Store mysql instance in the app config
app.config['mysql'] = mysql

# Register the routes

@app.route('/')
def startpage():
    # Clear the session to log the user out
    session.clear()
    return render_template('index.html')

@app.route('/startheader')
def startheader():
    return render_template('startheader.html')

if __name__ == '__main__':
    app.run(debug=True)
