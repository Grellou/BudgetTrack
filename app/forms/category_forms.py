from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models.category_model import CategoryModel

# Category form
class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired(), Length(min=3, max=64)])
    type = SelectField("Category type", choices=[("Income", "Income"), ("Expense", "Expense"), ("Credit", "Credit")])
    description = TextAreaField("Category description", validators=[Length(max=128)])
    submit = SubmitField("Save category")

    # Validate if category name is not taken
    def validate_name(self, name):
        from flask import request

        # Get category ID from URL while editing
        category_id = request.view_args.get("id") if request.view_args else None

        # Check for existing category by name
        existing_category = CategoryModel.query.filter_by(name=name.data).first()

        # If category with this name exists and it's not the one being edited
        if existing_category and (not category_id or existing_category.id != category_id):
            raise ValidationError("This category already exists.")

