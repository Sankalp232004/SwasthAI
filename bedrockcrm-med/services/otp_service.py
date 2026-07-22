"""
OTP Service with Twilio Integration
"""
import random
import string
from datetime import datetime, timedelta
from app import db
from models import OTPRecord
import os

# Twilio credentials (will be set via environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Try to import Twilio
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER)
    if TWILIO_AVAILABLE:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    else:
        twilio_client = None
except ImportError:
    TWILIO_AVAILABLE = False
    twilio_client = None


class OTPService:
    """OTP Service for phone number verification"""
    
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    MAX_ATTEMPTS = 3
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=OTPService.OTP_LENGTH))
    
    @staticmethod
    def send_otp(clinic_id, phone, purpose='registration'):
        """
        Send OTP to phone number
        
        Args:
            clinic_id: Clinic ID
            phone: Phone number (with country code)
            purpose: Purpose of OTP (registration, verification, login)
        
        Returns:
            dict: {'success': bool, 'message': str, 'otp_id': int (if success)}
        """
        # Check for recent OTP
        recent_otp = OTPRecord.query.filter_by(
            clinic_id=clinic_id,
            phone=phone,
            is_verified=False
        ).filter(
            OTPRecord.expires_at > datetime.utcnow()
        ).order_by(
            OTPRecord.created_at.desc()
        ).first()
        
        if recent_otp and (datetime.utcnow() - recent_otp.created_at).seconds < 60:
            return {
                'success': False,
                'message': 'Please wait 60 seconds before requesting a new OTP'
            }
        
        # Generate new OTP
        otp_code = OTPService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=OTPService.OTP_EXPIRY_MINUTES)
        
        # Create OTP record
        otp_record = OTPRecord(
            clinic_id=clinic_id,
            phone=phone,
            otp_code=otp_code,
            expires_at=expires_at,
            purpose=purpose
        )
        
        db.session.add(otp_record)
        db.session.commit()
        
        # Send OTP via Twilio
        if TWILIO_AVAILABLE:
            try:
                message = twilio_client.messages.create(
                    body=f"Your SwasthAI verification code is: {otp_code}. Valid for {OTPService.OTP_EXPIRY_MINUTES} minutes.",
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone
                )
                
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'otp_id': otp_record.id,
                    'twilio_sid': message.sid
                }
            except Exception as e:
                print(f"Twilio error: {str(e)}")
                # In case of Twilio error, still return the OTP for dev/testing
                return {
                    'success': True,
                    'message': 'OTP generated (Twilio error - check logs)',
                    'otp_id': otp_record.id,
                    'otp_code': otp_code  # Only for dev/testing
                }
        else:
            # Development mode - return OTP directly
            return {
                'success': True,
                'message': 'OTP generated (Twilio not configured)',
                'otp_id': otp_record.id,
                'otp_code': otp_code  # Only for dev/testing
            }
    
    @staticmethod
    def verify_otp(clinic_id, phone, otp_code):
        """
        Verify OTP
        
        Args:
            clinic_id: Clinic ID
            phone: Phone number
            otp_code: OTP code to verify
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        otp_record = OTPRecord.query.filter_by(
            clinic_id=clinic_id,
            phone=phone,
            otp_code=otp_code,
            is_verified=False
        ).filter(
            OTPRecord.expires_at > datetime.utcnow()
        ).order_by(
            OTPRecord.created_at.desc()
        ).first()
        
        if not otp_record:
            # Increment attempts on any matching record
            any_record = OTPRecord.query.filter_by(
                clinic_id=clinic_id,
                phone=phone,
                is_verified=False
            ).filter(
                OTPRecord.expires_at > datetime.utcnow()
            ).order_by(
                OTPRecord.created_at.desc()
            ).first()
            
            if any_record:
                any_record.attempts += 1
                db.session.commit()
                
                if any_record.attempts >= any_record.max_attempts:
                    return {
                        'success': False,
                        'message': 'Maximum attempts exceeded. Please request a new OTP.'
                    }
            
            return {
                'success': False,
                'message': 'Invalid or expired OTP'
            }
        
        # Check if expired
        if otp_record.is_expired():
            return {
                'success': False,
                'message': 'OTP has expired. Please request a new one.'
            }
        
        # Check attempts
        if otp_record.attempts >= otp_record.max_attempts:
            return {
                'success': False,
                'message': 'Maximum verification attempts exceeded'
            }
        
        # Verify OTP
        if otp_record.otp_code == otp_code:
            otp_record.is_verified = True
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Phone number verified successfully'
            }
        else:
            otp_record.attempts += 1
            db.session.commit()
            
            remaining = otp_record.max_attempts - otp_record.attempts
            return {
                'success': False,
                'message': f'Invalid OTP. {remaining} attempts remaining.'
            }
    
    @staticmethod
    def cleanup_expired_otps():
        """Clean up expired OTP records (call periodically)"""
        expired = OTPRecord.query.filter(
            OTPRecord.expires_at < datetime.utcnow()
        ).delete()
        db.session.commit()
        return expired
