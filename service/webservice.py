import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask_restful import Api
from service.commons import app
from rest.resources import *

api = Api(app)

api.add_resource(DepartmentRes, '/departments/<name>')
api.add_resource(DepartmentList, '/departments/')
api.add_resource(EmployeeRes, '/employees/<id>')
api.add_resource(EmployeeList, '/employees/')


if __name__ == '__main__':
    print(sys.path)
    app.run()
