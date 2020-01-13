from datetime import date
from service.commons import db


def serialize_dept(list):
    return {
        'name': list[0],
        'avg_salary': list[1],
        'employees': list[2],
        'head_id': list[3]
    }


def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime('%Y-%m-%d')


class Department(db.Model):
    __tablename__ = 'department'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    name = db.Column(db.String(64),
                     primary_key=True)
    head = db.relationship('Head',
                           backref='department',
                           passive_deletes=True,
                           uselist=False)


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Integer, nullable=True)
    department = db.Column(db.String(64),
                           db.ForeignKey('department.name',
                                         ondelete='SET NULL',
                                         onupdate='CASCADE'),
                           nullable=True)
    birth_date = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date,
                          nullable=False,
                          default=date.today())
    dept = db.relationship('Department',
                           backref=db.backref('employee',
                                              passive_deletes=True,
                                              passive_updates=True))
    head = db.relationship('Head',
                           backref='employee',
                           passive_deletes=True,
                           uselist=False)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'salary': self.salary,
            'department': self.department,
            'birth_date': dump_date(self.birth_date),
            'hire_date': dump_date(self.hire_date)
        }


class Head(db.Model):
    __tablename__ = 'head'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    department_name = db.Column(db.String(64),
                                db.ForeignKey('department.name',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                                primary_key=True)
    head_id = db.Column(db.Integer,
                        db.ForeignKey('employee.id',
                                      ondelete='SET NULL',
                                      onupdate='CASCADE'),
                        nullable=True)

    def serialize(self):
        return {
            'department_name': self.department_name,
            'head_id': self.head_id,
        }
