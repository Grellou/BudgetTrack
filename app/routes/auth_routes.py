import logging

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.forms.auth_forms import (
    LoginForm,
    PasswordResetConfirmForm,
    PasswordResetForm,
    RegisterForm,
)
from app.models.user_model import UserModel
from app.utils.mail import send_password_reset_email

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


# Password reset request
@bp.route("/password_reset", methods=["GET", "POST"])
def password_reset_page():

    # Redirect if user already logged in
    if current_user.is_authenticated:
        flash(
            "Already logged in! You can change your password in user settings.",
            "info",
        )
        return redirect(url_for("navigation.home_page"))

    # Handle password reset form
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email_address=form.email_address.data).first()

        # Redirect and display message if email is invalid
        if not user:
            flash("Account with such email address not found!", "danger")
            return redirect(url_for("auth.password_reset_page"))

        # Send email with password reset URL
        if user:
            send_password_reset_email(user)
            flash(
                "Password reset instructions were sent to your email address.",
                "success",
            )

    return render_template("auth/password_reset.html", form=form)


# Password reset confirmation
@bp.route("/password_reset/<token>/<int:user_id>", methods=["GET", "POST"])
def password_reset_confirm_page(token, user_id):
    # Redirect if user already logged in
    if current_user.is_authenticated:
        flash(
            "Already logged in! You can change your password in user settings.",
            "info",
        )
        return redirect(url_for("navigation.home_page"))

    # Check if reset token is valid
    user = UserModel.validate_reset_password_token(token, user_id)

    # Redirect and display error if use not found
    if not user:
        flash("Error: Account not found.", "danger")
        return redirect(url_for("navigation.home_page"))

    # Handle password change form
    form = PasswordResetConfirmForm()
    if form.validate_on_submit():
        user.set_password(form.password1.data)
        db.session.commit()
        flash("Password has been changed successfully!", "success")
        return redirect(url_for("navigation.home_page"))

    return render_template(
        "auth/password_reset_confirm.html", form=form, token=token, user_id=user_id
    )


# Logout
@bp.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out succesfully.", "info")
    return redirect(url_for("navigation.home_page"))
