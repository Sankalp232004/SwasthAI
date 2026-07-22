#!/usr/bin/env python3
"""
Initialize Database - Create all tables from models
Run this once to set up the database schema
"""

from app import create_app, db
from models import (
    Clinic, Patient, Doctor, SuperAdmin, 
    OTPRecord, RegistrationToken, ClinicHours, 
    SlotConfiguration, Appointment, AuditLog, SystemSetting
)

import os
app = create_app('production' if os.environ.get('FLASK_ENV') == 'production' else 'development')

with app.app_context():
    print("\n" + "="*60)
    print("  Initializing Database Schema")
    print("="*60 + "\n")
    
    # Create all tables from models (no-op if they already exist — data is preserved)
    print("  Creating tables (skipping any that already exist)...")
    db.create_all()
    
    # ── Safe column migrations (ADD COLUMN IF NOT EXISTS) ─────────────
    # These are idempotent: safe to run on existing databases.
    from sqlalchemy import text, inspect as sa_inspect
    try:
        inspector = sa_inspect(db.engine)
        patient_cols = [c['name'] for c in inspector.get_columns('patients')]
        if 'doctor_id' not in patient_cols:
            with db.engine.connect() as conn:
                conn.execute(text(
                    'ALTER TABLE patients ADD COLUMN doctor_id INTEGER REFERENCES doctors(id)'
                ))
                conn.commit()
            print("  ✓ Added doctor_id column to patients table")
        else:
            print("  ✓ patients.doctor_id already exists — skipping")

        clinic_cols = [c['name'] for c in inspector.get_columns('clinics')]
        with db.engine.connect() as conn:
            if 'latitude' not in clinic_cols:
                conn.execute(text('ALTER TABLE clinics ADD COLUMN latitude DOUBLE PRECISION'))
                print("  ✓ Added latitude column to clinics table")
            else:
                print("  ✓ clinics.latitude already exists — skipping")

            if 'longitude' not in clinic_cols:
                conn.execute(text('ALTER TABLE clinics ADD COLUMN longitude DOUBLE PRECISION'))
                print("  ✓ Added longitude column to clinics table")
            else:
                print("  ✓ clinics.longitude already exists — skipping")

            conn.commit()
    except Exception as e:
        print(f"  ! Migration note: {e}")

    # Keep stored base_url in sync with current production URL defaults.
    default_base_url = (app.config.get('APP_BASE_URL') or '').strip().rstrip('/')
    stored_base_url = (SystemSetting.get('base_url') or '').strip().rstrip('/')
    legacy_base_url = 'https://bedrockcrm-med-production.up.railway.app'

    if stored_base_url == legacy_base_url and default_base_url:
        SystemSetting.set('base_url', default_base_url)
        print(f"  ✓ Migrated system base_url: {legacy_base_url} -> {default_base_url}")
    elif default_base_url and not stored_base_url:
        SystemSetting.set('base_url', default_base_url)
        print(f"  ✓ Seeded system base_url: {default_base_url}")
    elif stored_base_url:
        print("  ✓ system_settings.base_url already configured - skipping")

    print("\n  ✓ Database schema initialized successfully!")
    print("\n" + "="*60)
    print("  Next steps:")
    print("  1. Run: python -m scripts.setup.create_superadmin (to create superadmin)")
    print("  2. Run: python -m scripts.setup.create_clinic (to create sample clinic)")
    print("="*60 + "\n")
