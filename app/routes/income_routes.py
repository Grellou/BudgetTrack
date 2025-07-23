import logging
from flask import Blueprint, redirect, render_template, flash, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.forms.income_forms import IncomeForm 
from flask_login import current_user, login_required
from app import db
from app.models.category_model import CategoryModel
from app.models.income_model import IncomeModel

bp = Blueprint("incomes", __name__)

# Display list of all incomes
@bp.route("/incomes/list")
@login_required
def income_list_page():
    incomes = IncomeModel.query.all()

    # Calculate total
    total_amount = sum(float(income.amount) for income in incomes)

    return render_template("incomes/list.html", incomes=incomes, total_amount=total_amount)

# Create new income
@bp.route("/incomes/add", methods=["GET", "POST"])
@login_required
def income_add_page():
    form = IncomeForm()

    # Get and populate dropdown list with categories
    categories = CategoryModel.query.filter(
        ((CategoryModel.user_id == current_user.id) |
            (CategoryModel.user_id == None )) &
                (CategoryModel.type == "Income")
    ).order_by(CategoryModel.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():

        # Create income 
        income = IncomeModel(
            amount=form.amount.data, # type: ignore
            date=form.date.data, # type: ignore
            description=form.description.data, # type: ignore
            category_id=form.category_id.data, # type: ignore
            notes=form.notes.data, # type: ignore
            user_id=current_user.id # type: ignore
        )

        # Add to db
        try:
            db.session.add(income)
            db.session.commit()
            flash("Income added successfully!", "success")
            return redirect(url_for("incomes.income_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while adding income. Please try again.", "danger")
            logging.error(f"Database error when adding income: {e}")

    return render_template("incomes/form.html", form=form, title="Add income")

# Edit income
@bp.route("/incomes/edit/<int:id>", methods=["GET", "POST"])
@login_required
def income_edit_page(id):
    income = IncomeModel.query.get_or_404(id)

    # Prevent editing other user's incomes 
    if income.user_id and income.user_id != current_user.id:
        flash("You don't have permissions to edit this income.", "danger")
        return redirect(url_for("incomes.income_list_page"))

    # Create form with pre-populated form data and update on validation
    form = IncomeForm(obj=income)

    if form.validate_on_submit():
        income.amount = form.amount.data
        income.date = form.date.data
        income.description = form.description.data
        income.notes = form.notes.data

        # Add to db
        try:
            db.session.commit()
            flash("Income updated successfully!", "success")
            return redirect(url_for("incomes.income_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while editing income. Please try again.", "danger")
            logging.error(f"Database error income expense: {e}")

    return render_template("incomes/form.html", form=form, title="Editing Income", income=income)

# Delete income
@bp.route("/incomes/delete/<int:id>", methods=["POST"])
@login_required
def income_delete_page(id):
    income = IncomeModel.query.get_or_404(id)
    
    # Prevent deleting other user's income
    if income.user_id and income.user_id != current_user.id:
        flash("You don't have permissions to delete this income.", "danger")
        return redirect(url_for("incomes.income_list_page"))

    # Delete expense
    try:
        db.session.delete(income)
        db.session.commit()
        flash("Income deleted.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error while deleting income. Please try again.", "danger")
        logging.error(f"Database error while deleting income: {e}")

    return redirect(url_for("incomes.income_list_page"))
