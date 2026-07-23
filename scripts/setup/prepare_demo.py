#!/usr/bin/env python3
"""Prepare idempotent sample data for client-facing demos.

Usage:
    python -m scripts.setup.prepare_demo

Environment variables:
    DEMO_BASE_URL         Optional public app URL for printed links.
    DEMO_SUPERADMIN_EMAIL Optional superadmin email.
    DEMO_SUPERADMIN_PASSWORD Optional superadmin password.
"""

from datetime import date, datetime, time, timedelta
import os
from typing import Optional

from app import create_app, db
from models import (
    Appointment,
    Clinic,
    ClinicHours,
    Doctor,
    Patient,
    SlotConfiguration,
    SuperAdmin,
)


APP_CONFIG = "production" if os.environ.get("FLASK_ENV") == "production" else "development"
app = create_app(APP_CONFIG)


def upsert_superadmin() -> SuperAdmin:
    email = os.environ.get("DEMO_SUPERADMIN_EMAIL", "swasthai.admin@system.com").strip()
    password = os.environ.get("DEMO_SUPERADMIN_PASSWORD", "Sw@sth1#2026")

    admin = SuperAdmin.query.filter_by(email=email).first()
    if not admin:
        admin = SuperAdmin(
            name="System Administrator",
            email=email,
            is_super=True,
            is_active=True,
            permissions={
                "manage_clinics": True,
                "manage_patients": True,
                "manage_doctors": True,
                "view_analytics": True,
                "system_settings": True,
            },
        )
        db.session.add(admin)

    admin.name = "System Administrator"
    admin.is_super = True
    admin.is_active = True
    admin.set_password(password)
    return admin


def upsert_clinic() -> Clinic:
    clinic = Clinic.query.filter_by(slug="sample-clinic").first()
    if not clinic:
        clinic = Clinic(slug="sample-clinic")
        db.session.add(clinic)

    clinic.name = "Sample Medical Clinic"
    clinic.email = "admin@clinic.com"
    clinic.phone = "+919876543210"
    clinic.address = "123 Medical Plaza, Healthcare District, Mumbai"
    clinic.latitude = 19.0760
    clinic.longitude = 72.8777
    clinic.is_active = True
    clinic.subscription_status = "active"
    clinic.subscription_expiry = datetime.utcnow() + timedelta(days=365)
    clinic.max_doctors = 10
    clinic.max_patients_per_day = 200
    clinic.features = {
        "otp_verification": True,
        "multi_language": True,
        "analytics": True,
        "appointment_scheduling": True,
    }
    return clinic


def upsert_doctor(clinic_id: int, email: str, name: str, password: str, specialization: str) -> Doctor:
    doctor = Doctor.query.filter_by(email=email).first()
    if not doctor:
        doctor = Doctor(email=email)
        db.session.add(doctor)

    doctor.clinic_id = clinic_id
    doctor.name = name
    doctor.phone = "+919999999999"
    doctor.specialization = specialization
    doctor.is_active = True
    doctor.set_password(password)
    return doctor


def upsert_slot_and_hours(clinic: Clinic, doctor: Doctor) -> None:
    slot = SlotConfiguration.query.filter_by(doctor_id=doctor.id).first()
    if not slot:
        slot = SlotConfiguration(clinic_id=clinic.id, doctor_id=doctor.id)
        db.session.add(slot)

    slot.clinic_id = clinic.id
    slot.slot_duration_minutes = 30
    slot.slots_per_batch = 4
    slot.buffer_between_batches = 5
    slot.walkin_slots_per_batch = 1
    slot.appointment_slots_per_batch = 3
    slot.max_advance_days = 30
    slot.allow_same_day_booking = True
    slot.is_active = True

    # Ensure weekday working hours exist for a clean demo schedule.
    for dow in range(0, 5):
        hours = ClinicHours.query.filter_by(clinic_id=clinic.id, doctor_id=doctor.id, day_of_week=dow).first()
        if not hours:
            hours = ClinicHours(clinic_id=clinic.id, doctor_id=doctor.id, day_of_week=dow)
            db.session.add(hours)
        hours.start_time = time(9, 0)
        hours.end_time = time(14, 0)
        hours.patients_per_hour = 8
        hours.is_active = True


