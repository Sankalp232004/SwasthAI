#!/usr/bin/env python3
"""
Create / update the superadmin user.
Usage: python -m scripts.setup.create_superadmin
"""

from app import create_app, db
from models import SuperAdmin
from werkzeug.security import generate_password_hash

import os
app = create_app('production' if os.environ.get('FLASK_ENV') == 'production' else 'development')

APP_BASE_URL = os.environ.get('APP_BASE_URL', 'https://swasthai.roadto405.xyz').rstrip('/')

ADMIN_EMAIL    = 'swasthai.admin@system.com'
ADMIN_PASSWORD = 'Sw@sth1#2026'
ADMIN_NAME     = 'System Administrator'

with app.app_context():
    # Look up by either the new or the old email (handles first-time migration)
    admin = (
        SuperAdmin.query.filter_by(email=ADMIN_EMAIL).first() or
        SuperAdmin.query.filter_by(email='admin@swasthai.com').first()
    )

    if not admin:
        admin = SuperAdmin(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            is_super=True,
            is_active=True,
            permissions={
                'manage_clinics': True,
                'manage_patients': True,
                'manage_doctors': True,
                'view_analytics': True,
                'system_settings': True
            }
        )
        db.session.add(admin)
        db.session.commit()
        print("\n  ✓ Superadmin created")
    else:
        # Always keep email and password in sync with this file
        admin.email         = ADMIN_EMAIL
        admin.name          = ADMIN_NAME
        admin.password_hash = generate_password_hash(ADMIN_PASSWORD)
        db.session.commit()
        print("\n  ✓ Superadmin credentials updated")

    print(f"  Email:    {ADMIN_EMAIL}")
    print(f"  Login:    {APP_BASE_URL}/superadmin/login\n")
