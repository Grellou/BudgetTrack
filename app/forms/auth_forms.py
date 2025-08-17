from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.user_model import UserModel


# Registration form
class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=64)]
    )
    email_address = StringField(
        "Email address", validators=[DataRequired(), Email(), Length(max=128)]
    )
    password1 = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    password2 = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Register")

    # Check if username or email exists
    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken.")

    def validate_email_address(self, email_address):
        user = UserModel.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError("Email address already registered.")


# Login form
class LoginForm(FlaskForm):
    email_address = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


# Password reset form
class PasswordResetForm(FlaskForm):
    email_address = StringField("Email address", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset")


# Password reset confirmation form
class PasswordResetConfirmForm(FlaskForm):
    password1 = PasswordField(
        "Create new password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    password2 = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Confirm password reset")
