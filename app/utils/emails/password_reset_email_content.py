password_reset_email_html_content = """
<p>Hello,</p>
<p>You are receiving this email because password reset has been requested for your account.</p>
<p>
    To reset your password
    <a href="{{ password_reset_url }}">click here</a>
</p>
<p>
    Alternatively, you can paste the following link into your browser: <br>
    {{ password_reset_url }}
</p>
<p>If you have not requested a password reset you can ignore this email.</p>
"""
