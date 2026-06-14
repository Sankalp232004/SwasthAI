"""
Doctor Routes
Handles doctor dashboard and patient management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from app import db

doctor_bp = Blueprint('doctor', __name__)


def doctor_login_required(f):
    """Decorator to require doctor login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            return redirect(url_for('doctor.login'))
        return f(*args, **kwargs)
    return decorated_function


@doctor_bp.route('/login', methods=['GET'])
def login():
    """Doctor login page."""
    return render_template('doctor/login.html')


@doctor_bp.route('/dashboard')
@doctor_login_required
def dashboard():
    """Doctor dashboard with live queue."""
    return render_template('doctor/dashboard.html')


@doctor_bp.route('/appointments')
@doctor_login_required
def appointments_page():
    """Appointments management page."""
    return render_template('doctor/appointments.html')


@doctor_bp.route('/patient/<int:patient_id>')
@doctor_login_required
def patient_detail(patient_id):
    """Patient detail view for doctor."""
    return render_template('doctor/patient_detail.html', patient_id=patient_id)


@doctor_bp.route('/logout')
def logout():
    """Doctor logout."""
    session.pop('doctor_id', None)
    session.pop('doctor_name', None)
    return redirect(url_for('doctor.login'))


# ==================== PASSWORD MANAGEMENT ====================
@doctor_bp.route('/setup-password/<token>')
def setup_password_page(token):
    """Password setup page for new doctors."""
    from models import RegistrationToken
    
    # Verify token
    reg_token = RegistrationToken.query.filter_by(token=token).first()
    
    if not reg_token:
        return render_template('error.html', 
                             message='Invalid password setup link',
                             details='This link is not valid. Please contact your administrator.')
    
    is_valid, message = reg_token.is_valid()
    if not is_valid:
        return render_template('error.html',
                             message='Password setup link unavailable',
                             details=message)
    
    return render_template('doctor/setup_password.html', 
                         token=token, 
                         email=reg_token.email,
                         temp_password=reg_token.temp_password)


