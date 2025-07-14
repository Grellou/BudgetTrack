from flask_wtf import FlaskForm
from wtforms import SubmitField,  TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

# Income form
class IncomeForm(FlaskForm):
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0")])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    description = TextAreaField("Description", validators=[Length(max=128)])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save Income")
