from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


# Credit form
class CreditForm(FlaskForm):
    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message="Amount must be greater than 0"),
        ],
    )
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    description = TextAreaField("Description", validators=[Length(max=128)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save Credit")
