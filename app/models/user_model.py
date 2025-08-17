from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app import bcrypt, db, login_manager


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email_address = db.Column(db.String(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Prevent password from being accessed
    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    # Set password hash
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Check if password matches
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # For debugging
    def __repr__(self):
        return f"<User {self.username}>"

    # Generate token for password reset request
    def generate_password_reset_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(self.email_address, salt=self.password_hash)

    # Check if token is valid and return user
    @staticmethod
    def validate_reset_password_token(token, user_id):
        user = db.session.get(UserModel, user_id)
        if not user:
            return None

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config["RESET_PASS_TOKEN_MAX_AGE"],
                salt=user.password_hash,
            )
        except (BadSignature, SignatureExpired):
            return None

        if token_user_email != user.email_address:
            return None

        return user


# User loader
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
