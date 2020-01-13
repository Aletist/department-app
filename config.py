import pymysql
from flask import Config

class ServiceConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/dept_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ClientConfig(Config):
    WTF_CSRF_ENABLED = False

class DatabaseConfig():
    databaseServerIP = "127.0.0.1"  # IP address of the MySQL database server
    databaseUserName = "root"  # User name of the database server
    databaseUserPassword = ""  # Password for the database user
    newDatabaseName = "dept_db"  # Name of the database that is to be created
    charSet = "utf8mb4"  # Character set
    cursorType = pymysql.cursors.DictCursor
    connectionInstance = pymysql.connect(host=databaseServerIP, user=databaseUserName,
                                         password=databaseUserPassword,
                                         charset=charSet, cursorclass=cursorType)

class DeployConfig():
    project_dir='/'
    environment='PATH=/home/travis/virtualenv/bin'
    user = 'travis'
    dev = True


class ApiConfig():
    conf_location = '/etc/systemd/system/www-department-app.service'
    exec_command = '--workers 1 --bind'
    host = 'api.department-app'
    port = '5555'
    app = 'service.webservice:app'
    app_description = 'Gunicorn instance to serve department-app RESTful api'
    nginx = '/etc/nginx/sites-available/api-department-app'
    nginx_port = 80


class WebConfig():
    conf_location = '/etc/systemd/system/www-department-app.service'
    exec_command = '--workers 1 --bind'
    host = 'www.department-app'
    port = '5444'
    app = 'views.client:app'
    app_description = 'Gunicorn instance to serve department-app web client'
    nginx = '/etc/nginx/sites-available/www-department-app'
    nginx_port = 80



