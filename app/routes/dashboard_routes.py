import json
from datetime import datetime

import plotly
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models.credit_model import CreditModel
from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel
from app.utils.filters import model_filter
from app.utils.visualizations import expense_category_chart

bp = Blueprint("dashboard", __name__)


# Dashboard
@bp.route("/dashboard")
@login_required
def dashboard_page():

    # Read date parameters from request
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")
    start_date = _parse_date(start_str)
    end_date = _parse_date(end_str)

    # Income queries
    income_filters = model_filter(IncomeModel, current_user.id, start_date, end_date)
    user_income_total = (
        db.session.query(func.sum(IncomeModel.amount)).filter(*income_filters).scalar()
        or 0
    )

    # Expense queries
    expense_filters = model_filter(ExpenseModel, current_user.id, start_date, end_date)
    user_expense_total = (
        db.session.query(func.sum(ExpenseModel.amount))
        .filter(*expense_filters)
        .scalar()
        or 0
    )

    # Credit queries
    credit_filters = model_filter(CreditModel, current_user.id, start_date, end_date)
    user_credit_total = (
        db.session.query(func.sum(CreditModel.amount)).filter(*credit_filters).scalar()
        or 0
    )

    # Calculations
    income_transactions = IncomeModel.query.filter(*income_filters).all()
    expense_transactions = ExpenseModel.query.filter(*expense_filters).all()
    recent_transactions = income_transactions + expense_transactions
    recent_transactions.sort(key=lambda t: t.date, reverse=True)

    # Data dict
    dashboard_data = {
        "summary": {
            "total_incomes": user_income_total,
            "total_expenses": user_expense_total,
            "total_credits": user_credit_total,
            "remaining": user_income_total - user_expense_total,
        },
        "recent_transactions": recent_transactions,
    }

    # Date values back to form fields dict
    filters = {"start_date": start_str or "", "end_date": end_str or ""}

    # Graph implementation
    x = ["Feb", "Mar", "May"]
    y = ["20", "30", "10"]
    fig = expense_category_chart(x, y)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "dashboard/dashboard.html",
        data=dashboard_data,
        start=start_str,
        end=end_str,
        filters=filters,
        graphJSON=graphJSON,
    )


# Convert string into date object
def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
