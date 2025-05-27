from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

class EcoActionForm(FlaskForm):
    action_text = TextAreaField('What eco-friendly action did you take today?', 
                              validators=[DataRequired(), Length(min=5, max=200)])
    category = SelectField('Category', 
                         choices=[('energy', 'Energy Conservation'), 
                                  ('waste', 'Waste Reduction'),
                                  ('transport', 'Sustainable Transport'),
                                  ('food', 'Sustainable Food'),
                                  ('water', 'Water Conservation'),
                                  ('other', 'Other')])
    submit = SubmitField('Log Action')

class GoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Goal Description', validators=[DataRequired(), Length(min=10, max=500)])
    target_date = DateField('Target Completion Date (optional)', format='%Y-%m-%d')
    submit = SubmitField('Set Goal')