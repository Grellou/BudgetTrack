import logging

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.forms.credit_forms import CreditForm
from app.models.category_model import CategoryModel
from app.models.credit_model import CreditModel

bp = Blueprint("credits", __name__)


# Display list of all credits
@bp.route("/credits/list")
@login_required
def credit_list_page():
    credits = CreditModel.query.all()

    # Calculate total
    total_amount = sum(float(credit.amount) for credit in credits)

    return render_template(
        "credits/list.html", credits=credits, total_amount=total_amount
    )


# Create new credit
@bp.route("/credits/add", methods=["GET", "POST"])
@login_required
def credit_add_page():
    form = CreditForm()

    # Get and populate dropdown list with categories
    categories = (
        CategoryModel.query.filter(
            (
                (CategoryModel.user_id == current_user.id)
                | (CategoryModel.user_id == None)
            )
            & (CategoryModel.type == "Credit")
        )
        .order_by(CategoryModel.name)
        .all()
    )
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():

        # Create credit
        credit = CreditModel(
            amount=form.amount.data,  # type: ignore
            date=form.date.data,  # type: ignore
            description=form.description.data,  # type: ignore
            category_id=form.category_id.data,  # type: ignore
            notes=form.notes.data,  # type: ignore
            user_id=current_user.id,  # type: ignore
        )

        # Add to db
        try:
            db.session.add(credit)
            db.session.commit()
            flash("Credit added successfully!", "success")
            return redirect(url_for("credits.credit_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while adding credit. Please try again.", "danger")
            logging.error(f"Database error when adding credit: {e}")

    return render_template("credits/form.html", form=form, title="Add Credit")


# Edit credit
@bp.route("/credits/edit/<int:id>", methods=["GET", "POST"])
@login_required
def credit_edit_page(id):
    credit = CreditModel.query.get_or_404(id)

    # Prevent editing other user's credits
    if credit.user_id and credit.user_id != current_user.id:
        flash("You don't have permissions to edit this credit.", "danger")
        return redirect(url_for("credits.credit_list_page"))

    # Create form with pre-populated form data and update on validation
    form = CreditForm(obj=credit)

    if form.validate_on_submit():
        credit.amount = form.amount.data
        credit.date = form.date.data
        credit.description = form.description.data
        credit.notes = form.notes.data

        # Add to db
        try:
            db.session.commit()
            flash("Credit updated successfully!", "success")
            return redirect(url_for("credits.credit_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while editing credit. Please try again.", "danger")
            logging.error(f"Database error editing credit: {e}")

    return render_template(
        "credits/form.html", form=form, title="Editing Credit", credit=credit
    )


# Delete credit
@bp.route("/credits/delete/<int:id>", methods=["POST"])
@login_required
def credit_delete_page(id):
    credit = CreditModel.query.get_or_404(id)

    # Prevent deleting other user's credit
    if credit.user_id and credit.user_id != current_user.id:
        flash("You don't have permissions to delete this credit.", "danger")
        return redirect(url_for("credits.credit_list_page"))

    # Delete credit
    try:
        db.session.delete(credit)
        db.session.commit()
        flash("Credit deleted.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error while deleting credit. Please try again.", "danger")
        logging.error(f"Database error while deleting credit: {e}")

    return redirect(url_for("credits.credit_list_page"))
