from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import NumberRange, NoneOf
from wtforms.widgets import html5


class DepartmentForm(FlaskForm):
    dept_name = StringField('Department name:',
                            validators=[validators.data_required(),
                                        NoneOf(['unassigned', 'filter', 'add'], message='Dont use reserved names'),
                                        validators.Regexp('^[a-zA-Z0-9_]*$', message=('Department name must'
                                                                                      ' contain only letters,'
                                                                                      ' numbers or underscore'))])
    dept_head = SelectField('Department head:', coerce=int)
    head_salary = IntegerField('Department head`s salary:', widget=html5.NumberInput(),
                               validators=[validators.Optional(),
                                           NumberRange(min=0, message='People don`t pay to work')])


class DepartmentsFilterForm(FlaskForm):
    min_employees = IntegerField('Employees from:', widget=html5.NumberInput(),
                                 validators=[validators.Optional(),
                                             NumberRange(min=0, message='Number of people can not be negative')])
    max_employees = IntegerField('to:', widget=html5.NumberInput(),
                                 validators=[validators.Optional(),
                                             NumberRange(min=0, message='Number of people can not be negative')])
    min_salary = IntegerField('Average salary from:', widget=html5.NumberInput(),
                              validators=[validators.Optional(),
                                          NumberRange(min=0, message='People don`t pay to work')])
    max_salary = IntegerField('to:', widget=html5.NumberInput(),
                              validators=[validators.Optional(),
                                          NumberRange(min=0, message='People don`t pay to work')])

    def validate_on_submit(self):
        result = super(DepartmentsFilterForm, self).validate()
        if self.min_salary.data is not None and self.max_salary.data is not None:
            if self.min_salary.data > self.max_salary.data:
                self.min_salary.errors.append('Min filter for salary can`t be more than max filter')
                result = False

        if self.min_employees.data is not None and self.max_employees.data is not None:
            if self.min_employees.data > self.max_employees.data:
                self.min_employees.errors.append('Min filter for employee count can`t be more than max filter')
                result = False
        return result


class EmployeeFilterForm(FlaskForm):
    birth_date_min = DateField('Birth date from', validators=[validators.Optional()])
    birth_date_max = DateField('to', validators=[validators.Optional()])
    hire_date_min = DateField('Hire date from', validators=[validators.Optional()])
    hire_date_max = DateField('to', validators=[validators.Optional()])
    min_salary = IntegerField('Average salary from:', widget=html5.NumberInput(),
                              validators=[validators.Optional(),
                                          NumberRange(min=0, message='People don`t pay to work')])
    max_salary = IntegerField('to:', widget=html5.NumberInput(),
                              validators=[validators.Optional(),
                                          NumberRange(min=0, message='People don`t pay to work')])

    def validate_on_submit(self):
        result = super(EmployeeFilterForm, self).validate()
        if self.birth_date_min.data is not None and self.birth_date_max.data is not None:
            if self.birth_date_min.data > self.birth_date_max.data:
                self.birth_date_min.errors.append('Min filter for birth date can`t be more than max filter')
                result = False

        if self.hire_date_min.data is not None and self.hire_date_max.data is not None:
            if self.hire_date_min.data > self.hire_date_max.data:
                self.hire_date_min.errors.append('Min filter for birth date can`t be more than max filter')
                result = False

        if self.min_salary.data is not None and self.max_salary.data is not None:
            if self.min_salary.data > self.max_salary.data:
                self.min_salary.errors.append('Min filter for salary can`t be more than max filter')
                result = False
        return result


class EmployeeAddForm(FlaskForm):
    birth_date = DateField('Birth date', validators=[validators.Optional()])

    first_name = StringField('First name:',
                             validators=[
                                 validators.data_required(),
                                 validators.Regexp('^[a-zA-Z0-9_]*$',
                                                   message=('Department name must'
                                                            ' contain only letters,'
                                                            ' numbers or underscore'))])
    last_name = StringField('Last name:',
                            validators=[
                                validators.data_required(),
                                validators.Regexp('^[a-zA-Z0-9_]*$',
                                                  message=('Department name must'
                                                           ' contain only letters,'
                                                           ' numbers or underscore'))])


class EmployeeEditForm(FlaskForm):
    birth_date = DateField('Birth date', validators=[validators.data_required()])

    hire_date = DateField('Hire date', validators=[validators.data_required()])

    department = SelectField('Department:')

    salary = IntegerField('Salary:', widget=html5.NumberInput(),
                          validators=[validators.Optional(),
                                      NumberRange(min=0, message='People don`t pay to work')])

    first_name = StringField('First name:',
                             validators=[
                                 validators.data_required(),
                                 validators.Regexp('^[a-zA-Z0-9_]*$',
                                                   message=('Department name must'
                                                            ' contain only letters,'
                                                            ' numbers or underscore'))])
    last_name = StringField('Last name:',
                            validators=[
                                validators.data_required(),
                                validators.Regexp('^[a-zA-Z0-9_]*$',
                                                  message=('Department name must'
                                                           ' contain only letters,'
                                                           ' numbers or underscore'))])

    def validate_on_submit(self):
        result = super(EmployeeEditForm, self).validate()
        if self.birth_date.data is not None and self.hire_date.data is not None:
            if self.birth_date.data > self.hire_date.data:
                self.birth_date.errors.append('Started working before birth? Impressive.')
                result = False
        return result
