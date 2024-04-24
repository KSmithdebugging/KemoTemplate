# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.fields import URLField, DateField, IntegerRangeField, EmailField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, RadioField
from wtforms_components import TimeField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')

class MathTopicForm(FlaskForm):
    math_level = SelectField('Math Level', choices=[
        ('algebra1', 'Algebra 1'), 
        ('algebra2', 'Algebra 2'),
        ('geometry', 'Geometry'), 
        ('precalculus', 'Pre Calculus'), 
        ('stats', 'Statistics')
    ])
    practice_problem_one = StringField('Practice Problem One',validators=[DataRequired()])
    practice_problem_two= StringField('Practice Problem Two',validators=[DataRequired()])
    practice_problem_three = StringField('Practice Problem Three',validators=[DataRequired()])
    solution_one = StringField('Solution One',validators=[DataRequired()])
    solution_two = StringField('Solution Two',validators=[DataRequired()])
    solution_three = StringField('Solution Three',validators=[DataRequired()])
    topic_name = StringField('Topic Name',validators=[DataRequired()])
    tutorial_video = StringField('Tutorial Video')
    submit = SubmitField('Submit')
            


class ClinicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
