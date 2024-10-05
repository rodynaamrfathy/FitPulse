import pymysql
from flask_mysqldb import MySQL


def init_db(app):
    app.config['MYSQL_HOST'] = 'mysql-152861f4-khbayoumi-c1ab.c.aivencloud.com'
    app.config['MYSQL_PORT'] = 17157
    app.config['MYSQL_USER'] = 'mokhaled'
    app.config['MYSQL_PASSWORD'] = 'AVNS_Qhzik288HFHRuL-8Edd'
    app.config['MYSQL_DB'] = 'defaultdb'
    app.config['MYSQL_AUTH_PLUGIN'] = 'caching_sha2_password'  # If you're using the new plugin

    # Initialize MySQL
    mysql = MySQL(app)
    return mysql