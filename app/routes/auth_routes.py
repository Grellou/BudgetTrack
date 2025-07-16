from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models.user_model import UserModel
from sqlalchemy.exc import SQLAlchemyError
from app import db
import logging

bp = Blueprint("auth", __name__)


# Register new account
@bp.route("/register", methods=["GET", "POST"])
def register_page():
    # Redirect if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for("navigation.home_page"))

    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user
        user = UserModel(
            username=form.username.data,  # type: ignore
            email_address=form.email_address.data,  # type: ignore
        )
        user.set_password(form.password1.data)

        # Add to db
        try:
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login_page"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "danger")
            logging.error(f"Database error during registration: {e}")

    return render_template("auth/register.html", form=form)


# Login with email address and password
@bp.route("/login", methods=["GET", "POST"])
def login_page():
    # Redirect if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for("navigation.home_page"))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email_address=form.email_address.data).first()
        # Check if login detail matches
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login succesful!", "success")
            return redirect(url_for("navigation.home_page"))
        else:
            flash("Invalid email address or password.", "danger")

    return render_template("auth/login.html", form=form)


# Logout
@bp.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out succesfully.", "info")
    return redirect(url_for("navigation.home_page"))
