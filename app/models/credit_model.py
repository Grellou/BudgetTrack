from datetime import datetime

from app import db


class CreditModel(db.Model):
    __tablename__ = "credits"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    description = db.Column(db.String(128))
    type = db.Column(db.String(), default="credit")
    notes = db.Column(db.Text)

    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    category = db.relationship(
        "CategoryModel", backref=db.backref("credits", lazy="dynamic")
    )
    user = db.relationship("UserModel", backref=db.backref("credits", lazy="dynamic"))

    # For debugging
    def __repr__(self):
        return f"<Credit {self.id}: ${self.amount}>"

    # Format amount
    @property
    def formatted_amount(self):
        return f"${float(self.amount):,.2f}"

    # Format date
    @property
    def formatted_date(self):
        return self.date.strftime("%b %d, %Y")
