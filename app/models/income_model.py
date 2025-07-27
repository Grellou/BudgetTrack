from datetime import datetime

from app import db


class IncomeModel(db.Model):
    __tablename__ = "incomes"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    description = db.Column(db.String(128))
    type = db.Column(db.String(), default="income")
    notes = db.Column(db.Text)

    # Foreign Key
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship
    category = db.relationship(
        "CategoryModel", backref=db.backref("incomes", lazy="dynamic")
    )
    user = db.relationship("UserModel", backref=db.backref("incomes", lazy="dynamic"))

    # For debugging
    def __repr__(self):
        return f"<Income {self.id}: ${self.amount} on {self.date}>"

    # Format amount
    @property
    def formatted_amount(self):
        return f"${float(self.amount):,.2f}"

    # Format date
    @property
    def formatted_date(self):
        return self.date.strftime("%b %d, %Y")
