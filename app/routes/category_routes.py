from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.models.category_model import CategoryModel
from app.forms.category_forms import CategoryForm
from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging

bp = Blueprint("categories", __name__)

# Display list of available categories
@bp.route("/categories/list")
@login_required
def category_list_page():
    categories = CategoryModel.query.all()
    return render_template("categories/list.html", categories=categories)

# Create new category
@bp.route("/categories/add", methods=["GET", "POST"])
@login_required
def category_add_page():
    form = CategoryForm()
    if form.validate_on_submit():
        
        # Create category
        category = CategoryModel(
            name=form.name.data, # type: ignore
            description=form.description.data, # type: ignore
            is_essential=form.is_essential.data, # type: ignore
            user_id=current_user.id # type: ignore
        )
        
        # Add to db
        try:
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully!", "success")
            return redirect(url_for("categories.category_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error creating category. Please try again.", "danger")
            logging.error(f"Database error during category creation: {e}")

    return render_template("categories/form.html", form=form)

# Edit category
@bp.route("/categories/edit/<int:id>", methods=["GET", "POST"])
@login_required
def category_edit_page(id):
    category = CategoryModel.query.get_or_404(id)

    # Prevent editing other user's category
    if category.user_id and category.user_id != current_user.id:
        flash("You don't have permissions to edit this category.", "danger")
        return redirect(url_for("categories.category_list_page"))

    # Create form with pre-populated form data and update on validation
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.is_essential = form.is_essential.data

        # Add to db
        try:
            db.session.commit()
            flash("Category updated successfully!", "success")
            return redirect(url_for("categories.category_list_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error while updating category. Please try again.", "danger")
            logging.error(f"Database error during category editing: {e}")

    return render_template("categories/form.html", form=form, title="Edit Category", category=category)

# Delete category
@bp.route("/categories/delete/<int:id>", methods=["POST"])
@login_required
def category_delete_page(id):
    category = CategoryModel.query.get_or_404(id)

    # Prevent deleting other user's category
    if category.user_id and category.user_id != current_user.id:
        flash("You don't have permissions to delete this category.", "danger")
        return redirect(url_for("categories.category_list_page"))

    # Delete category
    try:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error while deleting category. Please try again.", "danger")
        logging.error(f"Database error during category deletion: {e}")

    return redirect(url_for("categories.category_list_page"))
