import requests
from flask import Flask, url_for, redirect, render_template, request

from forms import DepartmentsFilterForm

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['WTF_CSRF_ENABLED'] = False
api_url = 'http://api.department-app/'


@app.route('/')
def home():
    return redirect(url_for('departments'))


@app.route('/departments/')
def departments():
    request = requests.get(api_url + 'departments')
    depts = request.json()
    request = requests.get(api_url + 'employees/heads')
    heads = request.json()

    for dept in depts:
        head = next((item
                     for item
                     in heads
                     if item["id"] == dept['head_id']),
                    None)
        dept['head'] = ('unassigned'
                        if head is None
                        else '{} {}'.format(head["first_name"],
                                            head["last_name"]))
    return render_template('departments.html', depts=depts)


@app.route('/departments/filter', methods=['POST', 'GET'])
def departments_filter():
    form = DepartmentsFilterForm()
    api_request = requests.get(api_url + 'employees/heads')
    heads = api_request.json()
    api_request = requests.get(api_url + 'departments')
    depts = api_request.json()

    if form.validate_on_submit():
        if form.min_employees.data is not None:
            depts = [dept for dept in depts
                     if dept['employees'] >= form.min_employees.data]
        if form.max_employees.data is not None:
            depts = [dept for dept in depts
                     if dept['employees'] <= form.max_employees.data]
        if form.min_salary.data is not None:
            depts = [dept for dept in depts
                     if dept['avg_salary'] >= form.min_salary.data]
        if form.max_salary.data is not None:
            depts = [dept for dept in depts
                     if dept['avg_salary'] <= form.max_salary.data]
    for dept in depts:
        head = next((item
                     for item
                     in heads
                     if item["id"] == dept['head_id']),
                    None)
        dept['head'] = ('unassigned'
                        if head is None
                        else '{} {}'.format(head["first_name"],
                                            head["last_name"]))
    return render_template('departments_filter.html', depts=depts, form=form)


@app.route('/departments/add')
def add_dept():
    api_request = requests.get(api_url + 'employees?department=unassigned')
    candidates = api_request.json()
    return render_template('department_add.html', candidates=candidates)


@app.route('/departments/add/submit', methods=['POST'])
def submit_dept():
    data = request.form.to_dict()
    print(data)
    return redirect(url_for('departments'))


@app.route('/departments/delete', methods=['POST'])
def del_dept():
    data = request.form.to_dict()
    print(data)
    return redirect(url_for('departments'))


@app.route('/departments/<name>')
def department(name):
    request = requests.get(api_url + 'departments/' + name)
    dept = request.json()
    request = requests.get(api_url + 'employees/?department=' + dept['name'])
    employees = request.json()
    head = next(
        (person
         for person
         in employees
         if person["id"] == dept['head_id']
         ), None)
    dept['head'] = \
        'unassigned' if head is None \
            else ('{}, {} {}'
                  .format(head['id'],
                          head["first_name"],
                          head["last_name"])
                  )
    dept['head_salary'] = \
        None if head is None \
            else head['salary']

    return render_template('department.html', dept=dept, employees=employees)


@app.route('/departments/<name>/edit', methods=['POST'])
def edit_dept(name):
    data = request.form.to_dict()
    print(data)
    return redirect(url_for('department', name=name))


@app.route('/employees/')
def employees():
    api_request = requests.get(api_url + 'employees')
    employees = api_request.json()
    return render_template('employees.html', employees=employees)


@app.route('/employees/filter', methods=['GET', 'POST'])
def employees_filter():
    api_request = requests.get(api_url + 'employees')
    employees = api_request.json()
    return render_template('employees_filter.html', employees=employees)


@app.route('/departments/remove/<id>')
def remove_employee(id):
    return redirect(url_for('department'))


@app.route('/employees/<id>')
def employee(id):
    api_request = requests.get(api_url + 'employees/' + id)
    employee = api_request.json()
    api_request = requests.get(api_url + 'departments')
    depts = api_request.json()
    return render_template('employee.html', employee=employee, departments=depts)


@app.route('/employees/<id>/delete')
def del_employee(id):
    return redirect(url_for('department'))


@app.route('/employees/edit')
def edit_employee(id):
    return redirect(url_for('employees'))


@app.route('/employees/add')
def add_employee():
    return render_template('employee_add.html')


if __name__ == '__main__':
    app.run()
