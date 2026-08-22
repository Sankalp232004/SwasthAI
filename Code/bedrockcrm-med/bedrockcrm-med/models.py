"""
Enhanced models with Multi-Tenancy, Superadmin, and Clinic Management
"""
import enum
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# ==================== ENUMS ====================
class PriorityEnum(enum.Enum):
    """Triage Priority Levels."""
    EMERGENCY = "EMERGENCY"
    RED = "RED"
    AMBER = "AMBER"
    GREEN = "GREEN"


class StatusEnum(enum.Enum):
    """Patient consultation status."""
    WAITING = "Waiting"
    CONSULTING = "Consulting"
    COMPLETED = "Completed"


# ==================== CLINIC MODEL ====================
class Clinic(db.Model):
    __tablename__ = 'clinics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)  # URL identifier
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    latitude = db.Column(db.Float)  # For location-based discovery
    longitude = db.Column(db.Float)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    subscription_status = db.Column(db.String(50), default='trial')  # trial, active, suspended, expired
    subscription_expiry = db.Column(db.DateTime)
    
    # Settings
    max_doctors = db.Column(db.Integer, default=5)
    max_patients_per_day = db.Column(db.Integer, default=100)
    features = db.Column(db.JSON, default=dict)  # Feature flags
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patients = db.relationship('Patient', backref='clinic', lazy=True, cascade='all, delete-orphan')
    doctors = db.relationship('Doctor', backref='clinic', lazy=True, cascade='all, delete-orphan')
    otp_records = db.relationship('OTPRecord', backref='clinic', lazy=True, cascade='all, delete-orphan')
    registration_tokens = db.relationship('RegistrationToken', backref='clinic', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'is_active': self.is_active,
            'subscription_status': self.subscription_status,
            'subscription_expiry': self.subscription_expiry.isoformat() if self.subscription_expiry else None,
            'max_doctors': self.max_doctors,
            'max_patients_per_day': self.max_patients_per_day,
            'features': self.features,
            'created_at': self.created_at.isoformat(),
            'patient_count': len(self.patients),
            'doctor_count': len(self.doctors),
            'latitude': self.latitude,
            'longitude': self.longitude
        }


# ==================== SUPERADMIN MODEL ====================
class SuperAdmin(db.Model):
    __tablename__ = 'superadmins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    
    # Permissions
    is_super = db.Column(db.Boolean, default=True)  # Can manage other superadmins
    permissions = db.Column(db.JSON, default=dict)  # Granular permissions
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'is_super': self.is_super,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat()
        }


# ==================== ENHANCED PATIENT MODEL ====================
class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    
    # Patient Info
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    phone_verified = db.Column(db.Boolean, default=False)
    
    # Medical Info
    complaint = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Waiting')
    
    # Clinical Data
    clinical_data = db.Column(db.JSON)
    
    # Doctor assignment (for multi-doctor clinics)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)

    # Visit History
    visit_count = db.Column(db.Integer, default=1)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for fast lookup
    __table_args__ = (
        db.Index('idx_clinic_phone', 'clinic_id', 'phone'),
        db.Index('idx_clinic_status', 'clinic_id', 'status'),
        db.Index('idx_clinic_priority', 'clinic_id', 'priority'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'doctor_id': self.doctor_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'phone_verified': self.phone_verified,
            'complaint': self.complaint,
            'priority': self.priority,
            'status': self.status,
            'clinical_data': self.clinical_data,
            'visit_count': self.visit_count,
            'last_visit': (self.last_visit.isoformat() + 'Z') if self.last_visit else None,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }


# ==================== ENHANCED DOCTOR MODEL ====================
class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    specialization = db.Column(db.String(100))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialization': self.specialization,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat()
        }


# ==================== OTP RECORD MODEL ====================
class OTPRecord(db.Model):
    __tablename__ = 'otp_records'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    
    # Status
    is_verified = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    max_attempts = db.Column(db.Integer, default=3)
    
    # Expiry
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Purpose
    purpose = db.Column(db.String(50), default='registration')  # registration, verification, login
    
    __table_args__ = (
        db.Index('idx_clinic_phone_otp', 'clinic_id', 'phone', 'is_verified'),
    )
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        return not self.is_expired() and not self.is_verified and self.attempts < self.max_attempts
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'phone': self.phone,
            'is_verified': self.is_verified,
            'attempts': self.attempts,
            'expires_at': self.expires_at.isoformat(),
            'is_expired': self.is_expired(),
            'is_valid': self.is_valid()
        }

# ==================== DOCTOR PASSWORD SETUP TOKEN MODEL ====================
class RegistrationToken(db.Model):
    __tablename__ = 'registration_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))  # Associated doctor
    
    # Token details
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False)  # Doctor email
    temp_password = db.Column(db.String(256))  # Optional temporary password
    
    # Token type and purpose
    token_type = db.Column(db.String(50), default='password_setup')  # password_setup, password_reset
    
    # Status
    is_used = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Expiry
    expires_at = db.Column(db.DateTime)  # Token expiration
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('superadmins.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    
    def is_valid(self):
        """Check if token is valid for use."""
        if self.is_used:
            return False, "Token has already been used"
        
        if not self.is_active:
            return False, "Token has been deactivated"
        
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False, "Token has expired"
        
        return True, "Valid"
    
    def mark_used(self):
        """Mark token as used."""
        self.is_used = True
        self.used_at = datetime.utcnow()
    
    def to_dict(self):
        is_valid, message = self.is_valid()
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'doctor_id': self.doctor_id,
            'token': self.token,
            'email': self.email,
            'token_type': self.token_type,
            'is_used': self.is_used,
            'is_active': self.is_active,
            'is_valid': is_valid,
            'validation_message': message,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat(),
            'used_at': self.used_at.isoformat() if self.used_at else None
        }


