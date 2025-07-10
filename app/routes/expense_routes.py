import logging
from flask import Blueprint, redirect, render_template, flash, request, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.forms.expense_forms import ExpenseForm
from flask_login import current_user, login_required
from app import db
from app.models.category_model import CategoryModel
from app.models.expense_model import ExpenseModel

bp = Blueprint("expenses", __name__)

# Display all expenses
@bp.route("/expenses/list")
@login_required
def expense_list_page():
    # Filter parameters
    category_id = request.args.get("category", type=int)
    query = ExpenseModel.query.filter_by(user_id=current_user.id)

    # Apply filter
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Get all categories
    categories = CategoryModel.query.filter(
        (CategoryModel.user_id == current_user.id) | (CategoryModel.user_id == None) # noqa
    ).order_by(CategoryModel.name).all()

    # Order by date
    expenses = query.order_by(ExpenseModel.date.desc()).all()

    # Calculate total
    total_amount = sum(float(expense.amount) for expense in expenses)

    return render_template("expenses/list.html", expenses=expenses, categories=categories, total_amount=total_amount, selected_category=category_id)

# Create new expense
@bp.route("/expenses/add", methods=["GET", "POST"])
@login_required
def expense_add_page():
    form = ExpenseForm()

    # Get and populate dropdown list with categories
    categories = CategoryModel.query.filter(
        (CategoryModel.user_id == current_user.id) | (CategoryModel.user_id == None) # noqa
    ).order_by(CategoryModel.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():

        # Create expense
        expense = ExpenseModel(
            amount=form.amount.data, # type: ignore
            date=form.date.data, # type: ignore
            description=form.description.data, # type: ignore
            category_id=form.category_id.data, # type: ignore
            notes=form.notes.data, # type: ignore
            user_id=current_user.id # type: ignore
        )

        # Add to db
        try:
            db.session.add(expense)
            db.session.commit()
            flash("Expense added successfully!", "success")
            return redirect(url_for("expenses.expense_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while adding expense. Please try again.", "danger")
            logging.error(f"Database error when adding expense: {e}")

    return render_template("expenses/form.html", form=form, title="Add Expense")

# Edit expense
@bp.route("/expenses/edit/<int:id>", methods=["GET", "POST"])
@login_required
def expense_edit_page(id):
    expense = ExpenseModel.query.get_or_404(id)

    # Prevent editing other user's expenses
    if expense.user_id and expense.user_id != current_user.id:
        flash("You don't have permissions to edit this expense.", "danger")
        return redirect(url_for("expenses.expense_list_page"))

    # Create form with pre-populated form data and update on validation
    form = ExpenseForm(obj=expense)

    # Get and populate dropdown list with categories
    categories = CategoryModel.query.filter(
        (CategoryModel.user_id == current_user.id) | (CategoryModel.user_id == None) # noqa
    ).order_by(CategoryModel.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    # Set the currently selected category option
    if request.method == 'GET':
        form.category_id.data = expense.category_id

    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.date = form.date.data
        expense.description = form.description.data
        expense.category_id = form.category_id.data
        expense.notes = form.notes.data

        # Add to db
        try:
            db.session.commit()
            flash("Expense updated successfully!", "success")
            return redirect(url_for("expenses.expense_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while editing expense. Please try again.", "danger")
            logging.error(f"Database error editing expense: {e}")

    return render_template("expenses/form.html", form=form, title="Editing Expense", expense=expense)

# Delete exepse
@bp.route("/expenses/delete/<int:id>", methods=["POST"])
@login_required
def expense_delete_page(id):
    expense = ExpenseModel.query.get_or_404(id)
    
    # Prevent deleting other user's expense
    if expense.user_id and expense.user_id != current_user.id:
        flash("You don't have permissions to delete this expense.", "danger")
        return redirect(url_for("expenses.expense_list_page"))

    # Delete expense
    try:
        db.session.delete(expense)
        db.session.commit()
        flash("Expense deleted.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error while deleting expense. Please try again.", "danger")
        logging.error(f"Database error while deleting expense: {e}")

    return redirect(url_for("expenses.expense_list_page"))
