from flask import render_template_string, url_for
from flask_mailman import EmailMessage

from app.utils.emails.password_reset_email_content import (
    password_reset_email_html_content,
)


# Send email with password reset url to user's email address
def send_password_reset_email(user):
    password_reset_url = url_for(
        "auth.password_reset_confirm_page",
        token=user.generate_password_reset_token(),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        password_reset_email_html_content, password_reset_url=password_reset_url
    )

    message = EmailMessage(
        subject="BudgetTrack - Password Reset", body=email_body, to=[user.email_address]
    )
    message.content_subtype = "html"

    message.send()
