from flask import jsonify, request
from flask_restful import Resource, reqparse, inputs, abort
from sqlalchemy import func, cast, Integer

from models.models import Employee, Department, serialize_dept, Head
from service.commons import db


class Dept(Resource):

    def get(self, name):
        query = db.session \
            .query(Department.name) \
            .outerjoin(Employee,
                       Employee.department
                       == Department.name) \
            .add_columns(cast(func.avg(Employee.salary), Integer)
                         .label('avg'), func.count(Employee.id)
                         .label('cnt')) \
            .outerjoin(Head, Head.department_name == Department.name) \
            .add_columns(Head.head_id
                         .label('head')) \
            .filter(Department.name == name)
        result = query.first()
        if result[0] is None:
            abort(404)
        return jsonify(serialize_dept(result))

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('head_id', type=int)
        parser.add_argument('head_salary', type=int)
        args = parser.parse_args()
        department = Department.query.get(name)
        if department is None:
            abort(400)
        department.name = args['name']
        if args['head_id'] == -1:
            department.head.head_id = None
        elif args['head_id'] is not None:
            employee = Employee.query.get(args['head_id'])
            if employee is None:
                abort(400)
            department.head.head_id = args['head_id']
            if args['head_salary'] is not None:
                employee.salary = args['head_salary']
        db.session.commit()
        return '', 200

    def delete(self, name):
        department = Department.query.get(name)
        if department is None:
            abort(400)
        employees = Employee.query \
            .filter(Employee.department == name)
        for employee in employees:
            employee.salary = None
        db.session.delete(department)
        db.session.commit()
        return '', 204


class DeptList(Resource):
    def get(self):
        query = db.session \
            .query(Department.name) \
            .outerjoin(Employee, Employee.department == Department.name) \
            .add_columns(cast(func.avg(Employee.salary), Integer)
                         .label('avg'), func.count(Employee.id)
                         .label('cnt')) \
            .outerjoin(Head, Head.department_name == Department.name) \
            .add_columns(Head.head_id
                         .label('head')) \
            .group_by(Department.name)
        result = [serialize_dept(item)
                  for item
                  in query.all()]
        return jsonify(result)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('head_id', type=int)
        parser.add_argument('head_salary', type=int)
        args = parser.parse_args()

        dept = Department.query.get(args['name'])
        if dept is not None:
            abort(409)
        dept = Department(name=args['name'])
        emp = None
        if args['head_id'] is not None:
            emp = Employee.query.get(args['head_id'])
            if emp is None:
                abort(400)
        head = Head(department_name=dept.name,
                    head_id=args['head_id'])
        db.session.add(dept)
        db.session.add(head)
        if emp is not None:
            emp.salary = args['head_salary']
            emp.department = dept.name
        db.session.commit()
        return args['name'], 201


class Emp(Resource):
    def get(self, id):
        employee = Employee.query.get(id)
        if employee is None:
            abort(404)
        return jsonify(employee.serialize())

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('birth_date')
        parser.add_argument('department', type=str)
        parser.add_argument('hire_date')
        parser.add_argument('salary', type=int)
        args = {k: v
                for k, v
                in parser.parse_args().items()
                if v is not None}
        if args.get('department') == 'unassigned':
            args['department'] = None
        if args.get('salary') == 1:
            args['salary'] = None
        employee = Employee.query.get(id)
        if employee is None:
            abort(404)
        for key in args:
            setattr(employee, key, args[key])
        db.session.commit()
        return '', 200

    def delete(self, id):
        employee = Employee.query.get(id)
        if employee is None:
            abort(400)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


class EmpList(Resource):

    def get(self):
        department = request.args.get('department', None)
        min_salary = request.args.get('min_salary', None)
        max_salary = request.args.get('max_salary', None)
        min_birth = request.args.get('min_birth', None)
        max_birth = request.args.get('max_birth', None)
        min_hire = request.args.get('min_hire', None)
        max_hire = request.args.get('max_hire', None)
        query = Employee.query
        if min_hire is not None:
            query = query \
                .filter(Employee
                        .hire_date >= min_hire)
        if max_hire is not None:
            query = query \
                .filter(Employee
                        .hire_date <= max_hire)
        if min_birth is not None:
            query = query \
                .filter(Employee
                        .birth_date >= min_birth)
        if max_birth is not None:
            query = query \
                .filter(Employee
                        .birth_date <= max_birth)
        if min_salary is not None:
            query = query \
                .filter(Employee
                        .salary >= int(min_salary))
        if max_salary is not None:
            query = query \
                .filter(Employee
                        .salary <= int(max_salary))
        if department is not None:
            if department == 'unassigned':
                department = None
            query = query \
                .filter(Employee
                        .department == department)
        result = query.all()
        return jsonify([item.serialize()
                        for item
                        in result])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', required=True)
        args = parser.parse_args()
        employee = Employee(first_name=args['first_name'],
                            last_name=args['last_name'],
                            birth_date=args['birth_date'])
        db.session.add(employee)
        db.session.commit()
        return employee.id, 201


class Heads(Resource):
    def get(self):
        query = db.session.query(Head.head_id)
        ids = [id
               for (id,)
               in query.all()
               if id is not None]
        print(ids)
        query = Employee.query.filter(Employee.id.in_(ids))
        return jsonify([head.serialize()
                        for head
                        in query.all()])