@doctor_bp.route('/setup-password', methods=['POST'])
def setup_password():
    """Handle password setup for new doctors."""
    from models import Doctor, RegistrationToken, AuditLog
    
    try:
        data = request.json or {}
        token = data.get('token')
        temp_password = data.get('temp_password')
        new_password = data.get('new_password')
        
        if not all([token, temp_password, new_password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Find and validate token
        reg_token = RegistrationToken.query.filter_by(token=token).first()
        
        if not reg_token:
            return jsonify({'error': 'Invalid or expired password setup link'}), 400
        
        is_valid, message = reg_token.is_valid()
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Verify temporary password matches
        if reg_token.temp_password != temp_password:
            return jsonify({'error': 'Incorrect temporary password. Check the credentials shown when the clinic was created.'}), 400
        
        # Get the doctor
        doctor = db.session.get(Doctor, reg_token.doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor account not found'}), 404
        
        # Set new password and mark token used
        doctor.set_password(new_password)
        reg_token.mark_used()
        
        # Log the action
        log = AuditLog(
            clinic_id=reg_token.clinic_id,
            actor_type='doctor',
            actor_id=doctor.id,
            actor_name=doctor.name,
            action='password_setup_completed',
            entity_type='doctor',
            entity_id=doctor.id,
            details={'email': doctor.email}
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password set successfully. You can now login.',
            'redirect_url': '/doctor/login'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@doctor_bp.route('/change-password')
@doctor_login_required
def change_password_page():
    """Password change page for logged-in doctors."""
    return render_template('doctor/change_password.html')


@doctor_bp.route('/change-password', methods=['POST'])
@doctor_login_required
def change_password():
    """Handle password change for logged-in doctors."""
    from models import Doctor
    from werkzeug.security import check_password_hash
    
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    # Get current doctor
    doctor = Doctor.query.get(session.get('doctor_id'))
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Verify current password
    if not doctor.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    # Update password
    doctor.set_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password updated successfully'})


# ==================== CLINIC HOURS MANAGEMENT ====================

@doctor_bp.route('/clinic-hours')
@doctor_login_required
def clinic_hours_page():
    """Clinic hours management page."""
    return render_template('doctor/clinic_hours.html')


@doctor_bp.route('/api/clinic-hours', methods=['GET'])
@doctor_login_required
def get_clinic_hours():
    """Get all clinic hours for the logged-in doctor."""
    from models import ClinicHours, Doctor
    
    doctor_id = session.get('doctor_id')
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Get all clinic hours for this doctor
    hours = ClinicHours.query.filter_by(
        clinic_id=doctor.clinic_id,
        doctor_id=doctor_id,
        is_active=True
    ).order_by(ClinicHours.day_of_week, ClinicHours.start_time).all()
    
    # Convert to dict
    hours_data = []
    for hour in hours:
        hours_data.append({
            'id': hour.id,
            'day_of_week': hour.day_of_week,
            'start_time': hour.start_time.strftime('%H:%M'),
            'end_time': hour.end_time.strftime('%H:%M'),
            'patients_per_hour': hour.patients_per_hour
        })
    
    return jsonify({'hours': hours_data})


@doctor_bp.route('/api/clinic-hours', methods=['POST'])
@doctor_login_required
def create_clinic_hours():
    """Create or update clinic hours for a specific day."""
    from models import ClinicHours, Doctor, AuditLog
    from app import db
    from datetime import datetime
    
    doctor_id = session.get('doctor_id')
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    data = request.json
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    patients_per_hour = data.get('patients_per_hour')
    
    # Validate input
    if not all([day_of_week is not None, start_time, end_time, patients_per_hour]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not (0 <= day_of_week <= 6):
        return jsonify({'error': 'Invalid day_of_week (must be 0-6)'}), 400
    
    if patients_per_hour < 1:
        return jsonify({'error': 'patients_per_hour must be at least 1'}), 400
    
    # Parse times
    try:
        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid time format (use HH:MM)'}), 400
    
    if start_time_obj >= end_time_obj:
        return jsonify({'error': 'Start time must be before end time'}), 400
    
    # Check if clinic hours already exist for this day
    existing = ClinicHours.query.filter_by(
        clinic_id=doctor.clinic_id,
        doctor_id=doctor_id,
        day_of_week=day_of_week,
        is_active=True
    ).first()
    
    if existing:
        # Update existing
        existing.start_time = start_time_obj
        existing.end_time = end_time_obj
        existing.patients_per_hour = patients_per_hour
        
        log = AuditLog(
            clinic_id=doctor.clinic_id,
            actor_type='doctor',
            actor_id=doctor_id,
            actor_name=doctor.name,
            action='update_clinic_hours',
            entity_type='clinic_hours',
            entity_id=existing.id,
            details={
                'day_of_week': day_of_week,
                'start_time': start_time,
                'end_time': end_time,
                'patients_per_hour': patients_per_hour
            }
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Clinic hours updated', 'id': existing.id})
    else:
        # Create new
        clinic_hours = ClinicHours(
            clinic_id=doctor.clinic_id,
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            start_time=start_time_obj,
            end_time=end_time_obj,
            patients_per_hour=patients_per_hour
        )
        db.session.add(clinic_hours)
        db.session.flush()
        
        log = AuditLog(
            clinic_id=doctor.clinic_id,
            actor_type='doctor',
            actor_id=doctor_id,
            actor_name=doctor.name,
            action='create_clinic_hours',
            entity_type='clinic_hours',
            entity_id=clinic_hours.id,
            details={
                'day_of_week': day_of_week,
                'start_time': start_time,
                'end_time': end_time,
                'patients_per_hour': patients_per_hour
            }
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Clinic hours created', 'id': clinic_hours.id})


@doctor_bp.route('/api/clinic-hours/<int:hour_id>', methods=['DELETE'])
@doctor_login_required
def delete_clinic_hours(hour_id):
    """Delete clinic hours."""
    from models import ClinicHours, Doctor, AuditLog
    from app import db
    
    doctor_id = session.get('doctor_id')
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Get clinic hours
    clinic_hours = ClinicHours.query.get(hour_id)
    
    if not clinic_hours:
        return jsonify({'error': 'Clinic hours not found'}), 404
    
    # Verify ownership
    if clinic_hours.doctor_id != doctor_id or clinic_hours.clinic_id != doctor.clinic_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Soft delete (set is_active = False)
    clinic_hours.is_active = False
    
    log = AuditLog(
        clinic_id=doctor.clinic_id,
        actor_type='doctor',
        actor_id=doctor_id,
        actor_name=doctor.name,
        action='delete_clinic_hours',
        entity_type='clinic_hours',
        entity_id=hour_id,
        details={'day_of_week': clinic_hours.day_of_week}
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Clinic hours deleted'})


# ==================== SLOT CONFIGURATION ====================

@doctor_bp.route('/slot-settings')
@doctor_login_required
def slot_settings_page():
    """Slot configuration page for doctors."""
    return render_template('doctor/slot_settings.html')


@doctor_bp.route('/api/doctor/<int:doctor_id>/slot-config', methods=['GET'])
@doctor_login_required
def get_slot_config(doctor_id):
    """Get slot configuration for a doctor."""
    from models import SlotConfiguration, Doctor
    
    # Verify the logged-in doctor is accessing their own config
    if session.get('doctor_id') != doctor_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Get existing configuration
    config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
    
    if config:
        return jsonify(config.to_dict())
    else:
        # Return default configuration
        return jsonify({
            'doctor_id': doctor_id,
            'clinic_id': doctor.clinic_id,
            'slot_duration_minutes': 30,
            'slots_per_batch': 5,
            'buffer_between_batches': 5,
            'walkin_slots_per_batch': 2,
            'appointment_slots_per_batch': 3,
            'max_advance_days': 30,
            'allow_same_day_booking': True,
            'is_active': True
        })


@doctor_bp.route('/api/doctor/<int:doctor_id>/slot-config', methods=['POST'])
@doctor_login_required
def update_slot_config(doctor_id):
    """Update slot configuration for a doctor."""
    from models import SlotConfiguration, Doctor, AuditLog
    from app import db
    
    # Verify the logged-in doctor is accessing their own config
    if session.get('doctor_id') != doctor_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    data = request.json
    
    # Validate input
    required_fields = ['slot_duration_minutes', 'slots_per_batch', 'max_advance_days']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate values
    if data['slot_duration_minutes'] < 5 or data['slot_duration_minutes'] > 120:
        return jsonify({'error': 'Slot duration must be between 5 and 120 minutes'}), 400
    
    if data['slots_per_batch'] < 1 or data['slots_per_batch'] > 20:
        return jsonify({'error': 'Slots per batch must be between 1 and 20'}), 400
    
    if data['max_advance_days'] < 1 or data['max_advance_days'] > 90:
        return jsonify({'error': 'Max advance days must be between 1 and 90'}), 400
    
    # Validate walk-in and appointment slots sum equals total slots
    walkin_slots = data.get('walkin_slots_per_batch', 0)
    appointment_slots = data.get('appointment_slots_per_batch', 0)
    total_slots = data['slots_per_batch']
    
    if walkin_slots + appointment_slots != total_slots:
        return jsonify({'error': 'Walk-in and appointment slots must sum to total slots'}), 400
    
    # Get existing configuration or create new
    config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
    
    if config:
        # Update existing
        config.slot_duration_minutes = data['slot_duration_minutes']
        config.slots_per_batch = data['slots_per_batch']
        config.buffer_between_batches = data.get('buffer_between_batches', 5)
        config.walkin_slots_per_batch = walkin_slots
        config.appointment_slots_per_batch = appointment_slots
        config.max_advance_days = data['max_advance_days']
        config.allow_same_day_booking = data.get('allow_same_day_booking', True)
        config.is_active = data.get('is_active', True)
        
        action = 'update_slot_config'
        message = 'Slot configuration updated'
    else:
        # Create new
        config = SlotConfiguration(
            clinic_id=doctor.clinic_id,
            doctor_id=doctor_id,
            slot_duration_minutes=data['slot_duration_minutes'],
            slots_per_batch=data['slots_per_batch'],
            buffer_between_batches=data.get('buffer_between_batches', 5),
            walkin_slots_per_batch=walkin_slots,
            appointment_slots_per_batch=appointment_slots,
            max_advance_days=data['max_advance_days'],
            allow_same_day_booking=data.get('allow_same_day_booking', True),
            is_active=data.get('is_active', True)
        )
        db.session.add(config)
        action = 'create_slot_config'
        message = 'Slot configuration created'
    
    # Log the action
    log = AuditLog(
        clinic_id=doctor.clinic_id,
        actor_type='doctor',
        actor_id=doctor_id,
        actor_name=doctor.name,
        action=action,
        entity_type='slot_configuration',
        entity_id=config.id if config.id else None,
        details=data
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': message, 'config': config.to_dict()})
