from datetime import date
import pymysql
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from models.models import Employee, Department, Head
from setup import app, db
from config import DatabaseConfig


class Connect(Command):
    def run(self):
        try:
            # Create a cursor object
            cursorInsatnce = DatabaseConfig.connectionInstance.cursor()
            # SQL Statement to create a database
            sqlStatement = "CREATE DATABASE " + DatabaseConfig.newDatabaseName
            # Execute the create database SQL statment through the cursor instance
            cursorInsatnce.execute(sqlStatement)
            # SQL query string
            sqlQuery = "SHOW DATABASES"
            # Execute the sqlQuery
            cursorInsatnce.execute(sqlQuery)
            # Fetch all the rows
            databaseList = cursorInsatnce.fetchall()
            for database in databaseList:
                print(database)


        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            DatabaseConfig.connectionInstance.close()


class Seed(Command):
    def run(self):
        depts = [Department(name='IT'),
                 Department(name='Sales'),
                 Department(name='Research'),
                 Department(name='PR')]

        for dept in depts:
            db.session.add(dept)
        db.session.commit()

        employees = [
            Employee(first_name='Siusan',
                     last_name='Turner',
                     department='PR',
                     salary=3340,
                     birth_date=date(1995, 4, 7)
                     ),
            Employee(first_name='Andrew',
                     last_name='Miles',
                     department='IT',
                     salary=1700,
                     birth_date=date(1989, 1, 17)
                     ),
            Employee(first_name='Oleg',
                     last_name='Sidorov',
                     department='IT',
                     salary=1600,
                     birth_date=date(1990, 7, 13)
                     ),
            Employee(first_name='Brian',
                     last_name='Fox',
                     department='Research',
                     salary=3500,
                     birth_date=date(1990, 1, 6)
                     ),
            Employee(first_name='Steve',
                     last_name='Johnson',
                     birth_date=date(1999, 9, 9)
                     ),
            Employee(first_name='Martin',
                     last_name='Black',
                     birth_date=date(1988, 8, 18)
                     ),
            Employee(first_name='Alex',
                     last_name='Jones',
                     department='PR',
                     salary=3400,
                     birth_date=date(1975, 3, 17)
                     ),
            Employee(first_name='Michael',
                     last_name='Payne',
                     department='IT',
                     salary=3200,
                     birth_date=date(1980, 7, 25)
                     ),
            Employee(first_name='Jonathan',
                     last_name='Miles',
                     department='Research',
                     salary=1100,
                     birth_date=date(1989, 9, 17)
                     ),
            Employee(first_name='Stefanie',
                     last_name='Miller',
                     department='Research',
                     salary=1300,
                     birth_date=date(1990, 5, 12)
                     ),
            Employee(first_name='Taras',
                     last_name='Prokopenko',
                     department='Sales',
                     salary=1000,
                     birth_date=date(1990, 4, 2)
                     )
        ]

        for employee in employees:
            db.session.add(employee)
        db.session.commit()

        heads = [
            Head(department_name='IT', head_id=8),
            Head(department_name='PR', head_id=1),
            Head(department_name='Research', head_id=4),
            Head(department_name='Sales')
        ]

        for head in heads:
            db.session.add(head)
        db.session.commit()


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('connect', Connect())
manager.add_command('seed', Seed())


def main():
    manager.run()

if __name__ == '__main__':
    main()