# ==================== AUDIT LOG MODEL ====================
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=True)
    
    # Actor
    actor_type = db.Column(db.String(50))  # doctor, superadmin, system
    actor_id = db.Column(db.Integer)
    actor_name = db.Column(db.String(100))
    
    # Action
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50))  # patient, clinic, doctor, etc.
    entity_id = db.Column(db.Integer)
    
    # Details
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_clinic_timestamp', 'clinic_id', 'timestamp'),
        db.Index('idx_actor', 'actor_type', 'actor_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'actor_type': self.actor_type,
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() + 'Z'
        }


# ==================== CLINIC HOURS MODEL ====================
# ==================== SYSTEM SETTINGS ====================
class SystemSetting(db.Model):
    """Key-value store for global app settings (e.g., base URL for QR codes)."""
    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key, default=None):
        row = cls.query.filter_by(key=key).first()
        return row.value if row else default

    @classmethod
    def set(cls, key, value):
        row = cls.query.filter_by(key=key).first()
        if row:
            row.value = value
            row.updated_at = datetime.utcnow()
        else:
            row = cls(key=key, value=value)
            db.session.add(row)
        db.session.commit()


class ClinicHours(db.Model):
    __tablename__ = 'clinic_hours'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # Day of week (0 = Monday, 6 = Sunday)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6
    
    # Time slots
    start_time = db.Column(db.Time, nullable=False)  # e.g., 12:00
    end_time = db.Column(db.Time, nullable=False)  # e.g., 16:00
    
    # Capacity
    patients_per_hour = db.Column(db.Integer, nullable=False)  # e.g., 4
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'doctor_id': self.doctor_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'patients_per_hour': self.patients_per_hour,
            'is_active': self.is_active
        }


# ==================== SLOT CONFIGURATION MODEL ====================
class SlotConfiguration(db.Model):
    __tablename__ = 'slot_configurations'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # Slot settings
    slot_duration_minutes = db.Column(db.Integer, default=30)  # Duration of each batch slot
    slots_per_batch = db.Column(db.Integer, default=5)  # Number of patients per batch
    buffer_between_batches = db.Column(db.Integer, default=5)  # Break time in minutes
    
    # Walk-in vs Appointment Balance
    walkin_slots_per_batch = db.Column(db.Integer, default=2)  # Reserved slots for walk-ins
    appointment_slots_per_batch = db.Column(db.Integer, default=3)  # Reserved slots for appointments
    
    # Advance booking settings
    max_advance_days = db.Column(db.Integer, default=30)  # How far in advance can patients book
    allow_same_day_booking = db.Column(db.Boolean, default=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('doctor_id', name='uq_doctor_slot_config'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'doctor_id': self.doctor_id,
            'slot_duration_minutes': self.slot_duration_minutes,
            'slots_per_batch': self.slots_per_batch,
            'buffer_between_batches': self.buffer_between_batches,
            'walkin_slots_per_batch': self.walkin_slots_per_batch,
            'appointment_slots_per_batch': self.appointment_slots_per_batch,
            'max_advance_days': self.max_advance_days,
            'allow_same_day_booking': self.allow_same_day_booking,
            'is_active': self.is_active
        }


# ==================== APPOINTMENT MODEL ====================
class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # Appointment details
    appointment_date = db.Column(db.Date, nullable=False)
    slot_start_time = db.Column(db.Time, nullable=False)  # e.g., 12:00
    slot_end_time = db.Column(db.Time, nullable=False)  # e.g., 12:30
    batch_number = db.Column(db.Integer)  # Which batch within the slot (1-5 for default 5 slots)
    
    # Status
    status = db.Column(db.String(20), default='scheduled')  # scheduled, checked_in, in_triage, ready, consulting, completed, cancelled, no_show
    
    # Pre-appointment Triage (filled 10 mins before)
    triage_completed = db.Column(db.Boolean, default=False)
    triage_data = db.Column(db.JSON)  # Stores symptoms, vitals, chief complaint
    triage_priority = db.Column(db.String(20))  # RED, AMBER, GREEN based on triage
    triage_completed_at = db.Column(db.DateTime)
    
    # Reminder sent
    reminder_sent = db.Column(db.Boolean, default=False)
    reminder_sent_at = db.Column(db.DateTime)
    
    # Notes
    reason = db.Column(db.Text)  # Reason for visit
    notes = db.Column(db.Text)  # Doctor notes (after visit)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    checked_in_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    
    __table_args__ = (
        db.Index('idx_appointment_date', 'clinic_id', 'doctor_id', 'appointment_date'),
        db.Index('idx_patient_appointments', 'patient_id', 'appointment_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient_name': self.patient.name if self.patient else None,
            'patient_phone': self.patient.phone if self.patient else None,
            'patient_age': self.patient.age if self.patient else None,
            'patient_gender': self.patient.gender if self.patient else None,
            'doctor_name': self.doctor.name if self.doctor else None,
            'appointment_date': self.appointment_date.isoformat(),
            'slot_start_time': self.slot_start_time.strftime('%H:%M'),
            'slot_end_time': self.slot_end_time.strftime('%H:%M'),
            'batch_number': self.batch_number,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'triage_completed': self.triage_completed,
            'triage_data': self.triage_data,
            'triage_priority': self.triage_priority,
            'triage_completed_at': (self.triage_completed_at.isoformat() + 'Z') if self.triage_completed_at else None,
            'reminder_sent': self.reminder_sent,
            'created_at': self.created_at.isoformat() + 'Z',
            'checked_in_at': (self.checked_in_at.isoformat() + 'Z') if self.checked_in_at else None,
            'completed_at': (self.completed_at.isoformat() + 'Z') if self.completed_at else None
        }

