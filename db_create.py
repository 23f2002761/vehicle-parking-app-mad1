from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    existing_admin=User.query.filter_by(username="admin").first()
    if not existing_admin:
        admin=User(
            full_name="Admin",
            username="admin",
            email="admin@mail.com",
            password=generate_password_hash("admin@123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin is created")
    print("The table are created in the database")
