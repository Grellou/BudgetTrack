# Always filter by logged in user. Optionally filter by dates
def model_filter(Model, user_id, start_date=None, end_date=None):
    conds = [Model.user_id == user_id]
    if start_date is not None:
        conds.append(Model.date >= start_date)
    if end_date is not None:
        conds.append(Model.date <= end_date)
    return conds
