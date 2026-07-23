#!/usr/bin/env python3
"""
Create Sample Clinic and Doctor for Initial Setup
"""

from app import create_app, db
from models import Clinic, Doctor
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

import os
app = create_app('production' if os.environ.get('FLASK_ENV') == 'production' else 'development')
APP_BASE_URL = os.environ.get('APP_BASE_URL', 'https://swasthai-2tv5.onrender.com').rstrip('/')

with app.app_context():
    # Create Sample Clinic
    sample_clinic = Clinic.query.filter_by(slug='sample-clinic').first()
    
    if not sample_clinic:
        sample_clinic = Clinic(
            name='Sample Medical Clinic',
            slug='sample-clinic',
            email='admin@clinic.com',
            phone='+919876543210',
            address='123 Medical Plaza, Healthcare District, Mumbai, Maharashtra 400001',
            is_active=True,
            subscription_status='active',
            subscription_expiry=datetime.utcnow() + timedelta(days=365),
            max_doctors=10,
            max_patients_per_day=200,
            features={
                'otp_verification': True,
                'multi_language': True,
                'analytics': True,
                'appointment_scheduling': False
            }
        )
        db.session.add(sample_clinic)
        db.session.commit()
        
        print("\n" + "="*60)
        print("  ✓ Sample Clinic Created!")
        print("="*60)
        print(f"\n  Clinic Name:    {sample_clinic.name}")
        print(f"  Clinic Slug:    {sample_clinic.slug}")
        print(f"  Registration:   {APP_BASE_URL}/c/{sample_clinic.slug}/register")
        print(f"  Status:         {sample_clinic.subscription_status}")
        print("\n" + "="*60 + "\n")
    else:
        print("\n✓ Sample clinic already exists: sample-clinic\n")
    
    # Create Doctor linked to the clinic
    sample_doctor = Doctor.query.filter_by(email='admin@clinic.com').first()
    
    if not sample_doctor:
        sample_doctor = Doctor(
            clinic_id=sample_clinic.id,
            name='Dr. Admin',
            email='admin@clinic.com',
            password_hash=generate_password_hash('admin123'),
            phone='+919876543210',
            specialization='General Medicine',
            is_active=True
        )
        db.session.add(sample_doctor)
        db.session.commit()
        
        print("  ✓ Doctor Created and Linked to Clinic")
        print(f"  Doctor Email:   {sample_doctor.email}")
        print(f"  Password:       admin123")
        print(f"  Login URL:      {APP_BASE_URL}/doctor/login")
        print("\n" + "="*60 + "\n")
    else:
        print("  ✓ Doctor already exists\n")

