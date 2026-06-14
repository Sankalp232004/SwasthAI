"""
Superadmin Routes - Clinic Management & Full Access
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from app import db
from models import SuperAdmin, Clinic, Patient, Doctor, AuditLog, RegistrationToken, SystemSetting
from datetime import datetime, timedelta
from functools import wraps
import secrets
import string
from qr_generator import generate_clinic_qr, get_clinic_url

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')


def get_app_base_url():
    """Return the configured app base URL for use in QR codes and links.
    Priority: (1) request ?base_url param, (2) stored SystemSetting,
    (3) APP_BASE_URL config, (4) request.host_url.
    """
    override = request.args.get('base_url', '').strip()
    if override:
        return override.rstrip('/')
    stored = SystemSetting.get('base_url', '').strip()
    if stored:
        return stored.rstrip('/')
    configured = (current_app.config.get('APP_BASE_URL') or '').strip()
    if configured:
        return configured.rstrip('/')
    return request.host_url.rstrip('/')

# ==================== AUTHENTICATION DECORATOR ====================
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'superadmin_id' not in session:
            return redirect(url_for('superadmin.login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTH ROUTES ====================
@superadmin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('superadmin/login.html')
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    superadmin = SuperAdmin.query.filter_by(email=email, is_active=True).first()
    
    if superadmin and superadmin.check_password(password):
        session['superadmin_id'] = superadmin.id
        session['superadmin_name'] = superadmin.name
        session['is_super'] = superadmin.is_super
        
        superadmin.last_login = datetime.utcnow()
        
        # Log
        log = AuditLog(
            actor_type='superadmin',
            actor_id=superadmin.id,
            actor_name=superadmin.name,
            action='login',
            entity_type='superadmin',
            entity_id=superadmin.id,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@superadmin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('superadmin.login'))


# ==================== DASHBOARD ====================
@superadmin_bp.route('/dashboard')
@superadmin_required
def dashboard():
    # Statistics
    stats = {
        'total_clinics': Clinic.query.count(),
        'active_clinics': Clinic.query.filter_by(is_active=True).count(),
        'total_patients': Patient.query.count(),
        'total_doctors': Doctor.query.count(),
        'today_patients': Patient.query.filter(
            Patient.created_at >= datetime.utcnow().date()
        ).count()
    }
    
    # Recent clinics
    recent_clinics = Clinic.query.order_by(Clinic.created_at.desc()).limit(10).all()
    
    # Recent activity
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    
    return render_template('superadmin/dashboard.html', 
                         stats=stats, 
                         recent_clinics=recent_clinics,
                         recent_logs=recent_logs)


# ==================== CLINIC MANAGEMENT ====================
@superadmin_bp.route('/clinics')
@superadmin_required
def clinics():
    return render_template('superadmin/clinics.html')


@superadmin_bp.route('/api/clinics', methods=['GET'])
@superadmin_required
def api_get_clinics():
    clinics = Clinic.query.order_by(Clinic.created_at.desc()).all()
    return jsonify([c.to_dict() for c in clinics])


@superadmin_bp.route('/api/clinics', methods=['POST'])
@superadmin_required
def api_create_clinic():
    data = request.json
    
    # Generate slug from name
    slug = data['name'].lower().replace(' ', '-').replace('_', '-')
    # Remove special characters
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    
    # Check if slug exists
    if Clinic.query.filter_by(slug=slug).first():
        slug = f"{slug}-{Clinic.query.count() + 1}"
    
    clinic = Clinic(
        name=data['name'],
        slug=slug,
        address=data.get('address'),
        phone=data.get('phone'),
        email=data.get('email'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        max_doctors=data.get('max_doctors', 5),
        max_patients_per_day=data.get('max_patients_per_day', 100),
        subscription_status=data.get('subscription_status', 'trial'),
        subscription_expiry=datetime.utcnow() + timedelta(days=30)
    )
    
    db.session.add(clinic)
    db.session.commit()
    
    # Generate a random secure password for the clinic admin
    alphabet = string.ascii_letters + string.digits
    admin_password = ''.join(secrets.choice(alphabet) for _ in range(12))
    
    # Create default admin doctor for this clinic
    admin_email = data.get('email') or f"admin@{slug}.com"
    
    # Check if email already exists
    if Doctor.query.filter_by(email=admin_email).first():
        admin_email = f"admin-{clinic.id}@{slug}.com"
    
    admin_doctor = Doctor(
        clinic_id=clinic.id,
        name=f"{clinic.name} Admin",
        email=admin_email,
        phone=data.get('phone'),
        specialization='Administrator',
        is_active=True
    )
    admin_doctor.set_password(admin_password)
    
    db.session.add(admin_doctor)
    db.session.commit()

    # Create registration token for admin doctor (used in setup link)
    setup_token = secrets.token_urlsafe(32)
    reg_token = RegistrationToken(
        clinic_id=clinic.id,
        doctor_id=admin_doctor.id,
        token=setup_token,
        email=admin_email,
        temp_password=admin_password,
        token_type='password_setup',
        expires_at=datetime.utcnow() + timedelta(days=7),
        created_by=session['superadmin_id']
    )
    db.session.add(reg_token)
    db.session.commit()

    # Log
    log = AuditLog(
        clinic_id=clinic.id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='create_clinic',
        entity_type='clinic',
        entity_id=clinic.id,
        details={
            'clinic_name': clinic.name,
            'admin_email': admin_email,
            'admin_created': True
        }
    )
    db.session.add(log)
    db.session.commit()
    
    # Return clinic info with admin credentials
    result = clinic.to_dict()
    result['admin_credentials'] = {
        'email': admin_email,
        'password': admin_password,
        'setup_link': f'/doctor/setup-password/{setup_token}',
        'login_url': f'/doctor/login'
    }
    
    return jsonify(result), 201


@superadmin_bp.route('/api/clinics/<int:clinic_id>', methods=['PUT'])
@superadmin_required
def api_update_clinic(clinic_id):
    clinic = Clinic.query.get_or_404(clinic_id)
    data = request.json
    
    clinic.name = data.get('name', clinic.name)
    clinic.address = data.get('address', clinic.address)
    clinic.phone = data.get('phone', clinic.phone)
    clinic.email = data.get('email', clinic.email)
    if 'latitude' in data:
        clinic.latitude = data['latitude']
    if 'longitude' in data:
        clinic.longitude = data['longitude']
    clinic.max_doctors = data.get('max_doctors', clinic.max_doctors)
    clinic.max_patients_per_day = data.get('max_patients_per_day', clinic.max_patients_per_day)
    clinic.subscription_status = data.get('subscription_status', clinic.subscription_status)
    
    db.session.commit()
    
    # Log
    log = AuditLog(
        clinic_id=clinic.id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='update_clinic',
        entity_type='clinic',
        entity_id=clinic.id,
        details={'clinic_name': clinic.name, 'changes': data}
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(clinic.to_dict())


@superadmin_bp.route('/api/clinics/<int:clinic_id>/toggle-status', methods=['POST'])
@superadmin_required
def api_toggle_clinic_status(clinic_id):
    clinic = Clinic.query.get_or_404(clinic_id)
    clinic.is_active = not clinic.is_active
    db.session.commit()
    
    # Log
    log = AuditLog(
        clinic_id=clinic.id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='toggle_clinic_status',
        entity_type='clinic',
        entity_id=clinic.id,
        details={'new_status': 'active' if clinic.is_active else 'inactive'}
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(clinic.to_dict())


@superadmin_bp.route('/api/clinics/<int:clinic_id>', methods=['DELETE'])
@superadmin_required
def api_delete_clinic(clinic_id):
    from models import ClinicHours, SlotConfiguration, Appointment
    from sqlalchemy import text
    
    clinic = db.session.get(Clinic, clinic_id)
    if clinic is None:
        return jsonify({'error': 'Clinic not found'}), 404
    
    clinic_name = clinic.name
    
    try:
        # Delete everything via raw SQL in dependency order to avoid FK violations
        db.session.execute(text('UPDATE audit_logs SET clinic_id = NULL WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM appointments WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM clinic_hours WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM slot_configurations WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM otp_records WHERE clinic_id = :cid'), {'cid': clinic_id})
        # registration_tokens references both clinic_id AND doctor_id — must go before doctors/patients
        db.session.execute(text('DELETE FROM registration_tokens WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM doctors WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM patients WHERE clinic_id = :cid'), {'cid': clinic_id})
        db.session.execute(text('DELETE FROM clinics WHERE id = :cid'), {'cid': clinic_id})
        db.session.commit()
        
        # Log (clinic_id left NULL since clinic is gone)
        log = AuditLog(
            actor_type='superadmin',
            actor_id=session['superadmin_id'],
            actor_name=session['superadmin_name'],
            action='delete_clinic',
            entity_type='clinic',
            entity_id=clinic_id,
            details={'clinic_name': clinic_name}
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete clinic: {str(e)}'}), 500


@superadmin_bp.route('/api/clinics/<int:clinic_id>/qr', methods=['GET'])
@superadmin_required
def api_get_clinic_qr(clinic_id):
    """Generate QR code for clinic registration page."""
    clinic = Clinic.query.get_or_404(clinic_id)

    base_url = get_app_base_url()

    # Generate QR code as base64 image
    qr_code = generate_clinic_qr(clinic.slug, base_url)
    registration_url = get_clinic_url(clinic.slug, base_url)

    return jsonify({
        'success': True,
        'qr_code': qr_code,
        'registration_url': registration_url,
        'clinic_name': clinic.name,
        'clinic_slug': clinic.slug
    })


@superadmin_bp.route('/api/clinics/<slug>/qr-code', methods=['GET'])
@superadmin_required
def download_clinic_qr(slug):
    """Download QR code as PNG file."""
    from io import BytesIO
    import qrcode
    from flask import send_file
    
    clinic = Clinic.query.filter_by(slug=slug).first_or_404()

    base_url = get_app_base_url()
    registration_url = get_clinic_url(clinic.slug, base_url)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(
        img_io,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'{clinic.name}_QR_Code.png'
    )


# ==================== NETWORK SETTINGS ====================
@superadmin_bp.route('/api/settings/base-url', methods=['GET'])
@superadmin_required
def api_get_base_url():
    """Get the configured app base URL for QR codes and shared links."""
    stored = SystemSetting.get('base_url', '').strip()
    configured = (current_app.config.get('APP_BASE_URL') or '').strip()
    return jsonify({
        'base_url': stored or configured or request.host_url.rstrip('/'),
        'is_configured': bool(stored),
        'current_host': request.host_url.rstrip('/')
    })


@superadmin_bp.route('/api/settings/base-url', methods=['PUT'])
@superadmin_required
def api_set_base_url():
    """Save the app base URL (e.g. http://192.168.1.5:5010) for QR codes."""
    data = request.json or {}
    url = data.get('base_url', '').strip().rstrip('/')
    if not url:
        return jsonify({'error': 'base_url is required'}), 400
    if not url.startswith('http'):
        return jsonify({'error': 'base_url must start with http:// or https://'}), 400
    SystemSetting.set('base_url', url)
    return jsonify({'success': True, 'base_url': url})


@superadmin_bp.route('/api/settings/tunnel-url', methods=['GET'])
@superadmin_required
def api_get_tunnel_url():
    """Return the configured public URL from system settings."""
    stored = SystemSetting.get('base_url', '').strip()
    if stored and stored.startswith('https://'):
        return jsonify({'url': stored, 'found': True})
    return jsonify({'url': None, 'found': False})


@superadmin_bp.route('/api/geocode', methods=['GET'])
@superadmin_required
def api_geocode():
    """Backend geocoding proxy. Uses Photon (primary) then Nominatim (fallback).
    Photon has no rate limits and no auth requirement.
    Nominatim is a backup for addresses Photon cannot resolve.
    """
    import urllib.request as ureq
    import urllib.parse as uparse
    import json as _json
    address = request.args.get('address', '').strip()
    if not address:
        return jsonify({'error': 'address parameter required'}), 400

    def _photon(addr):
        """Photon geocoder – Komoot open server, no key, generous limits."""
        url = ('https://photon.komoot.io/api/?q=' + uparse.quote(addr) + '&limit=3&lang=en')
        req = ureq.Request(url, headers={'User-Agent': 'SwasthAI-CRM/1.0'})
        with ureq.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
        features = data.get('features', [])
        if not features:
            return None
        f = features[0]
        coords = f['geometry']['coordinates']  # [lon, lat]
        props = f.get('properties', {})
        parts = [props.get('name'), props.get('street'), props.get('city'),
                 props.get('state'), props.get('country')]
        display = ', '.join(p for p in parts if p)
        return {'found': True, 'lat': float(coords[1]), 'lon': float(coords[0]),
                'display_name': display or addr}

    def _nominatim(addr):
        """Nominatim fallback."""
        url = ('https://nominatim.openstreetmap.org/search?q=' +
               uparse.quote(addr) + '&format=json&limit=3&addressdetails=1')
        req = ureq.Request(url, headers={
            'User-Agent': 'SwasthAI-CRM/1.0 (contact@swasthai.in)',
            'Accept-Language': 'en'
        })
        with ureq.urlopen(req, timeout=8) as resp:
            results = _json.loads(resp.read())
        if not results:
            return None
        top = results[0]
        return {'found': True, 'lat': float(top['lat']), 'lon': float(top['lon']),
                'display_name': top.get('display_name', '')}

    # Try Photon first, then Nominatim
    for _fn in (_photon, _nominatim):
        try:
            result = _fn(address)
            if result:
                return jsonify(result)
        except Exception:
            continue

    return jsonify({'found': False})


@superadmin_bp.route('/api/recent-activity', methods=['GET'])
@superadmin_required
def api_recent_activity():
    """Return the 20 most recent audit log entries as JSON (UTC ISO timestamps)."""
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    return jsonify([{
        'id': log.id,
        'actor_name': log.actor_name or 'System',
        'actor_type': log.actor_type or 'system',
        'action': log.action.replace('_', ' '),
        'entity_type': log.entity_type or '',
        'timestamp': log.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
    } for log in logs])


# ==================== PATIENT MANAGEMENT ====================
@superadmin_bp.route('/patients')
@superadmin_required
def patients():
    return render_template('superadmin/patients.html')


@superadmin_bp.route('/api/patients', methods=['GET'])
@superadmin_required
def api_get_patients():
    clinic_id = request.args.get('clinic_id', type=int)
    phone = request.args.get('phone')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = Patient.query
    
    if clinic_id:
        query = query.filter_by(clinic_id=clinic_id)
    
    if phone:
        query = query.filter(Patient.phone.like(f'%{phone}%'))
    
    pagination = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'patients': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@superadmin_bp.route('/api/patients/history/<phone>', methods=['GET'])
@superadmin_required
def api_patient_history(phone):
    """Get patient history across all clinics, with optional clinic + date filters."""
    from datetime import date as date_type
    clinic_id  = request.args.get('clinic_id',  type=int)
    date_from  = request.args.get('date_from')   # YYYY-MM-DD
    date_to    = request.args.get('date_to')     # YYYY-MM-DD

    query = Patient.query.filter_by(phone=phone)

    if clinic_id:
        query = query.filter_by(clinic_id=clinic_id)

    if date_from:
        try:
            df = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Patient.created_at >= df)
        except ValueError:
            pass

    if date_to:
        try:
            dt_end = datetime.strptime(date_to, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query = query.filter(Patient.created_at <= dt_end)
        except ValueError:
            pass

    patients = query.order_by(Patient.created_at.desc()).all()

    # Build clinic_id → name lookup (single query, no N+1)
    clinic_ids = list({p.clinic_id for p in patients})
    clinic_map = {c.id: c.name for c in Clinic.query.filter(Clinic.id.in_(clinic_ids)).all()}

    visits = []
    for p in patients:
        d = p.to_dict()
        d['clinic_name']    = clinic_map.get(p.clinic_id, f'Clinic {p.clinic_id}')
        d['chief_complaint'] = p.complaint
        d['severity']       = p.priority.lower() if p.priority else 'unknown'
        visits.append(d)

    return jsonify({
        'phone':        phone,
        'total_visits': len(visits),
        'visits':       visits
    })


@superadmin_bp.route('/api/patients/<int:patient_id>', methods=['DELETE'])
@superadmin_required
def api_delete_patient(patient_id):
    from sqlalchemy import text
    patient = Patient.query.get_or_404(patient_id)
    patient_name = patient.name
    patient_phone = patient.phone
    clinic_id = patient.clinic_id
    patient_id_val = patient.id
    
    try:
        # appointments.patient_id FK must be removed first
        db.session.execute(text('DELETE FROM appointments WHERE patient_id = :pid'), {'pid': patient_id_val})
        db.session.execute(text('DELETE FROM patients WHERE id = :pid'), {'pid': patient_id_val})
        db.session.commit()
        
        log = AuditLog(
            clinic_id=clinic_id,
            actor_type='superadmin',
            actor_id=session['superadmin_id'],
            actor_name=session['superadmin_name'],
            action='delete_patient',
            entity_type='patient',
            entity_id=patient_id_val,
            details={'patient_name': patient_name, 'phone': patient_phone}
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete patient: {str(e)}'}), 500

# ==================== REGISTRATION TOKEN MANAGEMENT ====================
@superadmin_bp.route('/api/clinics/<int:clinic_id>/tokens', methods=['GET'])
@superadmin_required
def api_get_clinic_tokens(clinic_id):
    """Get all doctor password setup tokens for a clinic."""
    tokens = RegistrationToken.query.filter_by(clinic_id=clinic_id).order_by(RegistrationToken.created_at.desc()).all()
    
    # Add full URL to each token
    tokens_data = []
    for t in tokens:
        token_dict = t.to_dict()
        token_dict['setup_url'] = f"{get_app_base_url()}/doctor/setup-password/{t.token}"
        tokens_data.append(token_dict)
    
    return jsonify(tokens_data)


# ==================== DOCTOR MANAGEMENT API ====================
@superadmin_bp.route('/api/clinics/<int:clinic_id>/doctors', methods=['GET'])
@superadmin_required
def api_get_clinic_doctors(clinic_id):
    """Get all doctors for a clinic."""
    doctors = Doctor.query.filter_by(clinic_id=clinic_id).all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'email': d.email,
        'specialization': d.specialization,
        'is_active': d.is_active,
        'created_at': d.created_at.isoformat()
    } for d in doctors])


