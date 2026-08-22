"""
API Routes
RESTful API for patient submission, doctor queue, and overrides.
"""

from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, date, time, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_

from app import db
from models import Patient, Doctor, AuditLog, PriorityEnum, StatusEnum, Clinic, Appointment, SlotConfiguration, ClinicHours, SystemSetting
from triage_engine import validate_triage_input, compute_triage, triage_to_dict, ENGINE_VERSION

api_bp = Blueprint('api', __name__)

# India Standard Time = UTC+5:30
_IST = timezone(timedelta(hours=5, minutes=30))

def ist_day_start_utc():
    """Return the start of the current IST calendar day as a naive UTC datetime.
    IST midnight = 18:30 UTC the previous day.
    Using this instead of UTC midnight ensures 'today' matches what users see.
    """
    ist_now = datetime.now(tz=_IST)
    ist_midnight = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)
    return ist_midnight.astimezone(timezone.utc).replace(tzinfo=None)

def ist_today_date():
    """Return today's date in IST (may differ from UTC date after 18:30 UTC)."""
    return datetime.now(tz=_IST).date()

def format_ist(dt_naive_utc):
    """Format a naive UTC datetime as a human-readable IST string.
    Uses portable stripping instead of %-d/%-I (Linux-only strftime flags).
    """
    if dt_naive_utc is None:
        return None
    import re as _re
    dt_utc = dt_naive_utc.replace(tzinfo=timezone.utc)
    dt_ist = dt_utc.astimezone(_IST)
    s = dt_ist.strftime('%d %b %Y, %I:%M %p IST')
    # Strip leading zero from day (01 → 1) and hour (01:05 PM → 1:05 PM)
    s = _re.sub(r'^0', '', s)
    s = _re.sub(r', 0(\d:)', r', \1', s)
    return s


@api_bp.route('/server-base-url', methods=['GET'])
def get_server_base_url():
    """Public endpoint: returns the configured app base URL for QR links.
    Priority: (1) stored SystemSetting, (2) live cloudflared URL,
    (3) APP_BASE_URL config, (4) request.host_url.
    """
    stored = SystemSetting.get('base_url', '').strip()
    if stored:
        return jsonify({'base_url': stored, 'is_configured': True})

    import re as _re
    try:
        with open('/shared/cloudflared.log') as _f:
            _m = _re.search(r'https://[a-z0-9\-]+\.trycloudflare\.com', _f.read())
        if _m:
            live_url = _m.group()
            # Persist so QR codes and other callers stay in sync
            SystemSetting.set('base_url', live_url)
            return jsonify({'base_url': live_url, 'is_configured': True})
    except Exception:
        pass

    configured = (current_app.config.get('APP_BASE_URL') or '').strip()
    return jsonify({
        'base_url': configured or request.host_url.rstrip('/'),
        'is_configured': False
    })


# Event broadcaster for SSE
_event_subscribers = []


def broadcast_event(event_type: str, data: dict):
    """Broadcast event to all SSE subscribers."""
    from routes.sse_routes import broadcast_queue_update
    broadcast_queue_update(event_type, data)


# =============================================================================
# PATIENT API
# =============================================================================

@api_bp.route('/patient/submit', methods=['POST'])
def patient_submit():
    """
    Patient Submit Endpoint.
    - Validate input
    - Run triage engine
    - Save atomically (with clinic association)
    - Return priority + reasons
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get clinic from session
        clinic_id = session.get('clinic_id')
        if not clinic_id:
            return jsonify({'error': 'No clinic context. Please scan QR code or select a clinic.'}), 400
        
        # Verify clinic exists and is active
        clinic = Clinic.query.get(clinic_id)
        if not clinic:
            return jsonify({'error': 'Clinic not found'}), 404
        if not clinic.is_active:
            return jsonify({'error': 'Clinic is currently inactive'}), 403
        
        # Extract demographics
        name = data.get('name', '').strip()
        age = data.get('age')
        gender = data.get('gender', '').strip()
        phone = data.get('phone', '').strip()
        complaint = data.get('complaint', '').strip()
        
        # Validate demographics
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        if not isinstance(age, int) or age < 0 or age > 150:
            return jsonify({'error': 'Valid age is required (0-150)'}), 400
        if gender not in ['Male', 'Female', 'Other']:
            return jsonify({'error': 'Gender must be Male, Female, or Other'}), 400
        if not phone:
            return jsonify({'error': 'Phone is required'}), 400
        if not complaint:
            return jsonify({'error': 'Chief complaint is required'}), 400
        
        # Resolve doctor_id for this submission
        # 1. Use explicitly provided doctor_id
        # 2. Auto-assign if clinic has only one active (non-admin) doctor
        # 3. Fall back to any single active doctor in the clinic
        request_doctor_id = data.get('doctor_id')
        resolved_doctor_id = None
        if request_doctor_id:
            try:
                rid = int(request_doctor_id)
                doc_check = Doctor.query.filter_by(id=rid, clinic_id=clinic_id, is_active=True).first()
                if doc_check:
                    resolved_doctor_id = rid
            except (ValueError, TypeError):
                pass
        if not resolved_doctor_id:
            # Auto-assign: prefer clinical (non-admin) doctors if any
            all_docs = Doctor.query.filter_by(clinic_id=clinic_id, is_active=True).all()
            clinical_docs = [d for d in all_docs if d.specialization and d.specialization.lower() != 'administrator']
            target_docs = clinical_docs if clinical_docs else all_docs
            if len(target_docs) == 1:
                resolved_doctor_id = target_docs[0].id
            # If multiple doctors and no selection: leave None (unassigned)

        # Extract clinical data (15 inputs)
        clinical_inputs = {
            'heart_rate': data.get('heart_rate'),
            'systolic_bp': data.get('systolic_bp'),
            'diastolic_bp': data.get('diastolic_bp'),
            'respiratory_rate': data.get('respiratory_rate'),
            'temperature': data.get('temperature'),
            'consciousness_level': data.get('consciousness_level'),
            'pain_level': data.get('pain_level'),
            'pain_location': data.get('pain_location', 'N/A'),
            'chest_pain': data.get('chest_pain'),
            'difficulty_breathing': data.get('difficulty_breathing'),
            'bleeding_severity': data.get('bleeding_severity'),
            'symptom_duration_hours': data.get('symptom_duration_hours'),
            'is_pregnant': data.get('is_pregnant'),
            'has_diabetes': data.get('has_diabetes'),
            'has_heart_condition': data.get('has_heart_condition')
        }
        
        # Validate clinical inputs
        is_valid, error_msg, validated_input = validate_triage_input(clinical_inputs)
        
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Run triage engine (PURE FUNCTION)
        triage_result = compute_triage(validated_input)
        
        # If red flags present, this is a hard stop - priority cannot be GREEN
        # Red flags trigger immediate escalation
        has_red_flags = len(triage_result.red_flags) > 0
        
        # Build clinical_data JSONB
        clinical_data = {
            'inputs': clinical_inputs,
            'triage_result': triage_to_dict(triage_result),
            'red_flags': triage_result.red_flags,
            'engine_version': ENGINE_VERSION,
            'override_history': [],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Check if patient exists (returning patient)
        existing_patient = Patient.query.filter_by(
            clinic_id=clinic_id,
            phone=phone
        ).first()
        
        if existing_patient:
            # RETURNING PATIENT - Store visit history
            visit_history = existing_patient.clinical_data.get('visit_history', []) if existing_patient.clinical_data else []
            
            # Add previous visit to history
            visit_history.append({
                'visit_number': existing_patient.visit_count,
                'date': (existing_patient.last_visit.isoformat() + 'Z') if existing_patient.last_visit else None,
                'complaint': existing_patient.complaint,
                'priority': existing_patient.priority,
                'status': existing_patient.status,
                'triage_result': existing_patient.clinical_data.get('triage_result') if existing_patient.clinical_data else None
            })
            
            # Keep only last 10 visits in history
            if len(visit_history) > 10:
                visit_history = visit_history[-10:]
            
            clinical_data['visit_history'] = visit_history
            clinical_data['is_returning_patient'] = True
            clinical_data['previous_visit_count'] = existing_patient.visit_count
            
            # Update existing patient - new visit
            existing_patient.name = name
            existing_patient.age = age
            existing_patient.gender = gender
            existing_patient.complaint = complaint
            existing_patient.priority = triage_result.priority
            existing_patient.status = 'Waiting'
            existing_patient.clinical_data = clinical_data
            existing_patient.visit_count += 1
            existing_patient.last_visit = datetime.utcnow()
            existing_patient.updated_at = datetime.utcnow()
            if resolved_doctor_id:
                existing_patient.doctor_id = resolved_doctor_id
            patient = existing_patient
        else:
            # NEW PATIENT
            clinical_data['visit_history'] = []
            clinical_data['is_returning_patient'] = False
            
            # Create new patient record
            # Set last_visit to now so daily_token computation works uniformly
            # (token query filters on last_visit; without it new patients get token 0)
            patient = Patient(
                clinic_id=clinic_id,
                doctor_id=resolved_doctor_id,
                name=name,
                age=age,
                gender=gender,
                phone=phone,
                complaint=complaint,
                priority=triage_result.priority,
                status='Waiting',
                clinical_data=clinical_data,
                last_visit=datetime.utcnow()
            )
            db.session.add(patient)
        
        # Save atomically
        db.session.commit()
        
        # Broadcast new patient event for realtime updates
        broadcast_event('new_patient', patient.to_dict())
        
        # Store patient_id in session for booking flow
        session['patient_id'] = patient.id
        session['patient_phone'] = phone
        
        # Get redirect URL with token
        token = session.get('registration_token')
        redirect_slug = session.get('clinic_slug', clinic.slug)
        
        return jsonify({
            'success': True,
            'patient_id': patient.id,
            'priority': triage_result.priority,
            'reasons': triage_result.reasons,
            'red_flags': triage_result.red_flags,
            'has_red_flags': has_red_flags,
            'registration_token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Patient submit error: {str(e)}")
        return jsonify({'error': 'Internal server error. Please try again.'}), 500


@api_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient details with daily token number."""
    patient = Patient.query.get_or_404(patient_id)
    patient_data = patient.to_dict()
    # Compute today's sequential token using IST day boundary.
    # last_visit is set to utcnow() on both new registration and re-registration,
    # so it always reflects the patient's CURRENT check-in time (unlike created_at
    # which stays at the original registration date for returning patients).
    today_start = ist_day_start_utc()
    eff_time = patient.last_visit if patient.last_visit is not None else patient.created_at
    if eff_time >= today_start:
        today_token = Patient.query.filter(
            Patient.clinic_id == patient.clinic_id,
            Patient.last_visit >= today_start,
            or_(
                Patient.last_visit < eff_time,
                and_(Patient.last_visit == eff_time, Patient.id <= patient_id)
            )
        ).count()
    else:
        today_token = 0
    patient_data['daily_token'] = today_token
    # Pre-format time server-side in IST so JS timezone parsing is irrelevant.
    # For returning patients, last_visit holds the current check-in time;
    # for new patients it equals created_at. Always prefer last_visit.
    visit_time = patient.last_visit if patient.last_visit else patient.created_at
    patient_data['created_at_local'] = format_ist(visit_time)
    return jsonify(patient_data)


