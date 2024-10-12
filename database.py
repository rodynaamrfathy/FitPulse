import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_db(app):
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_AUTH_PLUGIN'] = 'caching_sha2_password'  # If you're using the new plugin

    # Initialize MySQL
    mysql = MySQL(app)
    return mysql