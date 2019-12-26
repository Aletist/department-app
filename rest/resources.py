from flask import jsonify, request
from flask_restful import Resource, reqparse
from sqlalchemy import func, cast, Integer

from models.models import Employee, Department, serialize_dept
from service.commons import db


class DepartmentRes(Resource):

    def get(self, name):
        query = db.session.query(Department.name).outerjoin(
            Employee, Employee.department == Department.name
        ).add_columns(
            cast(func.avg(Employee.salary), Integer).label('avg'),
            func.count(Employee.id).label('cnt')
        ).filter(
            Department.name == name
        )
        result = serialize_dept(query.first())
        return jsonify(result)

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        department = Department.query.get(name)
        department.name = args['name']
        db.session.commit()
        return '', 200

    def delete(self, name):
        dept = Department.query.get(name)
        db.session.delete(dept)
        db.session.commit()
        return '', 204


class DepartmentList(Resource):
    def get(self):
        query = db.session.query(Department.name).outerjoin(
            Employee, Employee.department == Department.name
        ).add_columns(
            cast(func.avg(Employee.salary), Integer).label('avg'),
            func.count(Employee.id).label('cnt')
        ).group_by(Department.name)
        result = [serialize_dept(item) for item in query.all()]
        return jsonify(result)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        db.session.add(Department(name=args['name']))
        db.session.commit()
        dept = Department.query.get(args['name'])
        print(dept.name)
        return args['name'], 201


class EmployeeRes(Resource):
    def get(self, id):
        employee = Employee.query.get(id)
        return jsonify(employee.serialize())

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('birth_date')
        parser.add_argument('department', type=str)
        parser.add_argument('is_head', type=bool)
        parser.add_argument('hire_date')
        parser.add_argument('salary', type=int)

        args = {k: v for k, v in parser.parse_args().items() if v is not None}
        print(args)

        employee = Employee.query.get(id)
        print(employee.serialize())
        for key in args:
            setattr(employee, key, args[key])
        print(employee.serialize())
        db.session.commit()

        return '', 200

    def delete(self, id):
        employee = Employee.query.get(id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


class EmployeeList(Resource):

    def get(self):
        department = request.args.get('department', None)
        min_salary = request.args.get('min_salary', None)
        max_salary = request.args.get('max_salary', None)
        min_birth = request.args.get('min_birth', None)
        max_birth = request.args.get('max_birth', None)
        min_hire = request.args.get('min_hire', None)
        max_hire = request.args.get('max_hire', None)

        query = Employee.query
        if min_salary is not None: query = query.filter(Employee.salary >= int(min_salary))
        if max_salary is not None: query = query.filter(Employee.salary <= int(max_salary))
        if min_birth is not None: query = query.filter(Employee.birth_date >= min_birth)
        if max_birth is not None: query = query.filter(Employee.birth_date <= max_birth)
        if min_hire is not None: query = query.filter(Employee.hire_date >= min_hire)
        if max_hire is not None: query = query.filter(Employee.hire_date <= max_hire)
        if department is not None:
            if department == 'unassigned':
                department = None
            query = query.filter(Employee.department == department)
        result = query.all()
        return jsonify([item.serialize() for item in result])

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', required=True)
        args = parser.parse_args()

        employee = Employee(
            first_name=args['first_name'],
            last_name=args['last_name'],
            birth_date=args['birth_date']
        )
        db.session.add(employee)
        db.session.commit()
        return employee.id, 201
