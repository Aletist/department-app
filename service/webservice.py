from flask_restful import Api
from service.commons import app
from rest.resources import *

api = Api(app)

api.add_resource(Dept, '/departments/<name>')
api.add_resource(DeptList, '/departments/')
api.add_resource(Emp, '/employees/<id>')
api.add_resource(EmpList, '/employees/')

if __name__ == '__main__':
    app.run()