@superadmin_bp.route('/api/clinics/<int:clinic_id>/doctors', methods=['POST'])
@superadmin_required
def api_create_doctor(clinic_id):
    """Create a new doctor for a clinic."""
    clinic = Clinic.query.get_or_404(clinic_id)
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    specialization = data.get('specialization', '')
    
    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    # Check if email already exists
    existing = Doctor.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'A doctor with this email already exists'}), 400
    
    # Create doctor
    doctor = Doctor(
        clinic_id=clinic_id,
        name=name,
        email=email,
        specialization=specialization,
        is_active=True
    )
    doctor.set_password(password)
    
    db.session.add(doctor)
    db.session.commit()
    
    # Log action
    log = AuditLog(
        clinic_id=clinic_id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='create_doctor',
        entity_type='doctor',
        entity_id=doctor.id,
        details={
            'clinic_id': clinic_id,
            'clinic_name': clinic.name,
            'doctor_name': doctor.name,
            'doctor_email': doctor.email
        }
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'doctor': {
            'id': doctor.id,
            'name': doctor.name,
            'email': doctor.email,
            'specialization': doctor.specialization
        }
    }), 201


@superadmin_bp.route('/api/clinics/<int:clinic_id>/doctors/<int:doctor_id>/toggle', methods=['POST'])
@superadmin_required
def api_toggle_doctor(clinic_id, doctor_id):
    """Toggle doctor active status."""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if doctor.clinic_id != clinic_id:
        return jsonify({'error': 'Doctor does not belong to this clinic'}), 400
    
    doctor.is_active = not doctor.is_active
    db.session.commit()
    
    # Log action
    log = AuditLog(
        clinic_id=clinic_id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='toggle_doctor',
        entity_type='doctor',
        entity_id=doctor.id,
        details={'is_active': doctor.is_active}
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'is_active': doctor.is_active})


