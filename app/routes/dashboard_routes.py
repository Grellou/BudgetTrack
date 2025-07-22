from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app import db
from app.models.income_model import IncomeModel
from app.models.expense_model import ExpenseModel
from sqlalchemy import func

bp = Blueprint("dashboard", __name__)

# Display calculations
@bp.route("/dashboard")
@login_required
def dashboard_page():

    user_income_total = db.session.query(func.sum(IncomeModel.amount)).filter_by(user_id=current_user.id).scalar() or 0
    user_expense_total = db.session.query(func.sum(ExpenseModel.amount)).filter_by(user_id=current_user.id).scalar() or 0
    remaining_budget = user_income_total - user_expense_total 
    income_transactions = IncomeModel.query.all()
    expense_transactions = ExpenseModel.query.all()
    recent_transactions = income_transactions + expense_transactions

    dashboard_data = {
        "summary": {
            "total_incomes": user_income_total,
            "total_expenses": user_expense_total,
            "remaining": remaining_budget
        },
        "recent_transactions": recent_transactions
    }

    return render_template("dashboard/dashboard.html", data=dashboard_data)
