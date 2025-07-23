from app import db

class CreditModel(db.Model):
    __tablename__ = "credits"
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(128))
    notes = db.Column(db.Text)
    
