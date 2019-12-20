from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.models import Employee, Department

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dept_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    depts = [Department(name='IT'),
             Department(name='Sales'),
             Department(name='Research'),
             Department(name='PR')]

    for dept in depts:
        db.session.add(dept)
    db.session.commit()

    employees = [
        Employee(first_name='Siusan', last_name='Turner', head_of='Sales', salary=1340, birth_date=date(1995, 4, 7)),
        Employee(first_name='Andrew', last_name='Miles', department='IT', salary=1100, birth_date=date(1989, 1, 17)),
        Employee(first_name='Oleg', last_name='Sidorov', department='IT', salary=900, birth_date=date(1990, 7, 13)),
        Employee(first_name='Brian', last_name='Fox', department='Research', salary=900, birth_date=date(1990, 1, 6)),
        Employee(first_name='Steve', last_name='Johnson', birth_date=date(1999, 9, 9)),
        Employee(first_name='Martin', last_name='Black', birth_date=date(1988, 8, 18)),
        Employee(first_name='Alex', last_name='Jones', department='PR',
                 head_of='PR', salary=1400,birth_date=date(1975, 3, 17)),
        Employee(first_name='Michael', last_name='Pane', department='IT',
                 head_of='IT', salary=1200,birth_date=date(1980, 7, 25)),
        Employee(first_name='Jonathan', last_name='Miles', department='Research',
                 salary=1100, birth_date=date(1989, 9, 17)),
        Employee(first_name='Stefanie', last_name='Miller', department='Research',
                 salary=1300,birth_date=date(1990, 5, 12)),
        Employee(first_name='Taras', last_name='Prokopenko', department='Sales', salary=1000,
                 birth_date=date(1990, 4, 2))
    ]

    for employee in employees:
        db.session.add(employee)
    db.session.commit()
