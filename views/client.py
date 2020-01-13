import requests
from flask import Flask, url_for, redirect, render_template, request

from forms import DepartmentsFilterForm, DepartmentForm, EmployeeFilterForm

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['WTF_CSRF_ENABLED'] = False
api_url = 'http://api.department-app/'


def format_emplyee(id, first_name, last_name):
    return '{}, {} {}'.format(id, first_name, last_name)


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


@app.route('/departments/add', methods=['GET', 'POST'])
def add_dept():
    api_request = requests.get(api_url + 'employees?department=unassigned')
    candidates = api_request.json()
    candidates_list = [(-1, 'Unassigned')] + [(person['id'], '{}, {} {}'
                                               .format(person['id'],
                                                       person['first_name'],
                                                       person['last_name'])
                                               ) for person in candidates]
    form = DepartmentForm()
    form.dept_head.choices = candidates_list
    if form.validate_on_submit():
        args_string = 'departments?name={}'.format(form.dept_name.data)
        if form.dept_head.data > -1:
            args_string += '&head_id={}'.format(form.dept_head.data)
            if form.head_salary.data is not None:
                args_string += '&head_salary={}'.format(form.head_salary.data)
        api_request = requests.post(api_url + args_string)
        print(api_request.status_code)
        return redirect(url_for('departments'))
    return render_template('department_add.html', form=form)


@app.route('/departments/delete', methods=['POST'])
def del_dept():
    data = request.form.to_dict()
    print(data)
    return redirect(url_for('departments'))


@app.route('/departments/<name>', methods=['GET', 'POST'])
def department(name):
    request = requests.get(api_url + 'departments/' + name)
    dept = request.json()
    request = requests.get(api_url + 'employees/?department=' + dept['name'])
    employees = request.json()

    head = next((person for person in employees
                 if person["id"] == dept['head_id']
                 ), None)

    if head is not None:
        form = DepartmentForm(dept_name=dept['name'], head_salary=head['salary'])
    else:
        form = DepartmentForm(dept_name=dept['name'])

    dept['head'] = 'unassigned' if head is None \
        else (format_emplyee(head['id'],
                             head["first_name"], head["last_name"])
              )
    candidates_list = [(person['id'],
                        format_emplyee(person['id'],
                                       person['first_name'],
                                       person['last_name'])
                        ) for person in employees]
    candidates_list.insert(0, (-1, 'Unassigned'))

    if head is not None:  # making current head the first (default) option
        current_head = (head['id'], format_emplyee(head['id'], head['first_name'], head['last_name']))
        candidates_list.remove(current_head)
        candidates_list.insert(0, current_head)

    form.dept_head.choices = candidates_list
    if form.validate_on_submit():
        args_string = 'departments/{}?name={}'.format(name, form.dept_name.data)
        args_string += '&head_id={}'.format(form.dept_head.data)

        if form.head_salary.data is not None:
            args_string += '&head_salary={}'.format(form.head_salary.data)

        api_request = requests.put(api_url + args_string)
        print(api_request.status_code)
        return redirect(url_for('department', name=form.dept_name.data))

    dept['head_salary'] = None if head is None else head['salary']
    return render_template('department.html', dept=dept, employees=employees, form=form)


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
    form = EmployeeFilterForm()
    request_args = ''

    if form.validate_on_submit():
        request_args = '?'
        print(form.birth_date_min.data,
              form.birth_date_max.data,
              form.hire_date_min.data,
              form.hire_date_max.data)

        if form.birth_date_min.data is not None:
            request_args += '&min_birth={}'.format(form.birth_date_min.data)
        if form.birth_date_max.data is not None:
            request_args += '&max_birth={}'.format(form.birth_date_max.data)

        if form.birth_date_min.data is not None:
            request_args += '&min_hire={}'.format(form.birth_date_min.data)
        if form.birth_date_max.data is not None:
            request_args += '&max_hire={}'.format(form.birth_date_max.data)

        if form.min_salary.data is not None:
            request_args += '&min_salary={}'.format(form.min_salary.data)
        if form.max_salary.data is not None:
            request_args += '&max_salary={}'.format(form.max_salary.data)

    api_request = requests.get(api_url + 'employees' + request_args)
    employees = api_request.json()
    return render_template('employees_filter.html', employees=employees, form=form)


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
