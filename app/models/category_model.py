from datetime import datetime
from app import db

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    type = db.Column(db.String(64))
    description = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # For debugging
    def __repr__(self):
        return f"<Category {self.name}>"
