from datetime import date
from service.commons import db


def serialize_dept(list):
    return {
        'name': list[0],
        'avg_salary': list[1],
        'employees': list[2]
    }


def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime('%Y-%m-%d')


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Integer, nullable=True)
    department = db.Column(db.String(64), db.ForeignKey('department.name'), nullable=True)
    is_head = db.Column(db.Boolean, nullable=False, default=False)
    birth_date = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=date.today())

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'salary': self.salary,
            'department': self.department,
            'is_head': self.is_head,
            'birth_date': dump_date(self.birth_date),
            'hire_date': dump_date(self.hire_date)
        }


class Department(db.Model):
    __tablename__ = 'department'
    name = db.Column(db.String(64), primary_key=True)