@superadmin_bp.route('/api/clinics/<int:clinic_id>/doctors/<int:doctor_id>', methods=['DELETE'])
@superadmin_required
def api_delete_doctor(clinic_id, doctor_id):
    """Delete a doctor."""
    from sqlalchemy import text
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if doctor.clinic_id != clinic_id:
        return jsonify({'error': 'Doctor does not belong to this clinic'}), 400
    
    doctor_name = doctor.name
    doctor_email = doctor.email
    doctor_id_val = doctor.id
    
    try:
        # Clear all FK references to this doctor before deleting
        db.session.execute(text('UPDATE patients SET doctor_id = NULL WHERE doctor_id = :did'), {'did': doctor_id_val})
        db.session.execute(text('DELETE FROM registration_tokens WHERE doctor_id = :did'), {'did': doctor_id_val})
        db.session.execute(text('DELETE FROM appointments WHERE doctor_id = :did'), {'did': doctor_id_val})
        db.session.execute(text('DELETE FROM slot_configurations WHERE doctor_id = :did'), {'did': doctor_id_val})
        db.session.execute(text('DELETE FROM clinic_hours WHERE doctor_id = :did'), {'did': doctor_id_val})
        db.session.execute(text('DELETE FROM doctors WHERE id = :did'), {'did': doctor_id_val})
        db.session.commit()
        
        log = AuditLog(
            clinic_id=clinic_id,
            actor_type='superadmin',
            actor_id=session['superadmin_id'],
            actor_name=session['superadmin_name'],
            action='delete_doctor',
            entity_type='doctor',
            entity_id=doctor_id_val,
            details={'doctor_name': doctor_name, 'doctor_email': doctor_email}
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete doctor: {str(e)}'}), 500


@superadmin_bp.route('/api/clinics/<int:clinic_id>/doctors/<int:doctor_id>/generate-token', methods=['POST'])
@superadmin_required
def api_generate_doctor_password_token(clinic_id, doctor_id):
    """Generate a password setup token for a doctor."""
    clinic = Clinic.query.get_or_404(clinic_id)
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if doctor.clinic_id != clinic_id:
        return jsonify({'error': 'Doctor does not belong to this clinic'}), 400
    
    # Generate secure random token
    token = secrets.token_urlsafe(32)
    
    # Generate temporary password (8 chars: letters + digits)
    temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    
    # Parse expiry (default 7 days)
    data = request.json or {}
    expiry_days = data.get('expiry_days', 7)
    expires_at = datetime.utcnow() + timedelta(days=expiry_days)
    
    # Check if there's already an unused token for this doctor
    existing_token = RegistrationToken.query.filter_by(
        doctor_id=doctor_id, 
        is_used=False
    ).first()
    
    if existing_token and existing_token.is_active:
        # Deactivate old token
        existing_token.is_active = False
    
    # Create new token
    reg_token = RegistrationToken(
        clinic_id=clinic_id,
        doctor_id=doctor_id,
        token=token,
        email=doctor.email,
        temp_password=temp_password,
        token_type='password_setup',
        expires_at=expires_at,
        created_by=session['superadmin_id']
    )
    
    db.session.add(reg_token)
    db.session.commit()
    
    # Log action
    log = AuditLog(
        clinic_id=clinic_id,
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='generate_doctor_password_token',
        entity_type='registration_token',
        entity_id=reg_token.id,
        details={
            'clinic_id': clinic_id,
            'clinic_name': clinic.name,
            'doctor_id': doctor_id,
            'doctor_name': doctor.name,
            'doctor_email': doctor.email,
            'expires_at': reg_token.expires_at.isoformat()
        }
    )
    db.session.add(log)
    db.session.commit()
    
    # Return token with full URL
    return jsonify({
        'token': token,
        'temp_password': temp_password,
        'setup_url': f"{get_app_base_url()}/doctor/setup-password/{token}",
        'email': doctor.email,
        'doctor_name': doctor.name,
        'expires_at': reg_token.expires_at.isoformat()
    }), 201


@superadmin_bp.route('/api/tokens/<int:token_id>/toggle', methods=['POST'])
@superadmin_required
def api_toggle_token(token_id):
    """Activate/deactivate a registration token."""
    token = RegistrationToken.query.get_or_404(token_id)
    token.is_active = not token.is_active
    db.session.commit()
    
    # Log action
    log = AuditLog(
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='toggle_registration_token',
        entity_type='registration_token',
        entity_id=token.id,
        details={'is_active': token.is_active}
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(token.to_dict())


@superadmin_bp.route('/api/tokens/<int:token_id>', methods=['DELETE'])
@superadmin_required
def api_delete_token(token_id):
    """Delete a registration token."""
    token = RegistrationToken.query.get_or_404(token_id)
    token_id_val = token.id
    
    try:
        log = AuditLog(
            actor_type='superadmin',
            actor_id=session['superadmin_id'],
            actor_name=session['superadmin_name'],
            action='delete_registration_token',
            entity_type='registration_token',
            entity_id=token_id_val,
            details={'token': token.token, 'email': token.email}
        )
        db.session.add(log)
        
        db.session.delete(token)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete token: {str(e)}'}), 500

# ==================== DOCTOR MANAGEMENT ====================
@superadmin_bp.route('/api/doctors', methods=['GET'])
@superadmin_required
def api_get_doctors():
    clinic_id = request.args.get('clinic_id', type=int)
    
    query = Doctor.query
    if clinic_id:
        query = query.filter_by(clinic_id=clinic_id)
    
    doctors = query.all()
    return jsonify([d.to_dict() for d in doctors])


# ==================== ANALYTICS ====================
@superadmin_bp.route('/analytics')
@superadmin_required
def analytics():
    return render_template('superadmin/analytics.html')


@superadmin_bp.route('/api/analytics/overview', methods=['GET'])
@superadmin_required
def api_analytics_overview():
    from models import Appointment
    from sqlalchemy import func, case

    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    prev_start = start_date - timedelta(days=days)

    # ── Period-scoped patient & clinic counts ─────────────────────────────
    # Patients registered in this period
    current_pts = Patient.query.filter(Patient.created_at >= start_date).count()
    prev_pts    = Patient.query.filter(Patient.created_at >= prev_start,
                                       Patient.created_at <  start_date).count()
    patient_growth = round(((current_pts - prev_pts) / prev_pts * 100) if prev_pts > 0 else 0, 1)

    # Clinics that had at least one patient registration in this period
    active_clinic_ids = db.session.query(Patient.clinic_id).filter(
        Patient.created_at >= start_date
    ).distinct().subquery()
    active_clinics = db.session.query(func.count()).select_from(
        Clinic
    ).filter(
        Clinic.is_active == True,
        Clinic.id.in_(active_clinic_ids)
    ).scalar() or 0

    prev_cls = db.session.query(func.count(Patient.clinic_id.distinct())).filter(
        Patient.created_at >= prev_start,
        Patient.created_at <  start_date
    ).scalar() or 0
    current_cls = db.session.query(func.count(Patient.clinic_id.distinct())).filter(
        Patient.created_at >= start_date
    ).scalar() or 0
    clinic_growth = round(((current_cls - prev_cls) / max(prev_cls, 1) * 100), 1)

    total_patients = current_pts
    avg_patients_per_clinic = round(total_patients / active_clinics, 1) if active_clinics > 0 else 0

    # ── Patient trend (registrations per day) ────────────────────────────
    trend_rows = db.session.query(
        func.date(Patient.created_at).label('date'),
        func.count(Patient.id).label('count')
    ).filter(Patient.created_at >= start_date
    ).group_by(func.date(Patient.created_at)
    ).order_by('date').all()
    # Build a lookup dict then fill EVERY day in the period so the chart
    # always has a full continuous set of data points (no gaps).
    trend_dict = {str(d): c for d, c in trend_rows}
    _day = start_date.date()
    _end = datetime.utcnow().date()
    _all_days = []
    while _day <= _end:
        _all_days.append(_day)
        _day += timedelta(days=1)
    trend_labels = [str(d) for d in _all_days]
    trend_values = [trend_dict.get(str(d), 0) for d in _all_days]

    # ── Severity / Priority distribution ─────────────────────────────────
    prio_rows = db.session.query(
        Patient.priority, func.count(Patient.id)
    ).filter(Patient.created_at >= start_date
    ).group_by(Patient.priority).all()
    # Keys match actual DB values stored by triage engine
    prio_map = {'EMERGENCY': 0, 'RED': 0, 'AMBER': 0, 'GREEN': 0}
    for prio, cnt in prio_rows:
        key = (prio or '').upper()
        if key in prio_map:
            prio_map[key] = cnt

    # ── Top clinics ───────────────────────────────────────────────────────
    top_q = db.session.query(
        Clinic.id,
        Clinic.name,
        func.count(Patient.id).label('patient_count')
    ).join(Patient, Patient.clinic_id == Clinic.id, isouter=True
    ).filter(Patient.created_at >= start_date
    ).group_by(Clinic.id, Clinic.name
    ).order_by(func.count(Patient.id).desc()
    ).limit(10).all()

    wait_by_clinic = db.session.query(
        Appointment.clinic_id,
        func.avg(func.extract('epoch', Appointment.completed_at - Appointment.created_at) / 60)
    ).filter(
        Appointment.completed_at.isnot(None),
        Appointment.appointment_date >= start_date.date()
    ).group_by(Appointment.clinic_id).all()
    wait_map = {cid: round(float(w or 0), 1) for cid, w in wait_by_clinic}

    max_count = max((c for _, _, c in top_q), default=1) or 1
    top_clinics_data = [{
        'name': name,
        'patient_count': count,
        'avg_wait_time': wait_map.get(cid, 0),
        'performance': min(100, round((count / max_count) * 100))
    } for cid, name, count in top_q]

    # ── Queue metrics (derived from Patient + Appointment) ────────────────
    days_with_data = len(trend_values)
    peak_queue  = max(trend_values) if trend_values else 0
    avg_queue   = round(sum(trend_values) / days_with_data if days_with_data > 0 else 0, 1)

    wait_agg = db.session.query(
        func.avg(func.extract('epoch', Appointment.completed_at - Appointment.created_at) / 60),
        func.max(func.extract('epoch', Appointment.completed_at - Appointment.created_at) / 60)
    ).filter(
        Appointment.completed_at.isnot(None),
        Appointment.appointment_date >= start_date.date()
    ).first()
    queue_metrics = {
        'peak_queue':    peak_queue,
        'avg_queue':     avg_queue,
        'avg_wait_time': round(float(wait_agg[0] or 0), 1),
        'max_wait_time': round(float(wait_agg[1] or 0), 0)
    }

    # ── Slot / Appointment metrics ────────────────────────────────────────
    booked_statuses = ('scheduled', 'checked_in', 'in_triage', 'ready', 'consulting', 'completed')
    slot_agg = db.session.query(
        func.count(Appointment.id).label('total'),
        func.sum(case((Appointment.status.in_(booked_statuses), 1), else_=0)).label('booked')
    ).filter(Appointment.appointment_date >= start_date.date()).first()
    slot_metrics = {
        'total_slots':  slot_agg.total  or 0,
        'booked_slots': int(slot_agg.booked or 0)
    }

    # ── Patient status distribution ───────────────────────────────────────
    status_rows = db.session.query(
        Patient.status, func.count(Patient.id)
    ).filter(Patient.created_at >= start_date
    ).group_by(Patient.status).all()
    # Map all possible status strings stored in Patient.status to analytics keys
    status_name_map = {
        'Waiting':     'waiting',
        'With Doctor': 'in_progress',
        'Consulting':  'in_progress',
        'In Progress': 'in_progress',
        'Done':        'completed',
        'Completed':   'completed',
        'Cancelled':   'cancelled',
        'No Show':     'cancelled',
    }
    patient_statuses = {'waiting': 0, 'in_progress': 0, 'completed': 0, 'cancelled': 0}
    for st, cnt in status_rows:
        key = status_name_map.get(st)
        if key:
            patient_statuses[key] += cnt

    # ── Hourly distribution (from Patient.created_at) ─────────────────────
    hourly_rows = db.session.query(
        func.extract('hour', Patient.created_at).label('hour'),
        func.count(Patient.id).label('count')
    ).filter(Patient.created_at >= start_date
    ).group_by(func.extract('hour', Patient.created_at)
    ).order_by('hour').all()
    hourly_distribution = [0] * 24
    peak_hours = []
    for hour, cnt in hourly_rows:
        if hour is not None:
            hourly_distribution[int(hour)] = cnt
            peak_hours.append({'hour': int(hour), 'count': cnt})
    peak_hours.sort(key=lambda x: x['count'], reverse=True)

    # ── Slot utilisation by day of week ───────────────────────────────────
    dow_rows = db.session.query(
        func.extract('dow', Appointment.appointment_date).label('dow'),
        func.count(Appointment.id).label('total'),
        func.sum(case((Appointment.status.in_(booked_statuses), 1), else_=0)).label('booked')
    ).filter(Appointment.appointment_date >= start_date.date()
    ).group_by(func.extract('dow', Appointment.appointment_date)).all()
    slot_util_by_day = [0] * 7
    for dow, total, booked in dow_rows:
        if dow is not None and total and total > 0:
            day_index = (int(dow) + 6) % 7   # PG: 0=Sun → Mon=0 index
            slot_util_by_day[day_index] = round((float(booked or 0) / total) * 100, 1)

    # ── Queue / visit timeline (last 7 days) ─────────────────────────────
    timeline_rows = db.session.query(
        func.date(Patient.created_at).label('date'),
        func.count(Patient.id).label('count')
    ).filter(Patient.created_at >= datetime.utcnow() - timedelta(days=7)
    ).group_by(func.date(Patient.created_at)
    ).order_by('date').all()
    queue_timeline_data = {
        'labels': [str(d) for d, _ in timeline_rows],
        'data':   [c for _, c in timeline_rows]
    }

    return jsonify({
        'total_patients':        total_patients,
        'active_clinics':        active_clinics,
        'avg_patients_per_clinic': round(avg_patients_per_clinic, 1),
        'patient_growth':        patient_growth,
        'clinic_growth':         clinic_growth,
        'trend_labels':          trend_labels,
        'trend_data':            trend_values,
        'severity_distribution': [prio_map['EMERGENCY'], prio_map['RED'], prio_map['AMBER'], prio_map['GREEN']],
        'top_clinics':           top_clinics_data,
        'queue_metrics':         queue_metrics,
        'slot_metrics':          slot_metrics,
        'patient_statuses':      patient_statuses,
        'hourly_distribution':   hourly_distribution,
        'peak_hours':            peak_hours,
        'slot_by_day':           slot_util_by_day,
        'queue_timeline':        queue_timeline_data
    })
    
    # Basic metrics
    total_patients = Patient.query.count()
    active_clinics = Clinic.query.filter_by(is_active=True).count()
    avg_patients_per_clinic = total_patients / active_clinics if active_clinics > 0 else 0
    
    # Patient growth (compare to previous period)
    prev_start = start_date - timedelta(days=days)
    current_period_patients = Patient.query.filter(Patient.created_at >= start_date).count()
    prev_period_patients = Patient.query.filter(
        Patient.created_at >= prev_start,
        Patient.created_at < start_date
    ).count()
    patient_growth = ((current_period_patients - prev_period_patients) / prev_period_patients * 100) if prev_period_patients > 0 else 0
    
    # Clinic growth
    current_period_clinics = Clinic.query.filter(Clinic.created_at >= start_date).count()
    prev_period_clinics = Clinic.query.filter(
        Clinic.created_at >= prev_start,
        Clinic.created_at < start_date
    ).count()
    clinic_growth = ((current_period_clinics - prev_period_clinics) / max(prev_period_clinics, 1) * 100)
    
    # Patient trend data
    trend_data = db.session.query(
        func.date(Patient.created_at).label('date'),
        func.count(Patient.id).label('count')
    ).filter(
        Patient.created_at >= start_date
    ).group_by(
        func.date(Patient.created_at)
    ).order_by('date').all()
    
    trend_labels = [str(d) for d, _ in trend_data]
    trend_values = [c for _, c in trend_data]
    
    # Severity distribution
    severity_dist = db.session.query(
        PatientQueue.severity_level,
        func.count(PatientQueue.id)
    ).filter(
        PatientQueue.created_at >= start_date
    ).group_by(PatientQueue.severity_level).all()
    
    severity_map = {'critical': 0, 'urgent': 0, 'routine': 0}
    for sev, count in severity_dist:
        if sev in severity_map:
            severity_map[sev] = count
    
    # Top clinics
    top_clinics = db.session.query(
        Clinic.id,
        Clinic.name,
        func.count(Patient.id).label('patient_count'),
        func.coalesce(func.avg(
            case((PatientQueue.completed_at.isnot(None), 
                 func.extract('epoch', PatientQueue.completed_at - PatientQueue.created_at) / 60), else_=None)
        ), 0).label('avg_wait_time')
    ).join(Patient, Patient.clinic_id == Clinic.id, isouter=True
    ).join(PatientQueue, PatientQueue.patient_id == Patient.id, isouter=True
    ).filter(Patient.created_at >= start_date
    ).group_by(Clinic.id, Clinic.name
    ).order_by(func.count(Patient.id).desc()
    ).limit(10).all()
    
    top_clinics_data = [{
        'name': name,
        'patient_count': count,
        'avg_wait_time': round(float(wait_time), 1),
        'performance': min(100, round((count / max(current_period_patients / active_clinics, 1)) * 100, 0)) if active_clinics > 0 else 0
    } for _, name, count, wait_time in top_clinics]
    
    # Queue metrics
    queue_stats = db.session.query(
        func.count(PatientQueue.id).label('total'),
        func.max(PatientQueue.queue_position).label('peak_queue'),
        func.avg(PatientQueue.queue_position).label('avg_queue'),
        func.avg(
            case((PatientQueue.completed_at.isnot(None),
                 func.extract('epoch', PatientQueue.completed_at - PatientQueue.created_at) / 60), else_=None)
        ).label('avg_wait_time'),
        func.max(
            case((PatientQueue.completed_at.isnot(None),
                 func.extract('epoch', PatientQueue.completed_at - PatientQueue.created_at) / 60), else_=None)
        ).label('max_wait_time')
    ).filter(PatientQueue.created_at >= start_date).first()
    
    queue_metrics = {
        'peak_queue': queue_stats.peak_queue or 0,
        'avg_queue': round(float(queue_stats.avg_queue or 0), 1),
        'avg_wait_time': round(float(queue_stats.avg_wait_time or 0), 1),
        'max_wait_time': round(float(queue_stats.max_wait_time or 0), 0)
    }
    
    # Slot metrics (appointments)
    slot_stats = db.session.query(
        func.count(Appointment.id).label('total_slots'),
        func.sum(case((Appointment.status == 'confirmed', 1), else_=0)).label('booked_slots')
    ).filter(Appointment.appointment_date >= start_date.date()).first()
    
    slot_metrics = {
        'total_slots': slot_stats.total_slots or 0,
        'booked_slots': slot_stats.booked_slots or 0
    }
    
    # Patient statuses
    status_dist = db.session.query(
        PatientQueue.status,
        func.count(PatientQueue.id)
    ).filter(PatientQueue.created_at >= start_date
    ).group_by(PatientQueue.status).all()
    
    patient_statuses = {
        'waiting': 0,
        'in_progress': 0,
        'completed': 0,
        'cancelled': 0
    }
    for status, count in status_dist:
        if status in patient_statuses:
            patient_statuses[status] = count
    
    # Hourly distribution
    hourly_dist = db.session.query(
        func.extract('hour', PatientQueue.created_at).label('hour'),
        func.count(PatientQueue.id).label('count')
    ).filter(PatientQueue.created_at >= start_date
    ).group_by(func.extract('hour', PatientQueue.created_at)
    ).order_by('hour').all()
    
    hourly_distribution = [0] * 24
    peak_hours = []
    for hour, count in hourly_dist:
        if hour is not None:
            hourly_distribution[int(hour)] = count
            peak_hours.append({'hour': int(hour), 'count': count})
    
    peak_hours.sort(key=lambda x: x['count'], reverse=True)
    
    # Slot utilization by day of week
    slot_by_day = db.session.query(
        func.extract('dow', Appointment.appointment_date).label('dow'),
        func.count(Appointment.id).label('total'),
        func.sum(case((Appointment.status == 'confirmed', 1), else_=0)).label('booked')
    ).filter(Appointment.appointment_date >= start_date.date()
    ).group_by(func.extract('dow', Appointment.appointment_date)
    ).all()
    
    slot_util_by_day = [0] * 7  # Mon=1 to Sun=0 in PostgreSQL
    for dow, total, booked in slot_by_day:
        if dow is not None and total and total > 0:
            # Convert PostgreSQL dow (0=Sun, 1=Mon) to our format (Mon=0, Sun=6)
            day_index = (int(dow) + 6) % 7
            slot_util_by_day[day_index] = round((booked / total) * 100, 1)
    
    # Queue timeline (last 7 days)
    queue_timeline = db.session.query(
        func.date(PatientQueue.created_at).label('date'),
        func.max(PatientQueue.queue_position).label('max_queue')
    ).filter(
        PatientQueue.created_at >= datetime.utcnow() - timedelta(days=7)
    ).group_by(func.date(PatientQueue.created_at)
    ).order_by('date').all()
    
    queue_timeline_data = {
        'labels': [str(d) for d, _ in queue_timeline],
        'data': [q or 0 for _, q in queue_timeline]
    }
    
    return jsonify({
        'total_patients': total_patients,
        'active_clinics': active_clinics,
        'avg_patients_per_clinic': round(avg_patients_per_clinic, 1),
        'patient_growth': round(patient_growth, 1),
        'clinic_growth': round(clinic_growth, 1),
        'trend_labels': trend_labels,
        'trend_data': trend_values,
        'severity_distribution': [severity_map['critical'], severity_map['urgent'], severity_map['routine']],
        'top_clinics': top_clinics_data,
        'queue_metrics': queue_metrics,
        'slot_metrics': slot_metrics,
        'patient_statuses': patient_statuses,
        'hourly_distribution': hourly_distribution,
        'peak_hours': peak_hours,
        'slot_by_day': slot_util_by_day,
        'queue_timeline': queue_timeline_data
    })


# ==================== SUPERADMIN MANAGEMENT ====================

@superadmin_bp.route('/admins')
@superadmin_required
def admins():
    """Manage superadmin accounts (only accessible by super-admins)."""
    current = SuperAdmin.query.get(session['superadmin_id'])
    if not current or not current.is_super:
        return redirect(url_for('superadmin.dashboard'))
    return render_template('superadmin/admins.html')


@superadmin_bp.route('/api/superadmins', methods=['GET'])
@superadmin_required
def api_get_superadmins():
    """List all superadmin accounts."""
    admins_list = SuperAdmin.query.order_by(SuperAdmin.created_at.desc()).all()
    return jsonify([a.to_dict() for a in admins_list])


@superadmin_bp.route('/api/superadmins', methods=['POST'])
@superadmin_required
def api_create_superadmin():
    """Create a new superadmin account. Only super-superadmins may do this."""
    current = SuperAdmin.query.get(session['superadmin_id'])
    if not current or not current.is_super:
        return jsonify({'error': 'Permission denied. Only super-admins can create new admins.'}), 403

    data = request.json or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    is_super = bool(data.get('is_super', False))

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400

    if SuperAdmin.query.filter_by(email=email).first():
        return jsonify({'error': 'An admin with this email already exists'}), 400

    new_admin = SuperAdmin(name=name, email=email, is_super=is_super, is_active=True)
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()

    log = AuditLog(
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='create_superadmin',
        entity_type='superadmin',
        entity_id=new_admin.id,
        details={'name': name, 'email': email, 'is_super': is_super}
    )
    db.session.add(log)
    db.session.commit()

    return jsonify(new_admin.to_dict()), 201


@superadmin_bp.route('/api/superadmins/<int:admin_id>/toggle', methods=['POST'])
@superadmin_required
def api_toggle_superadmin(admin_id):
    """Activate or deactivate a superadmin account."""
    current = SuperAdmin.query.get(session['superadmin_id'])
    if not current or not current.is_super:
        return jsonify({'error': 'Permission denied'}), 403
    if admin_id == session['superadmin_id']:
        return jsonify({'error': 'You cannot deactivate your own account'}), 400

    admin = SuperAdmin.query.get_or_404(admin_id)
    admin.is_active = not admin.is_active
    db.session.commit()

    log = AuditLog(
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='toggle_superadmin',
        entity_type='superadmin',
        entity_id=admin_id,
        details={'is_active': admin.is_active}
    )
    db.session.add(log)
    db.session.commit()

    return jsonify(admin.to_dict())


@superadmin_bp.route('/api/superadmins/<int:admin_id>/reset-password', methods=['POST'])
@superadmin_required
def api_reset_superadmin_password(admin_id):
    """Reset another superadmin's password (super-superadmin only)."""
    current = SuperAdmin.query.get(session['superadmin_id'])
    if not current or not current.is_super:
        return jsonify({'error': 'Permission denied'}), 403

    data = request.json or {}
    new_password = data.get('new_password', '').strip()
    if not new_password or len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    admin = SuperAdmin.query.get_or_404(admin_id)
    admin.set_password(new_password)
    db.session.commit()

    log = AuditLog(
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='reset_superadmin_password',
        entity_type='superadmin',
        entity_id=admin_id,
        details={'target_email': admin.email}
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'success': True})


@superadmin_bp.route('/api/superadmins/<int:admin_id>', methods=['DELETE'])
@superadmin_required
def api_delete_superadmin(admin_id):
    """Delete a superadmin account (super-superadmin only)."""
    current = SuperAdmin.query.get(session['superadmin_id'])
    if not current or not current.is_super:
        return jsonify({'error': 'Permission denied'}), 403
    if admin_id == session['superadmin_id']:
        return jsonify({'error': 'You cannot delete your own account'}), 400

    admin = SuperAdmin.query.get_or_404(admin_id)
    name_bak = admin.name
    db.session.delete(admin)
    db.session.commit()

    log = AuditLog(
        actor_type='superadmin',
        actor_id=session['superadmin_id'],
        actor_name=session['superadmin_name'],
        action='delete_superadmin',
        entity_type='superadmin',
        entity_id=admin_id,
        details={'name': name_bak}
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'success': True})