@api_bp.route('/patient/lookup', methods=['POST'])
def patient_lookup():
    """
    Look up patient by phone number to fetch their history.
    Used to prefill form for returning patients.
    """
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        clinic_id = session.get('clinic_id')
        
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400
        
        if not clinic_id:
            return jsonify({'error': 'No clinic context'}), 400
        
        # Find patient by phone in this clinic
        patient = Patient.query.filter_by(
            clinic_id=clinic_id,
            phone=phone
        ).order_by(Patient.last_visit.desc()).first()
        
        if not patient:
            return jsonify({
                'found': False,
                'message': 'New patient - please fill in all details'
            })
        
        # Get patient's appointment history
        appointments = Appointment.query.filter_by(
            patient_id=patient.id
        ).order_by(Appointment.appointment_date.desc()).limit(10).all()
        
        # Get patient's visit history (previous triage records)
        # We'll store each visit in the audit logs
        visit_history = []
        if patient.clinical_data and isinstance(patient.clinical_data, dict):
            # Get last few visits from clinical_data history
            history = patient.clinical_data.get('visit_history', [])
            visit_history = history[-5:] if history else []  # Last 5 visits
        
        return jsonify({
            'found': True,
            'patient': patient.to_dict(),
            'appointments': [apt.to_dict() for apt in appointments],
            'visit_count': patient.visit_count,
            'last_visit': (patient.last_visit.isoformat() + 'Z') if patient.last_visit else None,
            'visit_history': visit_history,
            'message': f'Welcome back! You\'ve visited us {patient.visit_count} time(s).'
        })
        
    except Exception as e:
        current_app.logger.error(f"Patient lookup error: {str(e)}")
        return jsonify({'error': 'Lookup failed'}), 500


