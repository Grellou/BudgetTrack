import json
from datetime import datetime

import plotly
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models.category_model import CategoryModel
from app.models.credit_model import CreditModel
from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel
from app.utils.filters import model_filter
from app.utils.visualizations import (
    expense_category_chart,
    income_category_chart,
    income_vs_expense_chart,
)

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
    income_per_category = (
        db.session.query(CategoryModel.name, func.sum(IncomeModel.amount))
        .join(CategoryModel, IncomeModel.category_id == CategoryModel.id)
        .filter(*income_filters)
        .group_by(CategoryModel.name)
        .all()
    )
    income_category_names = [name for name, _ in income_per_category]
    income_category_values = [amount for _, amount in income_per_category]

    # Expense queries
    expense_filters = model_filter(ExpenseModel, current_user.id, start_date, end_date)
    user_expense_total = (
        db.session.query(func.sum(ExpenseModel.amount))
        .filter(*expense_filters)
        .scalar()
        or 0
    )
    expenses_per_category = (
        db.session.query(CategoryModel.name, func.sum(ExpenseModel.amount))
        .join(CategoryModel, ExpenseModel.category_id == CategoryModel.id)
        .filter(*expense_filters)
        .group_by(CategoryModel.name)
        .all()
    )
    expense_category_names = [name for name, _ in expenses_per_category]
    expense_category_values = [amount for _, amount in expenses_per_category]

    # Credit queries
    credit_filters = model_filter(CreditModel, current_user.id, start_date, end_date)
    user_credit_total = (
        db.session.query(func.sum(CreditModel.amount)).filter(*credit_filters).scalar()
        or 0
    )

    # Recent transactions calcs
    income_transactions = IncomeModel.query.filter(*income_filters).all()
    expense_transactions = ExpenseModel.query.filter(*expense_filters).all()
    credit_transactions = CreditModel.query.filter(*credit_filters).all()
    recent_transactions = (
        income_transactions + expense_transactions + credit_transactions
    )
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

    # Expense category graph
    expense_fig = expense_category_chart(
        expense_category_names, expense_category_values
    )
    expense_category_chart_JSON = json.dumps(
        expense_fig, cls=plotly.utils.PlotlyJSONEncoder
    )

    # Income category graph
    income_fig = income_category_chart(income_category_names, income_category_values)
    income_category_chart_JSON = json.dumps(
        income_fig, cls=plotly.utils.PlotlyJSONEncoder
    )

    # Income vs expense graph
    income_vs_expense_names = ["Income", "Expense"]
    income_vs_expense_total_income = dashboard_data["summary"]["total_incomes"]
    income_vs_expense_total_expenses = dashboard_data["summary"]["total_expenses"]
    income_vs_expense_values = [
        income_vs_expense_total_income,
        income_vs_expense_total_expenses,
    ]
    income_vs_expense_fig = income_vs_expense_chart(
        income_vs_expense_names, income_vs_expense_values
    )
    income_vs_expense_chart_JSON = json.dumps(
        income_vs_expense_fig, cls=plotly.utils.PlotlyJSONEncoder
    )

    return render_template(
        "dashboard/dashboard.html",
        data=dashboard_data,
        start=start_str,
        end=end_str,
        filters=filters,
        expense_category_chart_JSON=expense_category_chart_JSON,
        income_category_chart_JSON=income_category_chart_JSON,
        income_vs_expense_chart_JSON=income_vs_expense_chart_JSON,
    )


# Convert string into date object
def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
