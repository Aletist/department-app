from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dept_db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Integer, nullable=True)
    department = db.Column(db.String(64), db.ForeignKey('department.name'), nullable=True)
    head_of = db.Column(db.String(64), db.ForeignKey('department.name'), nullable=True)
    birth_date = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=date.today())


class Department(db.Model):
    __tablename__ = 'department'
    name = db.Column(db.String(64), primary_key=True)


if __name__ == '__main__':
    manager.run()