def upsert_patient(
    clinic_id: int,
    doctor_id: int,
    name: str,
    phone: str,
    age: int,
    gender: str,
    complaint: str,
    priority: str,
    status: str,
) -> Patient:
    patient = Patient.query.filter_by(clinic_id=clinic_id, phone=phone).first()
    if not patient:
        patient = Patient(clinic_id=clinic_id, phone=phone)
        db.session.add(patient)

    patient.doctor_id = doctor_id
    patient.name = name
    patient.age = age
    patient.gender = gender
    patient.complaint = complaint
    patient.priority = priority
    patient.status = status
    patient.phone_verified = True
    patient.visit_count = max(patient.visit_count or 1, 1)
    patient.last_visit = datetime.utcnow()
    patient.clinical_data = {
        "inputs": {
            "heart_rate": 88,
            "systolic_bp": 122,
            "diastolic_bp": 82,
            "respiratory_rate": 18,
            "temperature": 37.1,
            "consciousness_level": "ALERT",
            "pain_level": 4,
            "pain_location": "General",
            "chest_pain": False,
            "difficulty_breathing": False,
            "bleeding_severity": "NONE",
            "symptom_duration_hours": 8,
            "is_pregnant": False,
            "has_diabetes": False,
            "has_heart_condition": False,
        },
        "triage_result": {"priority": priority, "reasons": ["Demo sample case"]},
        "red_flags": [],
        "engine_version": "1.0.0",
        "override_history": [],
        "visit_history": [],
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return patient


def upsert_appointment(
    clinic_id: int,
    patient_id: int,
    doctor_id: int,
    appointment_date: date,
    slot_start: time,
    slot_end: time,
    status: str,
    reason: str,
    triage_priority: Optional[str] = None,
) -> Appointment:
    appt = Appointment.query.filter_by(
        clinic_id=clinic_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        slot_start_time=slot_start,
    ).first()

    if not appt:
        appt = Appointment(
            clinic_id=clinic_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            slot_start_time=slot_start,
            slot_end_time=slot_end,
        )
        db.session.add(appt)

    appt.slot_end_time = slot_end
    appt.status = status
    appt.reason = reason
    appt.batch_number = 1
    appt.triage_priority = triage_priority
    if triage_priority:
        appt.triage_completed = True
        appt.triage_completed_at = datetime.utcnow()
    return appt


def main() -> None:
    base_url = os.environ.get("DEMO_BASE_URL", "https://swasthai-2tv5.onrender.com").rstrip("/")

    with app.app_context():
        admin = upsert_superadmin()
        clinic = upsert_clinic()
        db.session.flush()

        doctor_primary = upsert_doctor(
            clinic_id=clinic.id,
            email="admin@clinic.com",
            name="Dr. Admin",
            password="admin123",
            specialization="General Medicine",
        )
        doctor_secondary = upsert_doctor(
            clinic_id=clinic.id,
            email="dr.rana@clinic.com",
            name="Dr. Neha Rana",
            password="rana123",
            specialization="Internal Medicine",
        )

        db.session.flush()

        upsert_slot_and_hours(clinic, doctor_primary)
        upsert_slot_and_hours(clinic, doctor_secondary)

        p1 = upsert_patient(
            clinic_id=clinic.id,
            doctor_id=doctor_primary.id,
            name="Rahul Sharma",
            phone="9000001001",
            age=34,
            gender="Male",
            complaint="Fever and sore throat",
            priority="AMBER",
            status="Waiting",
        )
        p2 = upsert_patient(
            clinic_id=clinic.id,
            doctor_id=doctor_primary.id,
            name="Meera Patil",
            phone="9000001002",
            age=58,
            gender="Female",
            complaint="Chest discomfort",
            priority="RED",
            status="Consulting",
        )
        p3 = upsert_patient(
            clinic_id=clinic.id,
            doctor_id=doctor_secondary.id,
            name="Arjun Verma",
            phone="9000001003",
            age=22,
            gender="Male",
            complaint="Seasonal cold",
            priority="GREEN",
            status="Completed",
        )

        db.session.flush()

        today = date.today()
        tomorrow = today + timedelta(days=1)

        upsert_appointment(
            clinic_id=clinic.id,
            patient_id=p1.id,
            doctor_id=doctor_primary.id,
            appointment_date=today,
            slot_start=time(10, 0),
            slot_end=time(10, 30),
            status="scheduled",
            reason="Follow-up for fever",
            triage_priority="AMBER",
        )
        upsert_appointment(
            clinic_id=clinic.id,
            patient_id=p2.id,
            doctor_id=doctor_primary.id,
            appointment_date=today,
            slot_start=time(11, 0),
            slot_end=time(11, 30),
            status="consulting",
            reason="Urgent chest pain review",
            triage_priority="RED",
        )
        upsert_appointment(
            clinic_id=clinic.id,
            patient_id=p3.id,
            doctor_id=doctor_secondary.id,
            appointment_date=tomorrow,
            slot_start=time(12, 0),
            slot_end=time(12, 30),
            status="scheduled",
            reason="General consultation",
            triage_priority="GREEN",
        )

        db.session.commit()

        print("\n" + "=" * 68)
        print(" Demo dataset is ready")
        print("=" * 68)
        print(f"Public Landing:   {base_url}/")
        print(f"Patient Journey:  {base_url}/c/sample-clinic")
        print(f"Doctor Login:     {base_url}/doctor/login")
        print(f"Admin Login:      {base_url}/superadmin/login")
        print("\nCredentials")
        print(f"- Superadmin: {admin.email} / {os.environ.get('DEMO_SUPERADMIN_PASSWORD', 'Sw@sth1#2026')}")
        print("- Doctor 1:   admin@clinic.com / admin123")
        print("- Doctor 2:   dr.rana@clinic.com / rana123")
        print("\nSample Patient Phones")
        print("- 9000001001")
        print("- 9000001002")
        print("- 9000001003")
        print("=" * 68 + "\n")


if __name__ == "__main__":
    main()