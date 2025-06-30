import os
from app import db, create_app

app = create_app(os.environ.get("FLASK_CONFIG", "Development"))

if __name__ == "__main__":
    app.run()
