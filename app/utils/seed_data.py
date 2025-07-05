from app import db
from app.models.category_model import CategoryModel

# Add default expense categories to db
def seed_default_categories(user_id = None):

    default_categories = [
        {"name": "Housing", "is_essential": True, "description": "Rent, mortgage, repairs"},
        {"name": "Utilities", "is_essential": True, "description": "Electricity, water, internet"},
        {"name": "Groceries", "is_essential": True, "description": "Food and household items"},
        {"name": "Transportation", "is_essential": True, "description": "Public transit, gas, car maintenance"},
        {"name": "Healthcare", "is_essential": True, "description": "Medications, doctor visits"},
        {"name": "Entertainment", "is_essential": False, "description": "Movies, concerts, subscriptions"},
        {"name": "Shopping", "is_essential": False, "description": "Clothes, electronics, home goods"},
        {"name": "Personal care", "is_essential": False, "description": "Haircut, gym, cosmetics"},
        {"name": "Travel", "is_essential": False, "description": "Vacations, trips, hotels"}
    ]

    categories_added = 0

    for category_data in default_categories:
        # Check if category already exists
        existing_category = CategoryModel.query.filter_by(name=category_data["name"]).first()
        if not existing_category:
            category = CategoryModel(name=category_data["name"], description=category_data["description"], is_essential=category_data["is_essential"], user_id=user_id) # type: ignore
            db.session.add(category)
            categories_added += 1

    if categories_added > 0:
        db.session.commit()
        print(f"{categories_added} default categories added successfully!")
    else:
        print("No new categories added.")

    return categories_added
