from flask_restful import Api
from setup import app
from rest.resources import *

api = Api(app)

api.add_resource(Dept, '/departments/<name>')
api.add_resource(DeptList, '/departments/')
api.add_resource(Emp, '/employees/<id>')
api.add_resource(EmpList, '/employees/')
api.add_resource(Heads, '/employees/heads')

if __name__ == '__main__':
    app.run()
