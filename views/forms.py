from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, SelectField
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
        result = True
        result = super(DepartmentsFilterForm, self).validate()
        if self.min_salary.data is not None and self.max_salary.data is not None:
            if self.min_salary.data > self.max_salary.data:
                self.min_salary.errors.append('Min salary should be less or equal than max salary')
                result = False
        if self.min_employees.data is not None and self.max_employees.data is not None:
            if self.min_employees.data > self.max_employees.data:
                self.min_employees.errors.append('Min number should be less or equal than max number of employees')
                result = False
        return result
