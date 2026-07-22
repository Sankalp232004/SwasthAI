"""
Patient Routes
Handles patient-facing pages and submissions.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app import db
from models import Clinic

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/')
def index():
    """Landing page - Clinic selector or info page."""
    return render_template('index.html')


# ==================== CLINIC-SPECIFIC ROUTES ====================

@patient_bp.route('/c/<slug>')
def clinic_landing(slug):
    """Clinic-specific landing page accessed via QR code."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    if not clinic.is_active:
        return render_template('clinic_inactive.html', clinic=clinic), 403
    
    # Store clinic context in session
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    session['clinic_name'] = clinic.name
    
    return render_template('clinic_landing.html', clinic=clinic)


@patient_bp.route('/c/<slug>/register')
def clinic_register(slug):
    """Patient registration form for specific clinic."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    if not clinic.is_active:
        return render_template('clinic_inactive.html', clinic=clinic), 403
    
    # Store clinic context in session
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    session['clinic_name'] = clinic.name
    
    return render_template('patient/register.html', clinic=clinic)


@patient_bp.route('/c/<slug>/waiting/<int:patient_id>')
def clinic_waiting(slug, patient_id):
    """Patient waiting room with live updates for specific clinic."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    # Restore clinic context so /api/doctor/queue can scope to this clinic
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    
    return render_template('patient/waiting.html', patient_id=patient_id, clinic=clinic)


@patient_bp.route('/c/<slug>/result/<int:patient_id>')
def clinic_result(slug, patient_id):
    """Patient triage result page for specific clinic."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    return render_template('patient/result.html', patient_id=patient_id, clinic=clinic)


@patient_bp.route('/c/<slug>/book-appointment/<int:patient_id>')
def book_appointment(slug, patient_id):
    """Appointment slot selection page after triage."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    # Must set clinic context so /api/appointments/book can find the clinic
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    
    return render_template('patient/book_appointment.html', patient_id=patient_id, clinic=clinic)


@patient_bp.route('/c/<slug>/book')
def clinic_book_direct(slug):
    """Direct appointment booking page (without triage)."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    if not clinic.is_active:
        return render_template('clinic_inactive.html', clinic=clinic), 403
    
    # Store clinic context in session
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    session['clinic_name'] = clinic.name
    
    return render_template('patient/book_direct.html', clinic=clinic)


@patient_bp.route('/c/<slug>/appointment-confirmed')
def appointment_confirmed(slug):
    """Appointment confirmation/thank you page."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    # Ensure clinic context is set for any follow-up API calls
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    
    # Get appointment ID from session or query parameter
    appointment_id = request.args.get('id') or session.get('last_appointment_id')
    if not appointment_id:
        return redirect(url_for('patient.clinic_landing', slug=slug))
    
    return render_template('patient/appointment_confirmed.html', appointment_id=appointment_id, clinic=clinic)


@patient_bp.route('/c/<slug>/my-appointments')
def my_appointments(slug):
    """Patient's appointment history."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    # Phone verification handled by template (uses sessionStorage)
    # Template will show phone input form if not in sessionStorage
    return render_template('patient/my_appointments.html', clinic=clinic)


@patient_bp.route('/c/<slug>/checkin/<int:appointment_id>')
def appointment_checkin(slug, appointment_id):
    """Pre-appointment check-in and triage page."""
    clinic = Clinic.query.filter_by(slug=slug).first()
    
    if not clinic:
        abort(404, description="Clinic not found")
    
    # Verify appointment belongs to this clinic
    from models import Appointment
    appointment = Appointment.query.filter_by(id=appointment_id, clinic_id=clinic.id).first()
    
    if not appointment:
        # Check if the appointment exists at all — if so, redirect to my-appointments
        # rather than showing a bare 404
        from models import Appointment as Appt
        any_appt = Appt.query.get(appointment_id)
        if any_appt:
            actual_clinic = Clinic.query.get(any_appt.clinic_id)
            if actual_clinic:
                return redirect(url_for('patient.appointment_checkin',
                                       slug=actual_clinic.slug,
                                       appointment_id=appointment_id))
        return redirect(url_for('patient.my_appointments', slug=slug))
    
    session['clinic_id'] = clinic.id
    session['clinic_slug'] = clinic.slug
    
    return render_template('patient/appointment_checkin.html', 
                         clinic=clinic, 
                         appointment_id=appointment_id)