@api_bp.route('/patient/<int:patient_id>/history', methods=['GET'])
def get_patient_history(patient_id):
    """
    Get comprehensive patient history for doctor to review.
    Includes all visits, appointments, and clinical data.
    """
    try:
        patient = Patient.query.get_or_404(patient_id)
        
        # Get all appointments
        appointments = Appointment.query.filter_by(
            patient_id=patient_id
        ).order_by(Appointment.appointment_date.desc()).all()
        
        # Get audit logs for this patient
        audit_logs = AuditLog.query.filter_by(
            entity_type='patient',
            entity_id=patient_id
        ).order_by(AuditLog.timestamp.desc()).limit(20).all()
        
        # Extract visit history from clinical data
        visit_history = []
        if patient.clinical_data and isinstance(patient.clinical_data, dict):
            visit_history = patient.clinical_data.get('visit_history', [])
        
        return jsonify({
            'patient': patient.to_dict(),
            'visit_count': patient.visit_count,
            'appointments': [apt.to_dict() for apt in appointments],
            'visit_history': visit_history,
            'audit_logs': [log.to_dict() for log in audit_logs],
            'summary': {
                'total_visits': patient.visit_count,
                'total_appointments': len(appointments),
                'last_visit': (patient.last_visit.isoformat() + 'Z') if patient.last_visit else None,
                'first_visit': patient.created_at.isoformat() + 'Z'
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching patient history: {str(e)}")
        return jsonify({'error': 'Failed to fetch history'}), 500


# =============================================================================
# DOCTOR API
# =============================================================================

@api_bp.route('/doctor/list', methods=['GET'])
def list_doctors():
    """Get list of doctors for a clinic (public endpoint for booking / walk-in selection).

    For multi-doctor clinics, the auto-created 'Administrator' doctor is excluded
    from patient-facing selection — only clinical doctors are shown.
    For single-doctor clinics (admin IS the doctor) the admin is included.
    """
    try:
        clinic_id = request.args.get('clinic_id')
        if not clinic_id:
            clinic_id = session.get('clinic_id')
        
        if not clinic_id:
            return jsonify({'error': 'Clinic ID required'}), 400
        
        all_doctors = Doctor.query.filter_by(
            clinic_id=clinic_id,
            is_active=True
        ).all()

        # Separate clinical doctors from admin-only doctors
        clinical_doctors = [
            d for d in all_doctors
            if not (d.specialization and d.specialization.lower() == 'administrator')
        ]
        # If clinical doctors exist, show only them; otherwise show all (single-doc clinic)
        doctors = clinical_doctors if clinical_doctors else all_doctors
        
        return jsonify({
            'doctors': [{
                'id': d.id,
                'name': d.name,
                'specialization': d.specialization,
                'email': d.email
            } for d in doctors]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error listing doctors: {str(e)}")
        return jsonify({'error': 'Failed to load doctors'}), 500


@api_bp.route('/doctor/login', methods=['POST'])
def doctor_login():
    """Doctor authentication."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    doctor = Doctor.query.filter_by(email=email, is_active=True).first()
    
    if not doctor or not check_password_hash(doctor.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Set session
    session['doctor_id'] = doctor.id
    session['doctor_name'] = doctor.name
    session['clinic_id'] = doctor.clinic_id
    session.permanent = True
    
    return jsonify({
        'success': True,
        'doctor': doctor.to_dict()
    })


@api_bp.route('/doctor/queue', methods=['GET'])
def doctor_queue():
    """
    Get patient queue for doctors and patients.
    Always sorted by:
    1. Priority (EMERGENCY > RED > AMBER > GREEN)
    2. Check-in time (oldest first)

    Accepts optional ?clinic_id= query param so the patient-side waiting
    room can always scope to the correct clinic even when the server-side
    session has been recycled or was never set (e.g. direct URL visit).
    """
    # Prefer explicit query-param (patient-side calls always send it),
    # fall back to session (doctor-side calls), then resolve from doctor record.
    clinic_id = request.args.get('clinic_id', type=int) or session.get('clinic_id')
    if not clinic_id:
        doctor_id = session.get('doctor_id')
        if doctor_id:
            doctor_rec = Doctor.query.get(doctor_id)
            if doctor_rec:
                clinic_id = doctor_rec.clinic_id
                session['clinic_id'] = clinic_id
    today = ist_today_date()

    # Patients IDs that have an active appointment today — exclude from walk-in list
    appt_patient_ids = {
        pid for (pid,) in db.session.query(Appointment.patient_id).filter(
            Appointment.appointment_date == today,
            Appointment.status.notin_(['cancelled', 'no_show', 'completed'])
        ).distinct().all()
    }

    # ── Doctor filter ─────────────────────────────────────────────────────────
    # Priority:
    #  1. session['doctor_id']  — set when a doctor is logged in (doctor dashboard)
    #  2. ?doctor_id= query param — sent by patient waiting room to scope to their doctor
    # Patients with doctor_id=NULL are treated as unassigned and shown to all.
    filter_doctor_id = session.get('doctor_id')
    if not filter_doctor_id:
        filter_doctor_id = request.args.get('doctor_id', type=int)

    # Only show waiting and consulting patients scoped to this clinic
    query = Patient.query.filter(Patient.status.in_(['Waiting', 'Consulting']))
    if clinic_id:
        query = query.filter_by(clinic_id=clinic_id)
    if filter_doctor_id:
        from sqlalchemy import or_ as _or
        query = query.filter(
            _or(Patient.doctor_id == filter_doctor_id, Patient.doctor_id == None)
        )
    patients = [p for p in query.all() if p.id not in appt_patient_ids]

    # Define priority order
    priority_order = {
        'EMERGENCY': 0,
        'RED': 1,
        'AMBER': 2,
        'GREEN': 3
    }

    # Sort by priority first, then by effective check-in time (last_visit for
    # returning patients, created_at for new ones) so a patient who re-checks in
    # today appears at the correct spot — AFTER others who arrived before them.
    sorted_patients = sorted(
        patients,
        key=lambda p: (priority_order.get(p.priority, 99), p.last_visit or p.created_at)
    )

    return jsonify({
        'queue': [p.to_dict() for p in sorted_patients],
        'count': len(sorted_patients)
    })


@api_bp.route('/doctor/patient/<int:patient_id>/status', methods=['PUT'])
def update_patient_status(patient_id):
    """Update patient consultation status."""
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['Waiting', 'Consulting', 'Completed']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Status must be one of: {valid_statuses}'}), 400
    
    patient = Patient.query.get_or_404(patient_id)
    old_status = patient.status if isinstance(patient.status, str) else patient.status.value
    
    # Update status (store as string, not enum)
    patient.status = new_status
    patient.updated_at = datetime.utcnow()
    
    # Create audit log
    audit = AuditLog(
        clinic_id=patient.clinic_id,
        actor_type='doctor',
        actor_id=session['doctor_id'],
        actor_name=session.get('doctor_name', 'Unknown'),
        action='STATUS_CHANGE',
        entity_type='patient',
        entity_id=patient.id,
        details={
            'before_status': old_status,
            'after_status': new_status,
            'reason': f"Status changed by Dr. {session.get('doctor_name', 'Unknown')}"
        },
        ip_address=request.remote_addr
    )
    
    db.session.add(audit)
    db.session.commit()
    
    # Broadcast status change
    broadcast_event('status_change', patient.to_dict())
    
    return jsonify({
        'success': True,
        'patient': patient.to_dict()
    })


@api_bp.route('/doctor/patient/<int:patient_id>/override', methods=['POST'])
def override_priority(patient_id):
    """
    Doctor Priority Override.
    - Role-protected
    - Requires justification
    - Logged permanently
    - Append-only (original never deleted)
    """
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    new_priority = data.get('priority')
    justification = data.get('justification', '').strip()
    
    # Validate priority
    valid_priorities = ['EMERGENCY', 'RED', 'AMBER', 'GREEN']
    if new_priority not in valid_priorities:
        return jsonify({'error': f'Priority must be one of: {valid_priorities}'}), 400
    
    # Require justification
    if not justification or len(justification) < 10:
        return jsonify({'error': 'Justification must be at least 10 characters'}), 400
    
    patient = Patient.query.get_or_404(patient_id)
    # priority is stored as a plain string in DB, not an enum instance
    old_priority = patient.priority if isinstance(patient.priority, str) else patient.priority.value

    # Don't allow same priority
    if old_priority == new_priority:
        return jsonify({'error': 'New priority must be different from current'}), 400
    
    # Update clinical_data with override history (append-only)
    clinical_data = (patient.clinical_data or {}).copy()
    override_entry = {
        'doctor_id': session['doctor_id'],
        'doctor_name': session.get('doctor_name', 'Unknown'),
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'from_priority': old_priority,
        'to_priority': new_priority,
        'justification': justification
    }
    
    clinical_data.setdefault('override_history', []).append(override_entry)
    
    # Update patient — store priority as plain string (not enum)
    patient.priority = new_priority
    patient.clinical_data = clinical_data

    # Sync triage_priority in any active appointments for this patient
    active_apts = Appointment.query.filter_by(patient_id=patient.id).filter(
        Appointment.status.in_(['scheduled', 'checked_in', 'consulting'])
    ).all()
    for apt_row in active_apts:
        apt_row.triage_priority = new_priority

    # Create audit log
    audit = AuditLog(
        clinic_id=patient.clinic_id,
        actor_type='doctor',
        actor_id=session['doctor_id'],
        actor_name=session.get('doctor_name', 'Unknown'),
        action='PRIORITY_OVERRIDE',
        entity_type='patient',
        entity_id=patient.id,
        details={
            'before_priority': old_priority,
            'after_priority': new_priority,
            'justification': justification
        }
    )
    
    db.session.add(audit)
    db.session.commit()
    
    # Broadcast priority change for realtime update
    broadcast_event('priority_override', patient.to_dict())
    
    return jsonify({
        'success': True,
        'patient': patient.to_dict(),
        'override': override_entry
    })


# =============================================================================
# APPOINTMENT STATUS UPDATE (doctor side)
# =============================================================================

@api_bp.route('/doctor/appointment/<int:appt_id>/status', methods=['PUT'])
def update_appointment_status(appt_id):
    """Update appointment status from the doctor dashboard."""
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['scheduled', 'checked_in', 'consulting', 'completed', 'no_show', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Status must be one of: {valid_statuses}'}), 400
    
    appt = Appointment.query.get_or_404(appt_id)
    old_status = appt.status
    
    appt.status = new_status
    appt.updated_at = datetime.utcnow()
    if new_status == 'completed' and not appt.completed_at:
        appt.completed_at = datetime.utcnow()
    elif new_status == 'checked_in' and not appt.checked_in_at:
        appt.checked_in_at = datetime.utcnow()
    
    audit = AuditLog(
        clinic_id=appt.clinic_id,
        actor_type='doctor',
        actor_id=session['doctor_id'],
        actor_name=session.get('doctor_name', 'Unknown'),
        action='APPOINTMENT_STATUS_CHANGE',
        entity_type='appointment',
        entity_id=appt_id,
        details={'before_status': old_status, 'after_status': new_status}
    )
    db.session.add(audit)
    db.session.commit()
    
    broadcast_event('status_change', {'appointment_id': appt_id, 'status': new_status})
    return jsonify({'success': True, 'appointment': appt.to_dict()})


# =============================================================================
# SETUP API (for initial doctor creation)
# =============================================================================

@api_bp.route('/setup/doctor', methods=['POST'])
def create_doctor():
    """Create a doctor account (for setup purposes)."""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    specialization = data.get('specialization', '').strip()
    clinic_id = data.get('clinic_id') or session.get('clinic_id')
    
    if not name or not email or not password or not clinic_id:
        return jsonify({'error': 'Name, email, password, and clinic_id are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if email exists
    existing = Doctor.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'Email already registered'}), 400
    
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return jsonify({'error': 'Clinic not found'}), 404

    doctor = Doctor(
        clinic_id=clinic_id,
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        specialization=specialization or None
    )
    
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'doctor': doctor.to_dict()
    }), 201


@api_bp.route('/audit/patient/<int:patient_id>', methods=['GET'])
def get_patient_audit(patient_id):
    """Get audit trail for a patient."""
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    audits = AuditLog.query.filter_by(
        entity_type='patient',
        entity_id=patient_id
    ).order_by(AuditLog.timestamp.desc()).all()
    
    return jsonify({
        'audits': [a.to_dict() for a in audits]
    })


# =============================================================================
# SLOT BOOKING API
# =============================================================================

@api_bp.route('/doctor/<int:doctor_id>/slot-config', methods=['GET', 'POST', 'PUT'])
def manage_slot_config(doctor_id):
    """Get or update slot configuration for a doctor."""
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if session.get('doctor_id') != doctor_id:
        return jsonify({'error': 'Access denied'}), 403
    
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'GET':
        config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
        if not config:
            # Return default config
            return jsonify({
                'slot_duration_minutes': 30,
                'slots_per_batch': 5,
                'buffer_between_batches': 5,
                'max_advance_days': 30,
                'allow_same_day_booking': True,
                'is_active': True,
                'walkin_slots_per_batch': 2,
                'appointment_slots_per_batch': 3
            })
        return jsonify(config.to_dict())
    
    # POST or PUT - create or update
    data = request.get_json()
    
    config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
    if not config:
        config = SlotConfiguration(
            clinic_id=doctor.clinic_id,
            doctor_id=doctor_id
        )
        db.session.add(config)
    
    # Update fields
    if 'slot_duration_minutes' in data:
        config.slot_duration_minutes = int(data['slot_duration_minutes'])
    if 'slots_per_batch' in data:
        config.slots_per_batch = int(data['slots_per_batch'])
    if 'buffer_between_batches' in data:
        config.buffer_between_batches = int(data['buffer_between_batches'])
    if 'max_advance_days' in data:
        config.max_advance_days = int(data['max_advance_days'])
    if 'allow_same_day_booking' in data:
        config.allow_same_day_booking = bool(data['allow_same_day_booking'])
    if 'is_active' in data:
        config.is_active = bool(data['is_active'])
    if 'walkin_slots_per_batch' in data:
        config.walkin_slots_per_batch = int(data['walkin_slots_per_batch'])
    if 'appointment_slots_per_batch' in data:
        config.appointment_slots_per_batch = int(data['appointment_slots_per_batch'])
    
    config.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True, 'config': config.to_dict()})


# =============================================================================
# LOCATION-BASED CLINIC DISCOVERY
# =============================================================================

@api_bp.route('/clinics/nearby', methods=['GET'])
def get_nearby_clinics():
    """
    Get nearby active clinics based on user location.
    Uses Haversine formula to calculate distance.
    """
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius_km = float(request.args.get('radius', 10))  # Default 10km radius
    except (TypeError, ValueError):
        return jsonify({'error': 'Valid latitude, longitude required'}), 400
    
    # Get all active clinics with location
    clinics = Clinic.query.filter_by(is_active=True).filter(
        Clinic.latitude.isnot(None),
        Clinic.longitude.isnot(None)
    ).all()
    
    # Calculate distance and filter
    from math import radians, cos, sin, asin, sqrt
    
    def haversine(lon1, lat1, lon2, lat2):
        """Calculate distance between two points on earth (in kilometers)"""
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    nearby = []
    for clinic in clinics:
        distance = haversine(lng, lat, clinic.longitude, clinic.latitude)
        if distance <= radius_km:
            clinic_data = clinic.to_dict()
            clinic_data['distance_km'] = round(distance, 2)
            clinic_data['doctors'] = [
                {
                    'id': d.id,
                    'name': d.name,
                    'specialization': d.specialization
                } for d in clinic.doctors if d.is_active
            ]
            nearby.append(clinic_data)
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        'clinics': nearby,
        'count': len(nearby),
        'search_center': {'lat': lat, 'lng': lng},
        'radius_km': radius_km
    })


@api_bp.route('/doctor/<int:doctor_id>/available-slots', methods=['GET'])
def get_available_slots(doctor_id):
    """Get available slots for a doctor on a specific date."""
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date parameter required (YYYY-MM-DD)'}), 400
        
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = ist_today_date()  # Use IST date to avoid UTC midnight mismatch
        
        # Check if date is in the past
        if appointment_date < today:
            return jsonify({'error': 'Cannot book appointments in the past'}), 400
        
        doctor = Doctor.query.get_or_404(doctor_id)
        
        # Get slot configuration (or use defaults)
        slot_config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
        if not slot_config:
            slot_config = SlotConfiguration(
                slot_duration_minutes=30,
                slots_per_batch=5,
                buffer_between_batches=5,
                max_advance_days=30,
                allow_same_day_booking=True
            )
        
        # Check advance booking limits
        days_advance = (appointment_date - today).days
        if days_advance > slot_config.max_advance_days:
            return jsonify({'error': f'Cannot book more than {slot_config.max_advance_days} days in advance'}), 400
        
        if days_advance == 0 and not slot_config.allow_same_day_booking:
            return jsonify({'error': 'Same-day booking is not allowed'}), 400
        
        # Get clinic hours for this day
        day_of_week = appointment_date.weekday()
        clinic_hours = ClinicHours.query.filter_by(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            is_active=True
        ).all()
        
        if not clinic_hours:
            return jsonify({
                'available_slots': [],
                'error': f'Doctor not available on {appointment_date.strftime("%A")}. Please select another date.'
            })
        
        # Generate HOUR-BLOCK slots (patients see the whole hour, system assigns their
        # exact sub-slot via batch_number when they book).
        BLOCK_MINUTES = 60
        capacity_per_block = slot_config.slots_per_batch  # e.g. 3 patients per hour

        available_slots = []
        is_today = (appointment_date == ist_today_date())
        # Current IST time as naive datetime for comparison
        ist_now_naive = datetime.now(tz=_IST).replace(tzinfo=None)

        # Batch-fetch ALL active appointments for this doctor+date in one query.
        # We store the HOUR-BLOCK start as slot_start_time for new bookings.
        active_appointments = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date
        ).filter(
            Appointment.status.notin_(['cancelled', 'no_show'])
        ).with_entities(Appointment.slot_start_time).all()

        # Build a counter: hour_block_start_time -> count
        from collections import Counter
        booked_counts = Counter(a.slot_start_time for a in active_appointments)

        for hours in clinic_hours:
            start_dt = datetime.combine(appointment_date, hours.start_time)
            end_dt   = datetime.combine(appointment_date, hours.end_time)

            block_start = start_dt
            while block_start < end_dt:
                block_end = min(block_start + timedelta(minutes=BLOCK_MINUTES), end_dt)

                # Skip past blocks for same-day bookings (IST)
                if is_today and block_end <= ist_now_naive:
                    block_start = block_end
                    continue

                booked_count   = booked_counts.get(block_start.time(), 0)
                spots_remaining = max(0, capacity_per_block - booked_count)

                available_slots.append({
                    'start_time':      block_start.strftime('%H:%M'),
                    'end_time':        block_end.strftime('%H:%M'),
                    'available_slots': spots_remaining,
                    'total_slots':     capacity_per_block,
                    'booked_count':    booked_count,
                    'is_available':    spots_remaining > 0
                })

                block_start = block_end

        return jsonify({
            'date': date_str,
            'doctor_id': doctor_id,
            'doctor_name': doctor.name,
            'available_slots': available_slots,
            'slot_config': {
                'duration_minutes': slot_config.slot_duration_minutes,
                'slots_per_batch':  capacity_per_block
            }
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting available slots: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/appointments/book', methods=['POST'])
def book_appointment():
    """Book an appointment slot."""
    try:
        data = request.get_json()
        
        # Get clinic from session (for walk-in triage flow)
        clinic_id = session.get('clinic_id')
        if not clinic_id:
            return jsonify({'error': 'No clinic context'}), 400
        
        # Required fields
        required = ['doctor_id', 'appointment_date', 'slot_start_time', 'slot_end_time', 'reason']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        doctor_id = int(data['doctor_id'])
        appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        slot_start = datetime.strptime(data['slot_start_time'], '%H:%M').time()
        slot_end = datetime.strptime(data['slot_end_time'], '%H:%M').time()
        reason = data['reason'].strip()
        
        # Validate time range
        if slot_end <= slot_start:
            return jsonify({'error': 'Slot end time must be after start time'}), 400
        
        # Validate doctor belongs to this clinic
        doctor = Doctor.query.get(doctor_id)
        if not doctor or doctor.clinic_id != clinic_id:
            return jsonify({'error': 'Doctor not available at this clinic'}), 400
        
        # Get or create patient
        patient_id = data.get('patient_id')
        if patient_id:
            patient = Patient.query.get(patient_id)
            if not patient:
                return jsonify({'error': 'Patient not found'}), 404
        else:
            # Create new patient from booking data
            patient = Patient(
                clinic_id=clinic_id,
                name=data.get('patient_name', 'Walk-in Patient'),
                age=data.get('patient_age', 0),
                gender=data.get('patient_gender', 'Other'),
                phone=data.get('patient_phone', ''),
                complaint=reason,
                priority='GREEN',
                status='Waiting',
                clinical_data={}
            )
            db.session.add(patient)
            db.session.flush()  # Get patient ID
        
        # Get slot configuration
        slot_config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
        if not slot_config:
            slot_config = SlotConfiguration(slots_per_batch=3)

        capacity_per_block = slot_config.slots_per_batch

        # Count how many patients have already booked this HOUR BLOCK
        # (all patients in the same hour share the same slot_start_time)
        booked_count = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            slot_start_time=slot_start  # hour-block start time
        ).filter(
            Appointment.status.notin_(['cancelled', 'no_show'])
        ).count()

        if booked_count >= capacity_per_block:
            return jsonify({'error': 'This time slot is fully booked. Please choose another slot.'}), 409

        # Auto-assign position within the hour block (1 = first, 2 = second …)
        batch_number = booked_count + 1

        # Create appointment — slot_start/end store the HOUR BLOCK so the patient
        # sees "11:00 – 12:00"; batch_number encodes the actual sub-slot order.
        appointment = Appointment(
            clinic_id=clinic_id,
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            slot_start_time=slot_start,
            slot_end_time=slot_end,
            batch_number=batch_number,
            reason=reason,
            status='scheduled'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # Store appointment ID in session for thank you page
        session['last_appointment_id'] = appointment.id
        
        return jsonify({
            'success': True,
            'appointment': appointment.to_dict(),
            'message': 'Appointment booked successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error booking appointment: {str(e)}")
        return jsonify({'error': 'Failed to book appointment'}), 500


@api_bp.route('/appointments/patient/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    """Get all appointments for a patient, optionally scoped to a clinic."""
    try:
        # Scope to clinic when called from patient-facing pages
        clinic_slug = request.args.get('clinic_slug')
        clinic_id = None
        if clinic_slug:
            from models import Clinic
            clinic_obj = Clinic.query.filter_by(slug=clinic_slug).first()
            if clinic_obj:
                clinic_id = clinic_obj.id
                # Also set session so subsequent POSTs (book, check-in) work
                session['clinic_id'] = clinic_id
                session['clinic_slug'] = clinic_slug

        query = Appointment.query.filter_by(patient_id=patient_id)
        if clinic_id:
            query = query.filter_by(clinic_id=clinic_id)
        appointments = query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.slot_start_time.desc()
        ).all()
        
        return jsonify({
            'appointments': [apt.to_dict() for apt in appointments]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting patient appointments: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/appointments/<int:appointment_id>/details', methods=['GET'])
def get_appointment_details(appointment_id):
    """Get complete appointment details for confirmation page."""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found', 'not_found': True}), 404
        patient = Patient.query.get(appointment.patient_id)
        if not patient:
            return jsonify({'error': 'Patient record not found', 'not_found': True}), 404
        doctor = Doctor.query.get(appointment.doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor record not found', 'not_found': True}), 404
        
        # Use stored slot times (hour block start/end) directly
        return jsonify({
            'id': appointment.id,
            'patient_name': patient.name,
            'patient': {
                'phone': patient.phone,
                'age': patient.age,
                'gender': patient.gender
            },
            'doctor_name': doctor.name,
            'appointment_date': appointment.appointment_date.isoformat(),
            'slot_start_time': appointment.slot_start_time.strftime('%H:%M'),
            'slot_end_time':   appointment.slot_end_time.strftime('%H:%M'),
            'batch_number': appointment.batch_number or 1,
            'status': appointment.status,
            'reason': appointment.reason or 'General consultation',
            'created_at': appointment.created_at.isoformat() + 'Z'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting appointment details: {str(e)}")
        return jsonify({'error': 'Failed to load appointment details'}), 500


@api_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """Cancel an appointment."""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Check if appointment can be cancelled
        if appointment.status in ['completed', 'cancelled']:
            return jsonify({'error': 'Cannot cancel this appointment'}), 400
        
        appointment.status = 'cancelled'
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appointment cancelled successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error cancelling appointment: {str(e)}")
        return jsonify({'error': 'Failed to cancel appointment'}), 500


# =============================================================================
# PRE-APPOINTMENT TRIAGE API
# =============================================================================

@api_bp.route('/appointments/<int:appointment_id>/check-in', methods=['GET'])
def get_appointment_checkin(appointment_id):
    """Get appointment details for check-in page."""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found', 'not_found': True}), 404
        
        return jsonify({
            'success': True,
            'appointment': appointment.to_dict(),
            'triage_required': not appointment.triage_completed,
            'can_checkin': appointment.status == 'scheduled'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/appointments/<int:appointment_id>/triage', methods=['POST'])
def submit_appointment_triage(appointment_id):
    """Submit pre-appointment triage for a scheduled appointment."""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.status != 'scheduled':
            return jsonify({'error': 'Appointment is not in scheduled status'}), 400
        
        data = request.get_json()
        
        # Validate triage data
        symptoms = data.get('symptoms', [])
        chief_complaint = data.get('chief_complaint', '')
        vitals = data.get('vitals', {})
        
        if not chief_complaint:
            return jsonify({'error': 'Chief complaint is required'}), 400
        
        # Run triage engine to calculate priority
        # Map the available appointment checkin data to the full 15-field TriageInput format
        # using safe defaults for fields not collected on the patient-facing checkin form.
        
        # Parse blood pressure ("120/80" → systolic=120, diastolic=80)
        systolic_bp, diastolic_bp = 120, 80
        if vitals.get('blood_pressure'):
            try:
                bp_parts = str(vitals['blood_pressure']).split('/')
                if len(bp_parts) == 2:
                    systolic_bp = int(bp_parts[0].strip())
                    diastolic_bp = int(bp_parts[1].strip())
            except (ValueError, AttributeError):
                pass
        
        # Convert temperature from Fahrenheit to Celsius (form collects °F)
        temperature_c = 37.0  # normal default
        if vitals.get('temperature'):
            try:
                temp_f = float(vitals['temperature'])
                temperature_c = round((temp_f - 32) * 5 / 9, 1)
                # Clamp to valid range (30–45°C)
                temperature_c = max(30.0, min(45.0, temperature_c))
            except (ValueError, TypeError):
                pass
        
        # Heart rate from vitals, default 75 (normal)
        heart_rate = 75
        if vitals.get('heart_rate'):
            try:
                heart_rate = int(vitals['heart_rate'])
                heart_rate = max(20, min(300, heart_rate))
            except (ValueError, TypeError):
                pass
        
        # Map symptom duration string to hours
        duration_map = {
            'today': 4,
            '1-3days': 48,
            '4-7days': 120,
            '1-2weeks': 240,
            '2+weeks': 500,
            'chronic': 720,
        }
        symptom_duration_hours = duration_map.get(vitals.get('symptom_duration', ''), 24)
        
        # Derive pain level from symptoms (conservative estimates)
        chest_present = 'chest_pain' in symptoms
        breathing_difficulty = 'breathing_difficulty' in symptoms
        body_pain = 'body_pain' in symptoms
        pain_level = 7 if chest_present else (5 if body_pain else 0)
        pain_location = 'chest' if chest_present else ('body' if body_pain else 'general')
        
        # Build the 15-field input dict for validate_triage_input
        clinical_inputs = {
            'heart_rate': heart_rate,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'respiratory_rate': 18,          # not collected; use normal default
            'temperature': temperature_c,
            'consciousness_level': 'ALERT',  # patient is self-reporting → alert
            'pain_level': pain_level,
            'pain_location': pain_location,
            'chest_pain': chest_present,
            'difficulty_breathing': breathing_difficulty,
            'bleeding_severity': 'NONE',     # not collected
            'symptom_duration_hours': symptom_duration_hours,
            'is_pregnant': False,            # not collected; safe default
            'has_diabetes': False,           # not collected; safe default
            'has_heart_condition': False,    # not collected; safe default
        }
        
        is_valid, error_msg, validated_input = validate_triage_input(clinical_inputs)
        triage_reasons = []
        if not is_valid or validated_input is None:
            # Log the issue and fall back to GREEN priority rather than blocking check-in
            current_app.logger.warning(f"Triage input validation failed (appointment {appointment_id}): {error_msg} — defaulting to GREEN")
            priority = 'GREEN'
        else:
            triage_result = compute_triage(validated_input)
            priority = triage_result.priority.value if hasattr(triage_result.priority, 'value') else str(triage_result.priority)
            triage_reasons = [r.to_dict() if hasattr(r, 'to_dict') else str(r) for r in triage_result.reasons]
        
        # Save triage data
        appointment.triage_completed = True
        appointment.triage_data = {
            'symptoms': symptoms,
            'chief_complaint': chief_complaint,
            'vitals': vitals,
            'triage_reasons': triage_reasons,
            'submitted_at': datetime.utcnow().isoformat() + 'Z'
        }
        appointment.triage_priority = priority
        appointment.triage_completed_at = datetime.utcnow()
        appointment.status = 'checked_in'
        appointment.checked_in_at = datetime.utcnow()
        
        db.session.commit()
        
        # Broadcast to doctor's dashboard
        broadcast_event('appointment_checkin', {
            'appointment_id': appointment.id,
            'patient_name': appointment.patient.name,
            'priority': priority,
            'slot_time': appointment.slot_start_time.strftime('%H:%M')
        })
        
        return jsonify({
            'success': True,
            'message': 'Triage completed and checked in successfully',
            'priority': priority,
            'appointment_status': appointment.status
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting triage: {str(e)}")
        return jsonify({'error': 'Failed to submit triage'}), 500


@api_bp.route('/appointments/<int:appointment_id>/quick-checkin', methods=['POST'])
def quick_checkin(appointment_id):
    """Quick check-in without full triage (for simple appointments)."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        
        if appointment.status != 'scheduled':
            return jsonify({'error': 'Appointment is not in scheduled status'}), 400
        
        appointment.status = 'checked_in'
        appointment.checked_in_at = datetime.utcnow()
        
        db.session.commit()
        
        # Broadcast to doctor's dashboard
        broadcast_event('appointment_checkin', {
            'appointment_id': appointment.id,
            'patient_name': appointment.patient.name,
            'slot_time': appointment.slot_start_time.strftime('%H:%M')
        })
        
        return jsonify({
            'success': True,
            'message': 'Checked in successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to check in'}), 500


# =============================================================================
# DOCTOR'S APPOINTMENT QUEUE API
# =============================================================================

@api_bp.route('/doctor/appointments/today', methods=['GET'])
def get_doctor_appointments_today():
    """Get all appointments for a doctor for today, organized by type."""
    try:
        doctor_id = session.get('doctor_id')
        if not doctor_id:
            return jsonify({'error': 'Not authenticated as doctor'}), 401
        
        clinic_id = session.get('clinic_id')
        if not clinic_id:
            doctor_rec = Doctor.query.get(doctor_id)
            if doctor_rec:
                clinic_id = doctor_rec.clinic_id
                session['clinic_id'] = clinic_id
        
        today = ist_today_date()
        ist_start = ist_day_start_utc()
        ist_end = ist_start + timedelta(days=1)

        # Get all appointments for today
        appointments = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=today
        ).filter(
            Appointment.status.in_(['scheduled', 'checked_in', 'in_triage', 'ready', 'consulting'])
        ).order_by(
            Appointment.slot_start_time,
            Appointment.batch_number
        ).all()
        
        # Get walk-in patients for today (IST day boundary)
        walkins = Patient.query.filter_by(
            clinic_id=session.get('clinic_id')
        ).filter(
            Patient.status.in_(['Waiting', 'Consulting']),
            Patient.created_at >= ist_start,
            Patient.created_at < ist_end
        ).order_by(
            db.case(
                (Patient.priority == 'EMERGENCY', 0),
                (Patient.priority == 'RED', 1),
                (Patient.priority == 'AMBER', 2),
                (Patient.priority == 'GREEN', 3),
                else_=4
            ),
            Patient.created_at
        ).all()
        
        return jsonify({
            'success': True,
            'date': today.isoformat(),
            'appointments': [a.to_dict() for a in appointments],
            'walkins': [{
                'id': p.id,
                'name': p.name,
                'age': p.age,
                'gender': p.gender,
                'phone': p.phone,
                'priority': p.priority,
                'complaint': p.complaint,
                'status': p.status,
                'created_at': p.created_at.isoformat() + 'Z',
                'type': 'walkin'
            } for p in walkins],
            'summary': {
                'total_appointments': len(appointments),
                'checked_in': len([a for a in appointments if a.status == 'checked_in']),
                'waiting_triage': len([a for a in appointments if a.status == 'scheduled']),
                'total_walkins': len(walkins)
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting doctor appointments: {str(e)}")
        return jsonify({'error': 'Failed to load appointments'}), 500


@api_bp.route('/doctor/appointments', methods=['GET'])
def get_doctor_appointments():
    """Get appointments for a doctor with optional date range filter."""
    try:
        doctor_id = session.get('doctor_id')
        if not doctor_id:
            return jsonify({'error': 'Not authenticated as doctor'}), 401
        
        # Get query parameters
        from_date_str = request.args.get('from_date')
        to_date_str = request.args.get('to_date')
        status_filter = request.args.get('status')
        
        # Build query
        query = Appointment.query.filter_by(doctor_id=doctor_id)
        
        # Apply date filters
        if from_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date >= from_date)
        
        if to_date_str:
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date <= to_date)
        
        # Apply status filter
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # Order by date and time
        appointments = query.order_by(
            Appointment.appointment_date,
            Appointment.slot_start_time,
            Appointment.batch_number
        ).all()
        
        return jsonify({
            'success': True,
            'appointments': [a.to_dict() for a in appointments],
            'count': len(appointments)
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting doctor appointments: {str(e)}")
        return jsonify({'error': 'Failed to load appointments'}), 500


@api_bp.route('/doctor/unified-queue', methods=['GET'])
def get_unified_queue():
    """Get unified queue combining appointments and walk-ins, ordered by time/priority."""
    try:
        doctor_id = session.get('doctor_id')
        clinic_id = session.get('clinic_id')
        
        if not doctor_id:
            return jsonify({'error': 'Not authenticated as doctor'}), 401
        
        # Fallback: resolve clinic_id from doctor record if session is stale
        if not clinic_id:
            doctor_rec = Doctor.query.get(doctor_id)
            if doctor_rec:
                clinic_id = doctor_rec.clinic_id
                session['clinic_id'] = clinic_id
        
        today = ist_today_date()
        
        # Get slot configuration for balancing
        slot_config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
        walkin_ratio = (slot_config.walkin_slots_per_batch if slot_config else 2) / 5
        appointment_ratio = (slot_config.appointment_slots_per_batch if slot_config else 3) / 5
        
        unified_queue = []
        priority_order = {'EMERGENCY': 0, 'RED': 1, 'AMBER': 2, 'GREEN': 3}

        # Appointment patients with active appointment IDs (for walk-in dedup)
        appt_patient_ids = {
            pid for (pid,) in db.session.query(Appointment.patient_id).filter(
                Appointment.appointment_date == today,
                Appointment.status.notin_(['cancelled', 'no_show', 'completed'])
            ).distinct().all()
        }

        appointments = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=today
        ).filter(
            Appointment.status.in_(['scheduled', 'checked_in', 'consulting'])
        ).order_by(
            Appointment.slot_start_time
        ).all()
        
        for appt in appointments:
            # Use appointment triage_priority if set, else fall back to patient's walk-in priority
            effective_priority = appt.triage_priority or (appt.patient.priority if appt.patient else None) or 'GREEN'
            unified_queue.append({
                'id': appt.id,
                'patient_id': appt.patient_id,
                'type': 'appointment',
                'name': appt.patient.name,
                'age': appt.patient.age,
                'gender': appt.patient.gender,
                'phone': appt.patient.phone,
                'priority': effective_priority,
                'complaint': appt.triage_data.get('chief_complaint') if appt.triage_data else appt.reason,
                'triage_data': appt.triage_data,
                'slot_time': appt.slot_start_time.strftime('%H:%M'),
                'status': appt.status,
                'triage_priority': effective_priority,
                'checked_in_at': (appt.checked_in_at.isoformat() + 'Z') if appt.checked_in_at else None,
                'sort_key': (
                    0 if appt.status == 'consulting' else 1,
                    priority_order.get(effective_priority, 3),
                    appt.slot_start_time.hour * 60 + appt.slot_start_time.minute
                )
            })
        
        # Get walk-in patients — no date restriction, exclude appointment patients
        walkins = [
            w for w in Patient.query.filter_by(clinic_id=clinic_id).filter(
                Patient.status.in_(['Waiting', 'Consulting'])
            ).all()
            if w.id not in appt_patient_ids
        ]
        
        for walkin in walkins:
            unified_queue.append({
                'id': walkin.id,
                'patient_id': walkin.id,
                'type': 'walkin',
                'name': walkin.name,
                'age': walkin.age,
                'gender': walkin.gender,
                'phone': walkin.phone,
                'priority': walkin.priority,
                'complaint': walkin.complaint,
                'triage_data': walkin.clinical_data,
                'slot_time': None,
                'status': walkin.status,
                'triage_priority': walkin.priority,
                'checked_in_at': walkin.created_at.isoformat() + 'Z',
                'sort_key': (
                    0 if walkin.status == 'Consulting' else 1,
                    priority_order.get(walkin.priority, 4),
                    walkin.created_at.hour * 60 + walkin.created_at.minute
                )
            })
        
        # Sort: Consulting first, then by priority, then by time
        unified_queue.sort(key=lambda x: x['sort_key'])
        
        return jsonify({
            'success': True,
            'queue': unified_queue,
            'balance': {
                'walkin_ratio': walkin_ratio,
                'appointment_ratio': appointment_ratio
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting unified queue: {str(e)}")
        return jsonify({'error': 'Failed to load queue'}), 500


@api_bp.route('/doctor/call-next', methods=['POST'])
def call_next_patient():
    """Smart call next patient based on appointment/walk-in balance."""
    try:
        doctor_id = session.get('doctor_id')
        clinic_id = session.get('clinic_id')
        
        if not doctor_id:
            return jsonify({'error': 'Not authenticated as doctor'}), 401
        
        # Fallback: resolve clinic_id from doctor record if session is stale
        if not clinic_id:
            doctor_rec = Doctor.query.get(doctor_id)
            if doctor_rec:
                clinic_id = doctor_rec.clinic_id
                session['clinic_id'] = clinic_id
        
        data = request.get_json() or {}
        patient_type = data.get('type')  # 'appointment', 'walkin', or None for auto
        patient_id = data.get('id')  # Specific patient/appointment ID
        
        today = ist_today_date()
        
        # If specific patient requested (type + id)
        if patient_type and patient_id:
            if patient_type == 'appointment':
                appt = Appointment.query.get(patient_id)
                if not appt:
                    return jsonify({'success': False, 'message': 'Appointment not found'})
                if appt.status == 'consulting':
                    return jsonify({'success': True, 'called': {'type': 'appointment', 'id': patient_id, 'name': appt.patient.name, 'already_consulting': True}})
                if appt.status == 'checked_in':
                    appt.status = 'consulting'
                    if appt.patient and appt.patient.status != 'Consulting':
                        appt.patient.status = 'Consulting'
                        appt.patient.updated_at = datetime.utcnow()
                    db.session.commit()
                    broadcast_event('patient_called', {'appointment_id': patient_id, 'type': 'appointment'})
                    if appt.patient:
                        broadcast_event('status_change', appt.patient.to_dict())
                    return jsonify({'success': True, 'called': {'type': 'appointment', 'id': patient_id, 'name': appt.patient.name}})
                return jsonify({'success': False, 'message': f'Cannot call: appointment is "{appt.status}" — check in the patient first'})
            else:  # walkin
                patient = Patient.query.get(patient_id)
                if not patient:
                    return jsonify({'success': False, 'message': 'Patient not found'})
                if patient.status == 'Consulting':
                    return jsonify({'success': True, 'called': {'type': 'walkin', 'id': patient_id, 'name': patient.name, 'already_consulting': True}})
                if patient.status == 'Waiting':
                    patient.status = 'Consulting'
                    db.session.commit()
                    broadcast_event('patient_called', {'patient_id': patient_id, 'type': 'walkin'})
                    broadcast_event('status_change', patient.to_dict())
                    return jsonify({'success': True, 'called': {'type': 'walkin', 'id': patient_id, 'name': patient.name}})
                return jsonify({'success': False, 'message': f'Cannot call: patient status is "{patient.status}"'})
        
        # If only type specified (no id) — force that patient type without ratio logic
        if patient_type and not patient_id:
            if patient_type == 'appointment':
                # Prefer checked_in first, fall back to scheduled
                next_appt = Appointment.query.filter_by(
                    doctor_id=doctor_id, appointment_date=today
                ).filter(
                    Appointment.status.in_(['checked_in', 'scheduled'])
                ).order_by(
                    db.case(
                        (Appointment.status == 'checked_in', 0),
                        (Appointment.status == 'scheduled', 1),
                        else_=2
                    ),
                    Appointment.slot_start_time
                ).first()
                if next_appt:
                    next_appt.status = 'consulting'
                    if next_appt.patient and next_appt.patient.status != 'Consulting':
                        next_appt.patient.status = 'Consulting'
                        next_appt.patient.updated_at = datetime.utcnow()
                    db.session.commit()
                    broadcast_event('patient_called', {'appointment_id': next_appt.id, 'type': 'appointment'})
                    if next_appt.patient:
                        broadcast_event('status_change', next_appt.patient.to_dict())
                    return jsonify({'success': True, 'called': {'type': 'appointment', 'id': next_appt.id, 'name': next_appt.patient.name}})
                return jsonify({'success': False, 'message': 'No pending appointments for today'})
            elif patient_type in ('walkin', 'walkins'):
                next_walkin = Patient.query.filter_by(
                    clinic_id=clinic_id, status='Waiting'
                ).order_by(
                    db.case(
                        (Patient.priority == 'EMERGENCY', 0),
                        (Patient.priority == 'RED', 1),
                        (Patient.priority == 'AMBER', 2),
                        (Patient.priority == 'GREEN', 3),
                        else_=4
                    ),
                    Patient.created_at
                ).first()
                if next_walkin:
                    next_walkin.status = 'Consulting'
                    db.session.commit()
                    broadcast_event('patient_called', {'patient_id': next_walkin.id, 'type': 'walkin'})
                    broadcast_event('status_change', next_walkin.to_dict())
                    return jsonify({'success': True, 'called': {'type': 'walkin', 'id': next_walkin.id, 'name': next_walkin.name}})
                return jsonify({'success': False, 'message': 'No walk-in patients waiting'})
        
        # Auto-select based on balance and priority
        slot_config = SlotConfiguration.query.filter_by(doctor_id=doctor_id).first()
        walkin_slots = slot_config.walkin_slots_per_batch if slot_config else 2
        appt_slots = slot_config.appointment_slots_per_batch if slot_config else 3
        
        # Count how many of each type currently consulting
        consulting_appts = Appointment.query.filter_by(doctor_id=doctor_id, appointment_date=today, status='consulting').count()
        # Keep walk-in scope consistent with queue endpoints (no same-day restriction).
        consulting_walkins = Patient.query.filter_by(clinic_id=clinic_id, status='Consulting').count()
        
        # Check for emergency walk-ins first
        emergency_walkin = Patient.query.filter_by(
            clinic_id=clinic_id, status='Waiting', priority='EMERGENCY'
        ).first()
        
        if emergency_walkin:
            emergency_walkin.status = 'Consulting'
            db.session.commit()
            broadcast_event('patient_called', {'patient_id': emergency_walkin.id, 'type': 'walkin', 'priority': 'EMERGENCY'})
            broadcast_event('status_change', emergency_walkin.to_dict())
            return jsonify({'success': True, 'called': {'type': 'walkin', 'id': emergency_walkin.id, 'name': emergency_walkin.name, 'priority': 'EMERGENCY'}})
        
        # Decide based on ratio
        should_call_appointment = (consulting_appts / max(appt_slots, 1)) <= (consulting_walkins / max(walkin_slots, 1))
        
        if should_call_appointment:
            # Try to call appointment first
            next_appt = Appointment.query.filter_by(
                doctor_id=doctor_id, appointment_date=today, status='checked_in'
            ).order_by(Appointment.slot_start_time).first()
            
            if next_appt:
                next_appt.status = 'consulting'
                if next_appt.patient and next_appt.patient.status != 'Consulting':
                    next_appt.patient.status = 'Consulting'
                    next_appt.patient.updated_at = datetime.utcnow()
                db.session.commit()
                broadcast_event('patient_called', {'appointment_id': next_appt.id, 'type': 'appointment'})
                if next_appt.patient:
                    broadcast_event('status_change', next_appt.patient.to_dict())
                return jsonify({'success': True, 'called': {'type': 'appointment', 'id': next_appt.id, 'name': next_appt.patient.name}})
        
        # Call walk-in by priority
        next_walkin = Patient.query.filter_by(
            clinic_id=clinic_id, status='Waiting'
        ).order_by(
            db.case(
                (Patient.priority == 'EMERGENCY', 0),
                (Patient.priority == 'RED', 1),
                (Patient.priority == 'AMBER', 2),
                (Patient.priority == 'GREEN', 3),
                else_=4
            ),
            Patient.created_at
        ).first()
        
        if next_walkin:
            next_walkin.status = 'Consulting'
            db.session.commit()
            broadcast_event('patient_called', {'patient_id': next_walkin.id, 'type': 'walkin'})
            broadcast_event('status_change', next_walkin.to_dict())
            return jsonify({'success': True, 'called': {'type': 'walkin', 'id': next_walkin.id, 'name': next_walkin.name}})
        
        # If no walk-in, try appointment again
        next_appt = Appointment.query.filter_by(
            doctor_id=doctor_id, appointment_date=today, status='checked_in'
        ).order_by(Appointment.slot_start_time).first()
        
        if next_appt:
            next_appt.status = 'consulting'
            if next_appt.patient and next_appt.patient.status != 'Consulting':
                next_appt.patient.status = 'Consulting'
                next_appt.patient.updated_at = datetime.utcnow()
            db.session.commit()
            broadcast_event('patient_called', {'appointment_id': next_appt.id, 'type': 'appointment'})
            if next_appt.patient:
                broadcast_event('status_change', next_appt.patient.to_dict())
            return jsonify({'success': True, 'called': {'type': 'appointment', 'id': next_appt.id, 'name': next_appt.patient.name}})
        
        return jsonify({'success': False, 'message': 'No patients waiting'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error calling next patient: {str(e)}")
        return jsonify({'error': 'Failed to call next patient'}), 500


# =============================================================================
# UPCOMING APPOINTMENTS (for reminder system)
# =============================================================================

@api_bp.route('/appointments/upcoming', methods=['GET'])
def get_upcoming_appointments():
    """Get appointments that are coming up in the next X minutes (for reminders)."""
    try:
        minutes_ahead = request.args.get('minutes', 15, type=int)
        
        now = datetime.now(tz=_IST).replace(tzinfo=None)
        today = ist_today_date()
        current_time = now.time()
        cutoff_time = (now + timedelta(minutes=minutes_ahead)).time()
        
        # Find appointments within the time window
        upcoming = Appointment.query.filter(
            Appointment.appointment_date == today,
            Appointment.status == 'scheduled',
            Appointment.slot_start_time >= current_time,
            Appointment.slot_start_time <= cutoff_time,
            Appointment.reminder_sent == False
        ).all()
        
        return jsonify({
            'success': True,
            'count': len(upcoming),
            'appointments': [a.to_dict() for a in upcoming]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/appointments/<int:appointment_id>/mark-reminded', methods=['POST'])
def mark_appointment_reminded(appointment_id):
    """Mark an appointment as having received reminder."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        appointment.reminder_sent = True
        appointment.reminder_sent_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
