# init_db.py

import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# ✅ Load Flask app
app = create_app()

# ✅ Secure environment fallback
DEFAULT_ADMIN_USERNAME = "secure_admin2"
DEFAULT_ADMIN_PASSWORD = "ChangeThis@123!"

# ✅ Get credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)

with app.app_context():
    db.create_all()

    # ✅ Avoid duplicate admin
    existing_user = User.query.filter_by(username=ADMIN_USERNAME).first()
    if existing_user:
        print(f"ℹ️ Admin user '{ADMIN_USERNAME}' already exists. Skipping creation.")
    else:
        # ✅ Securely hash the password
        hashed_password = generate_password_hash(ADMIN_PASSWORD, method='pbkdf2:sha256', salt_length=16)
        admin = User(username=ADMIN_USERNAME, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin user '{ADMIN_USERNAME}' created successfully.")
