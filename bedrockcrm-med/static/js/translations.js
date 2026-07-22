// SwasthAI Translation System
// Supports: English (en), Hindi (hi), Marathi (mr)

const translations = {
    en: {
        // ==================== COMMON ====================
        'app.name': 'SwasthAI',
        'app.tagline': 'Quick and Smart Medical Triage',
        'app.subtitle': 'Fast, Fair, and Accurate Patient Prioritization',
        
        // Buttons
        'btn.register': 'Register Now',
        'btn.doctor_login': 'Doctor Login',
        'btn.next': 'Next',
        'btn.back': 'Back',
        'btn.submit': 'Submit',
        'btn.continue': 'Continue',
        'btn.complete': 'Complete Registration',
        'btn.refresh': 'Refresh',
        'btn.close': 'Close',
        
        // ==================== LANDING PAGE ====================
        'landing.queue': 'In Queue',
        'landing.wait': 'Min Wait',
        'landing.reg_time': 'Registration takes less than 2 minutes',
        'landing.how_it_works': 'How It Works',
        
        // ==================== WELCOME / HOMEPAGE ====================
        'welcome.title': 'Welcome! How would you like to proceed?',
        'welcome.findNearby': 'Find Nearby Clinics',
        'welcome.findNearbyDesc': 'Discover clinics near your location',
        'welcome.scanQR': 'Scan QR Code',
        'welcome.scanQRDesc': 'Use QR code or enter clinic code',
        'welcome.provider': 'Are you a healthcare provider?',
        
        // ==================== NEARBY CLINICS ====================
        'nearby.title': 'Clinics Near You',
        'nearby.useLocation': 'Use My Current Location',
        'nearby.sampleLocation': 'Sample Location: Mumbai',
        
        // ==================== QR CODE ====================
        'qr.title': 'Enter Clinic Code',
        'qr.scanDesc': 'Scan the QR code at clinic reception or enter code below',
        'qr.placeholder': 'Enter clinic code',
        'qr.go': 'Go',
        'qr.scanCamera': 'Scan QR with Camera',
        'qr.stopCamera': 'Stop Camera',
        
        // ==================== LOGIN ====================
        'login.doctor': 'Doctor Login',
        'login.admin': 'Admin Login',
        
        'landing.feature1_title': 'Quick Check-in',
        'landing.feature1_desc': "Answer a few simple questions about how you're feeling. No typing required - just tap!",
        
        'landing.feature2_title': 'Instant Priority',
        'landing.feature2_desc': 'Get your priority level immediately. Higher priority = seen faster.',
        
        'landing.feature3_title': 'Live Updates',
        'landing.feature3_desc': "Track your position in queue. Get notified instantly when it's your turn.",
        
        // ==================== REGISTRATION - GENERAL ====================
        'reg.title': 'Patient Registration',
        'reg.quick_reg': 'Quick Registration',
        'reg.step1': 'Basic Info',
        'reg.step2': 'Symptoms',
        'reg.step3': 'Medical History',
        'reg.required': 'Required',
        'reg.optional': 'optional',
        'reg.select': 'Select...',
        'reg.processing': 'Processing your registration...',
        'reg.please_wait': 'Please wait',
        'reg.error': 'Error',
        'reg.network_error': 'Network error. Please try again.',
        'reg.select_all': 'Select all that apply',
        
        // ==================== REGISTRATION - STEP 1 ====================
        'reg.about_you': 'Tell us about yourself',
        'reg.name': 'Full Name',
        'reg.name_placeholder': 'Enter your full name',
        'reg.age': 'Age',
        'reg.age_years': 'Years',
        'reg.gender': 'Gender',
        'reg.gender_male': 'Male',
        'reg.gender_female': 'Female',
        'reg.gender_other': 'Other',
        'reg.phone': 'Phone Number',
        'reg.phone_placeholder': '10-digit mobile number',
        
        // ==================== REGISTRATION - STEP 2 ====================
        'reg.how_feeling': 'How are you feeling right now?',
        'reg.main_complaint': 'What brings you here today?',
        'reg.complaint_pain': 'Pain / Discomfort',
        'reg.complaint_fever': 'Fever / Infection',
        'reg.complaint_breathing': 'Breathing Problems',
        'reg.complaint_injury': 'Injury / Accident',
        'reg.complaint_stomach': 'Stomach / Digestive',
        'reg.complaint_skin': 'Skin Problem / Rash',
        'reg.complaint_other': 'Other',
        
        'reg.pain_level': 'How much pain are you in?',
        'reg.pain_0': 'No Pain',
        'reg.pain_2': 'Mild',
        'reg.pain_4': 'Moderate',
        'reg.pain_6': 'Bad',
        'reg.pain_8': 'Severe',
        'reg.pain_10': 'Worst',
        
        'reg.emergency_title': 'Are you experiencing any of these RIGHT NOW?',
        'reg.emergency_chest': 'Chest Pain or Pressure',
        'reg.emergency_breathing': 'Difficulty Breathing',
        'reg.emergency_bleeding': 'Heavy Bleeding',
        'reg.emergency_confusion': 'Confusion / Disorientation',
        
        'reg.duration': 'How long have you had this problem?',
        'reg.duration_now': 'Just now',
        'reg.duration_hours': 'Less than 1 hour',
        'reg.duration_today': 'Today (1-6 hours)',
        'reg.duration_yesterday': 'Since yesterday',
        'reg.duration_days': '1-3 days',
        'reg.duration_week': '4-7 days',
        'reg.duration_longer': 'More than a week',
        
        'reg.anything_else': 'Anything else we should know?',
        'reg.describe_briefly': 'Describe your symptoms briefly...',
        
        // ==================== REGISTRATION - STEP 3 ====================
        'reg.medical_history': 'Your Medical History',
        'reg.conditions': 'Do you have any of these conditions?',
        'reg.condition_diabetes': 'Diabetes',
        'reg.condition_heart': 'Heart Disease',
        'reg.condition_bp': 'High Blood Pressure',
        'reg.condition_asthma': 'Asthma / Lung Disease',
        'reg.condition_kidney': 'Kidney Disease',
        'reg.condition_allergies': 'Allergies',
        'reg.condition_none': 'None of these',
        
        'reg.pregnant': 'Are you currently pregnant?',
        'reg.pregnant_yes': 'Yes',
        'reg.pregnant_no': 'No',
        'reg.pregnant_maybe': 'Maybe / Not sure',
        
        'reg.fever': 'Do you have fever?',
        'reg.fever_no': 'No fever',
        'reg.fever_mild': 'Mild (Feel warm)',
        'reg.fever_high': 'High fever',
        
        'reg.vitals_note': 'Note: Our staff will take your vitals (BP, temperature, etc.) when you arrive.',
        
        // ==================== WAITING ROOM ====================
        'wait.title': 'Waiting Room',
        'wait.loading': 'Loading your status...',
        'wait.error_loading': 'Error loading your information. Please refresh the page.',
        
        'wait.your_priority': 'Your Priority',
        'wait.token': 'Token #',
        'wait.status': 'Status',
        'wait.position': 'Your Position in Queue',
        'wait.position_short': 'Position',
        'wait.patients_ahead': 'patients ahead of you',
        'wait.no_one_ahead': 'No one ahead!',
        
        'wait.please_wait': 'Please Wait',
        'wait.stay_nearby': 'Please stay nearby',
        'wait.youre_next': "You're next!",
        'wait.being_called': "You're being called!",
        'wait.go_now': 'Please proceed to the consultation room now.',
        'wait.consultation_complete': 'Your consultation has been completed',
        
        'wait.est_wait': 'Estimated wait',
        'wait.estimated': 'Estimated Wait Time',
        'wait.approximate': 'Approximate time based on current queue',
        'wait.your_turn_next': "You're next!",
        'wait.minutes': 'minutes',
        'wait.connected': 'Live updates active',
        'wait.connecting': 'Connecting to live updates...',
        'wait.reconnecting': 'Connection lost - Reconnecting...',
        'wait.auto_update': 'This page will update automatically',
        
        'wait.your_details': 'Your Details',
        'wait.prefer_book': 'Prefer to visit on a different day?',
        'wait.book_instead': 'Book an Appointment',
        'wait.detail_age': 'Age / Gender',
        'wait.detail_complaint': 'Complaint',
        'wait.detail_registered': 'Registered',
        'wait.years': 'years',
        
        'wait.important': 'Important',
        
        // ==================== PRIORITY LEVELS ====================
        'priority.emergency': 'Emergency',
        'priority.emergency_msg': 'Immediate Attention Required',
        'priority.emergency_sub': 'Please approach the emergency desk immediately',
        
        'priority.red': 'Critical',
        'priority.red_msg': 'High Priority — You will be seen very soon',
        'priority.red_sub': 'You will be seen very soon',
        
        'priority.amber': 'Urgent',
        'priority.amber_msg': 'Urgent — Please wait, you will be called shortly',
        'priority.amber_sub': 'Please wait, you will be called shortly',
        
        'priority.green': 'Routine',
        'priority.green_msg': 'Standard Queue — Please wait comfortably',
        'priority.green_sub': 'Please wait comfortably, we will call you',
        
        // ==================== STATUS LABELS ====================
        'status.waiting': 'Waiting',
        'status.consulting': 'Consulting',
        'status.completed': 'Completed',
        
        // ==================== NOTIFICATIONS ====================
        'notif.your_turn': 'Your Turn!',
        'notif.proceed': 'Please proceed to the consultation room',
        
        // ==================== ERRORS ====================
        'error.required_field': 'This field is required',
        'error.invalid_phone': 'Please enter a valid phone number',
        'error.invalid_age': 'Please enter a valid age',
        'error.select_option': 'Please select an option',
        'error.try_again': 'Please try again',
        
        // ==================== DOCTOR DASHBOARD ====================
        'doctor.title': 'Doctor Dashboard',
        'doctor.portal': 'Doctor Portal',
        'doctor.logout': 'Logout',
        'changePassword': 'Change Password',
        'setupPassword': 'Set Your Password',
        'setupPasswordDesc': 'Create a secure password for your account',
        'email': 'Email',
        'tempPassword': 'Temporary Password',
        'enterTempPassword': 'Enter the temporary password provided to you',
        'newPassword': 'New Password',
        'passwordRequirements': 'At least 8 characters',
        'confirmPassword': 'Confirm Password',
        'confirmNewPassword': 'Confirm New Password',
        'setPassword': 'Set Password',
        'backToLogin': '← Back to Login',
        'currentPassword': 'Current Password',
        'updatePassword': 'Update Password',
        'backToDashboard': '← Back to Dashboard',
        'doctor.patient_queue': 'Patient Queue',
        'doctor.refresh': 'Refresh',
        'doctor.loading_queue': 'Loading queue...',
        'doctor.no_patients': 'No patients in queue',
        'doctor.connecting': 'Connecting to live updates...',
        'doctor.live_active': 'Live updates active',
        'doctor.connection_lost': 'Connection lost - Reconnecting...',
        
        'doctor.token': 'Token',
        'doctor.patient': 'Patient',
        'doctor.complaint': 'Complaint',
        'doctor.waiting': 'Waiting',
        'doctor.actions': 'Actions',
        'doctor.years_short': 'y',
        'doctor.min_ago': 'min ago',
        'doctor.hour_ago': 'hour ago',
        'doctor.just_now': 'Just now',
        
        'doctor.view_details': 'View Details',
        'doctor.patient_details': 'Patient Details',
        'doctor.clinical_data': 'Clinical Data',
        'doctor.triage_result': 'Triage Result',
        'doctor.red_flags': 'Red Flags',
        'doctor.no_red_flags': 'None detected',
        
        'doctor.override': 'Override Priority',
        'doctor.current_priority': 'Current Priority',
        'doctor.new_priority': 'New Priority',
        'doctor.select_priority': 'Select new priority...',
        'doctor.justification': 'Justification',
        'doctor.justification_placeholder': 'Please provide clinical justification for this override (minimum 10 characters)...',
        'doctor.override_warning': 'This override will be permanently logged in the audit trail.',
        'doctor.confirm_override': 'Confirm Override',
        'doctor.cancel': 'Cancel',
        
        'doctor.login_title': 'Doctor Login',
        'doctor.username': 'Username',
        'doctor.password': 'Password',
        'doctor.login_btn': 'Login',
        
        // ==================== WAITING ROOM ADDITIONAL ====================
        'wait.loading_status': 'Loading your status...',
        'wait.position_label': 'Position',
        'wait.name': 'Name',
        'wait.age_gender': 'Age / Gender',
        'wait.complaint': 'Complaint',
        'wait.registered': 'Registered',
        'wait.relax': "You've been checked in. Please relax and wait for your turn.",
        'wait.immediate_attention': 'IMMEDIATE ATTENTION REQUIRED',
        'wait.stay_alert': 'Please wait, you will be called shortly',

        // ==================== CLINIC LANDING PAGE ====================
        'clinic.walkin.title': 'Walk-in Visit',
        'clinic.walkin.desc': "I'm here now and want to see a doctor today",
        'clinic.walkin.feat1': 'Quick 2-min registration',
        'clinic.walkin.feat2': 'Get priority based on symptoms',
        'clinic.walkin.feat3': 'Live queue updates',
        'clinic.book.title': 'Book Appointment',
        'clinic.book.desc': 'I want to schedule a visit for later',
        'clinic.book.feat1': 'Choose your preferred date',
        'clinic.book.feat2': 'Select your doctor',
        'clinic.book.feat3': 'No waiting on arrival',
        'btn.book_apt': 'Book Appointment',
        'clinic.existing.label': 'Already have an appointment?',
        'btn.view_appointments': 'View My Appointments',
        'clinic.track.label': 'Already registered? Find your status or upcoming appointment',
        'clinic.track.btn': 'Find My Status',

        // ==================== APPOINTMENT BOOKING PAGE ====================
        'apt.title': 'Book Your Appointment',
        'apt.select_date_doctor': 'Select Date & Doctor',
        'apt.choose_date': 'Choose Date',
        'apt.choose_doctor': 'Choose Doctor',
        'apt.available_slots_title': 'Available Time Slots',
        'apt.select_to_see': 'Select a date and doctor to see available slots',
        'apt.batch_info': 'Each slot is a batch — multiple patients can book the same time. Come at your scheduled time!',
        'apt.book_slot': 'Book This Slot',
        'apt.full': 'Full',
        'apt.slots_left': 'slots left',
        'apt.confirm_title': 'Confirm Appointment',
        'apt.date': 'Date:',
        'apt.time': 'Time:',
        'apt.doctor': 'Doctor:',
        'apt.patient': 'Patient:',
        'apt.arrive_early': 'Please arrive 10 minutes early',
        'apt.cancel_btn': 'Cancel',
        'apt.confirm_btn': 'Confirm Booking',
        'apt.loading': 'Loading appointment details...',
        'apt.confirmed_title': 'Appointment Confirmed!',
        'apt.confirmed_sub': 'Your appointment has been successfully booked',
        'apt.arrive_note': 'Please arrive 10 minutes before your appointment time',
        'apt.patient_details': 'Patient Details',
        'apt.appointment_details': 'Appointment Details',
        'apt.name': 'Name:',
        'apt.phone': 'Phone:',
        'apt.age': 'Age:',
        'apt.batch': 'Batch #:',
        'apt.reason': 'Reason for Visit',
        'apt.save_info': 'Keep this information safe!',
        'apt.my_appointments': 'My Appointments',
        'apt.print': 'Print Details',
        'apt.back_home': 'Back to Home',

        // ==================== DIRECT BOOKING PAGE ====================
        'bk.your_info': 'Your Information',
        'bk.step_info': 'Your Info',
        'bk.step_slot': 'Select Slot',
        'bk.step_confirm': 'Confirm',
        'bk.check': 'Check',
        'bk.check_hint': "We'll check if you've visited before",
        'bk.welcome_back': 'Welcome back!',
        'bk.reason_label': 'Reason for Visit',
        'bk.reason_placeholder': 'Briefly describe your reason (e.g., Checkup, Follow-up, Specific concern...)',
        'bk.select_time_slot': 'Select Time Slot',
        'bk.apt_date': 'Appointment Date',
        'bk.select_doctor': 'Select Doctor',
        'bk.find_slots': 'Find Available Slots',
        'bk.confirm_heading': 'Confirm Your Appointment',
        'bk.your_details': 'Your Details',
        'bk.age_gender': 'Age / Gender',
        'bk.change_slot': 'Change Slot',
        'bk.to_time': 'to',
        'bk.no_slots': 'No slots available for this date. Please try another date.',
        'bk.past_slot_err': 'Cannot book appointments in the past',
        'bk.visit_count': 'time(s). Last visit:',

        // ==================== MY APPOINTMENTS (ma.*) ====================
        'ma.title': 'My Appointments',
        'ma.book_new': 'Book Appointment',
        'ma.phone_label': 'Enter Phone Number',
        'ma.phone_hint': 'Please enter your registered phone number to view your appointments',
        'ma.find_btn': 'Find Appointments',
        'ma.loading': 'Loading your appointments...',
        'ma.none_found': 'No Appointments Found',
        'ma.none_hint': "You don't have any appointments with this clinic yet.",
        'ma.book_now': 'Book Now',
        'ma.upcoming': 'Upcoming Appointments',
        'ma.no_upcoming': 'No upcoming appointments',
        'ma.past': 'Past Appointments',
        'ma.no_past': 'No past appointments',
        'ma.booked_on': 'Booked on:',

        // ==================== CHECK-IN (ci.*) ====================
        'ci.title': 'Appointment Check-in',
        'ci.subtitle': 'Complete your pre-visit information',
        'ci.your_appointment': 'Your Appointment',
        'ci.already_checked': "You're Already Checked In!",
        'ci.wait_area': "Please wait in the waiting area. You'll be called when the doctor is ready.",
        'ci.pre_visit': 'Pre-Visit Questions',
        'ci.pre_visit_hint': 'Help us prepare for your visit by answering a few questions',
        'ci.chief_complaint': 'What brings you in today?',
        'ci.symptoms_label': 'Are you experiencing any of these symptoms?',
        'ci.symptoms_hint': 'Select all that apply',
        'ci.vitals_label': 'Vitals (if you know them)',
        'ci.vitals_hint': 'Optional - helps the doctor prepare',
        'ci.temp': 'Temperature (°F)',
        'ci.bp': 'Blood Pressure',
        'ci.hr': 'Heart Rate (bpm)',
        'ci.duration_label': 'How long have you had these symptoms?',
        'ci.dur_today': 'Started today',
        'ci.dur_1_3': '1-3 days',
        'ci.dur_4_7': '4-7 days',
        'ci.dur_1_2w': '1-2 weeks',
        'ci.dur_2plus': 'More than 2 weeks',
        'ci.dur_chronic': 'Ongoing/Chronic',
        'ci.complete_btn': 'Complete Check-in',
        'ci.quick_btn': 'Quick Check-in (Skip Questions)',
        'ci.checked_in': "You're Checked In!",
        'ci.notified': 'The doctor has been notified and will see you shortly.',
        'ci.wait_note': "Please have a seat in the waiting area. We'll call your name when it's your turn.",
        'ci.priority_label': 'Priority:',

        // ==================== TRIAGE RESULT (res.*) ====================
        'res.loading': 'Loading your triage result...',
        'res.patient_info': 'Patient Information',
        'res.token': 'Token #:',
        'res.status_label': 'Status:',
        'res.complaint': 'Complaint',
        'res.registered': 'Registered:',
        'res.red_flags': 'Red Flags Detected',
        'res.assessment': 'Assessment Reasons',
        'res.what_to_do': 'What would you like to do?',
        'res.walk_in_now': 'Walk-in Now',
        'res.walk_in_desc': 'Join the queue and wait for your turn',
        'res.go_waiting': 'Go to Waiting Room',
        'res.book_appt': 'Book Appointment',
        'res.book_desc': 'Choose a time slot for later',
        'res.select_slot': 'Select Time Slot',
        'res.emergency_msg': 'IMMEDIATE ATTENTION REQUIRED',
        'res.red_msg': 'Please proceed to the triage desk immediately',
        'res.amber_msg': 'You will be seen soon',
        'res.green_msg': 'Please wait comfortably to be called'
    },

    hi: {
        // ==================== COMMON ====================
        'app.name': 'स्वस्थAI',
        'app.tagline': 'त्वरित और स्मार्ट चिकित्सा ट्राइएज',
        'app.subtitle': 'तेज़, निष्पक्ष और सटीक रोगी प्राथमिकता',
        
        // Buttons
        'btn.register': 'अभी रजिस्टर करें',
        'btn.doctor_login': 'डॉक्टर लॉगिन',
        'btn.next': 'आगे',
        'btn.back': 'पीछे',
        'btn.submit': 'जमा करें',
        'btn.continue': 'जारी रखें',
        'btn.complete': 'रजिस्ट्रेशन पूरा करें',
        'btn.refresh': 'रिफ्रेश करें',
        'btn.close': 'बंद करें',
        
        // ==================== LANDING PAGE ====================
        'landing.queue': 'कतार में',
        'landing.wait': 'मिनट प्रतीक्षा',
        'landing.reg_time': 'रजिस्ट्रेशन में 2 मिनट से कम समय लगता है',
        'landing.how_it_works': 'यह कैसे काम करता है',
        
        // ==================== WELCOME / HOMEPAGE ====================
        'welcome.title': 'स्वागत है! आप कैसे आगे बढ़ना चाहेंगे?',
        'welcome.findNearby': 'पास के क्लीनिक खोजें',
        'welcome.findNearbyDesc': 'अपने स्थान के पास क्लीनिक खोजें',
        'welcome.scanQR': 'QR कोड स्कैन करें',
        'welcome.scanQRDesc': 'QR कोड का उपयोग करें या क्लीनिक कोड दर्ज करें',
        'welcome.provider': 'क्या आप एक स्वास्थ्य सेवा प्रदाता हैं?',
        
        // ==================== NEARBY CLINICS ====================
        'nearby.title': 'आपके पास के क्लीनिक',
        'nearby.useLocation': 'मेरा वर्तमान स्थान उपयोग करें',
        'nearby.sampleLocation': 'नमूना स्थान: मुंबई',
        
        // ==================== QR CODE ====================
        'qr.title': 'क्लीनिक कोड दर्ज करें',
        'qr.scanDesc': 'क्लीनिक रिसेप्शन पर QR कोड स्कैन करें या नीचे कोड दर्ज करें',
        'qr.placeholder': 'क्लीनिक कोड दर्ज करें',
        'qr.go': 'जाएं',
        'qr.scanCamera': 'कैमरे से QR स्कैन करें',
        'qr.stopCamera': 'कैमरा बंद करें',
        
        // ==================== LOGIN ====================
        'login.doctor': 'डॉक्टर लॉगिन',
        'login.admin': 'एडमिन लॉगिन',
        
        'landing.feature1_title': 'त्वरित चेक-इन',
        'landing.feature1_desc': 'अपनी तबीयत के बारे में कुछ सरल सवालों के जवाब दें। टाइप करने की जरूरत नहीं - बस टैप करें!',
        
        'landing.feature2_title': 'तुरंत प्राथमिकता',
        'landing.feature2_desc': 'अपना प्राथमिकता स्तर तुरंत पाएं। उच्च प्राथमिकता = जल्दी देखा जाएगा।',
        
        'landing.feature3_title': 'लाइव अपडेट',
        'landing.feature3_desc': 'कतार में अपनी स्थिति देखें। आपकी बारी आने पर तुरंत सूचना पाएं।',
        
        // ==================== REGISTRATION - GENERAL ====================
        'reg.title': 'मरीज पंजीकरण',
        'reg.quick_reg': 'त्वरित पंजीकरण',
        'reg.step1': 'बुनियादी जानकारी',
        'reg.step2': 'लक्षण',
        'reg.step3': 'चिकित्सा इतिहास',
        'reg.required': 'आवश्यक',
        'reg.optional': 'वैकल्पिक',
        'reg.select': 'चुनें...',
        'reg.processing': 'आपका पंजीकरण प्रोसेस हो रहा है...',
        'reg.please_wait': 'कृपया प्रतीक्षा करें',
        'reg.error': 'त्रुटि',
        'reg.network_error': 'नेटवर्क त्रुटि। कृपया पुनः प्रयास करें।',
        'reg.select_all': 'सभी लागू विकल्प चुनें',
        
        // ==================== REGISTRATION - STEP 1 ====================
        'reg.about_you': 'अपने बारे में बताएं',
        'reg.name': 'पूरा नाम',
        'reg.name_placeholder': 'अपना पूरा नाम दर्ज करें',
        'reg.age': 'उम्र',
        'reg.age_years': 'वर्ष',
        'reg.gender': 'लिंग',
        'reg.gender_male': 'पुरुष',
        'reg.gender_female': 'महिला',
        'reg.gender_other': 'अन्य',
        'reg.phone': 'फोन नंबर',
        'reg.phone_placeholder': '10 अंकों का मोबाइल नंबर',
        
        // ==================== REGISTRATION - STEP 2 ====================
        'reg.how_feeling': 'अभी आप कैसा महसूस कर रहे हैं?',
        'reg.main_complaint': 'आज आप यहाँ क्यों आए हैं?',
        'reg.complaint_pain': 'दर्द / तकलीफ',
        'reg.complaint_fever': 'बुखार / संक्रमण',
        'reg.complaint_breathing': 'सांस की समस्या',
        'reg.complaint_injury': 'चोट / दुर्घटना',
        'reg.complaint_stomach': 'पेट / पाचन समस्या',
        'reg.complaint_skin': 'त्वचा की समस्या / रैश',
        'reg.complaint_other': 'अन्य',
        
        'reg.pain_level': 'आपको कितना दर्द है?',
        'reg.pain_0': 'दर्द नहीं',
        'reg.pain_2': 'हल्का',
        'reg.pain_4': 'मध्यम',
        'reg.pain_6': 'खराब',
        'reg.pain_8': 'तेज',
        'reg.pain_10': 'सबसे तेज',
        
        'reg.emergency_title': 'क्या आप अभी इनमें से कुछ अनुभव कर रहे हैं?',
        'reg.emergency_chest': 'सीने में दर्द या दबाव',
        'reg.emergency_breathing': 'सांस लेने में कठिनाई',
        'reg.emergency_bleeding': 'भारी रक्तस्राव',
        'reg.emergency_confusion': 'भ्रम / चक्कर आना',
        
        'reg.duration': 'यह समस्या आपको कितने समय से है?',
        'reg.duration_now': 'अभी-अभी',
        'reg.duration_hours': '1 घंटे से कम',
        'reg.duration_today': 'आज (1-6 घंटे)',
        'reg.duration_yesterday': 'कल से',
        'reg.duration_days': '1-3 दिन',
        'reg.duration_week': '4-7 दिन',
        'reg.duration_longer': 'एक सप्ताह से अधिक',
        
        'reg.anything_else': 'और कुछ जो हमें पता होना चाहिए?',
        'reg.describe_briefly': 'अपने लक्षणों का संक्षेप में वर्णन करें...',
        
        // ==================== REGISTRATION - STEP 3 ====================
        'reg.medical_history': 'आपका चिकित्सा इतिहास',
        'reg.conditions': 'क्या आपको इनमें से कोई बीमारी है?',
        'reg.condition_diabetes': 'मधुमेह (डायबिटीज)',
        'reg.condition_heart': 'हृदय रोग',
        'reg.condition_bp': 'उच्च रक्तचाप (बीपी)',
        'reg.condition_asthma': 'अस्थमा / फेफड़े की बीमारी',
        'reg.condition_kidney': 'गुर्दे की बीमारी',
        'reg.condition_allergies': 'एलर्जी',
        'reg.condition_none': 'इनमें से कोई नहीं',
        
        'reg.pregnant': 'क्या आप गर्भवती हैं?',
        'reg.pregnant_yes': 'हाँ',
        'reg.pregnant_no': 'नहीं',
        'reg.pregnant_maybe': 'शायद / पता नहीं',
        
        'reg.fever': 'क्या आपको बुखार है?',
        'reg.fever_no': 'बुखार नहीं',
        'reg.fever_mild': 'हल्का (गर्म लगना)',
        'reg.fever_high': 'तेज बुखार',
        
        'reg.vitals_note': 'नोट: आपके आने पर हमारा स्टाफ आपके विटल्स (बीपी, तापमान आदि) लेगा।',
        
        // ==================== WAITING ROOM ====================
        'wait.title': 'प्रतीक्षा कक्ष',
        'wait.loading': 'आपकी स्थिति लोड हो रही है...',
        'wait.error_loading': 'जानकारी लोड करने में त्रुटि। कृपया पेज रिफ्रेश करें।',
        
        'wait.your_priority': 'आपकी प्राथमिकता',
        'wait.token': 'टोकन #',
        'wait.status': 'स्थिति',
        'wait.position': 'कतार में आपकी स्थिति',
        'wait.position_short': 'स्थिति',
        'wait.patients_ahead': 'मरीज आपसे आगे हैं',
        'wait.no_one_ahead': 'कोई आगे नहीं!',
        
        'wait.please_wait': 'कृपया प्रतीक्षा करें',
        'wait.stay_nearby': 'कृपया पास रहें',
        'wait.youre_next': 'आप अगले हैं!',
        'wait.being_called': 'आपको बुलाया जा रहा है!',
        'wait.go_now': 'कृपया अभी परामर्श कक्ष में जाएं।',
        'wait.consultation_complete': 'आपका परामर्श पूरा हो गया है',
        
        'wait.est_wait': 'अनुमानित प्रतीक्षा',
        'wait.estimated': 'अनुमानित प्रतीक्षा समय',
        'wait.approximate': 'मौजूदा कतार के आधार पर अनुमानित समय',
        'wait.your_turn_next': 'अब आपकी बारी है!',
        'wait.minutes': 'मिनट',
        'wait.connected': 'लाइव अपडेट सक्रिय',
        'wait.connecting': 'लाइव अपडेट से कनेक्ट हो रहा है...',
        'wait.reconnecting': 'कनेक्शन टूटा - पुनः कनेक्ट हो रहा है...',
        'wait.auto_update': 'यह पेज अपने आप अपडेट होगा',
        
        'wait.your_details': 'आपका विवरण',
        'wait.prefer_book': 'किसी अन्य दिन आना चाहते हैं?',
        'wait.book_instead': 'अपॉइंटमेंट बुक करें',
        'wait.detail_age': 'उम्र / लिंग',
        'wait.detail_complaint': 'शिकायत',
        'wait.detail_registered': 'पंजीकृत',
        'wait.years': 'वर्ष',
        
        'wait.important': 'महत्वपूर्ण',
        
        // ==================== PRIORITY LEVELS ====================
        'priority.emergency': 'आपातकालीन',
        'priority.emergency_msg': 'तत्काल ध्यान आवश्यक',
        'priority.emergency_sub': 'कृपया तुरंत आपातकालीन डेस्क पर जाएं',
        
        'priority.red': 'अत्यावश्यक',
        'priority.red_msg': 'उच्च प्राथमिकता',
        'priority.red_sub': 'आपको बहुत जल्द देखा जाएगा',
        
        'priority.amber': 'अर्ध-आपातकालीन',
        'priority.amber_msg': 'मध्यम प्राथमिकता',
        'priority.amber_sub': 'कृपया प्रतीक्षा करें, जल्द ही बुलाया जाएगा',
        
        'priority.green': 'सामान्य',
        'priority.green_msg': 'सामान्य कतार',
        'priority.green_sub': 'कृपया आराम से बैठें, हम आपको बुलाएंगे',
        
        // ==================== STATUS LABELS ====================
        'status.waiting': 'प्रतीक्षा में',
        'status.consulting': 'परामर्श में',
        'status.completed': 'पूर्ण',
        
        // ==================== NOTIFICATIONS ====================
        'notif.your_turn': 'आपकी बारी!',
        'notif.proceed': 'कृपया परामर्श कक्ष में जाएं',
        
        // ==================== ERRORS ====================
        'error.required_field': 'यह फ़ील्ड आवश्यक है',
        'error.invalid_phone': 'कृपया वैध फोन नंबर दर्ज करें',
        'error.invalid_age': 'कृपया वैध उम्र दर्ज करें',
        'error.select_option': 'कृपया एक विकल्प चुनें',
        'error.try_again': 'कृपया पुनः प्रयास करें',
        
        // ==================== DOCTOR DASHBOARD ====================
        'doctor.title': 'डॉक्टर डैशबोर्ड',
        'doctor.portal': 'डॉक्टर पोर्टल',
        'doctor.logout': 'लॉगआउट',
        'changePassword': 'पासवर्ड बदलें',
        'setupPassword': 'पासवर्ड सेट करें',
        'setupPasswordDesc': 'अपने खाते के लिए एक सुरक्षित पासवर्ड बनाएं',
        'email': 'ईमेल',
        'tempPassword': 'अस्थायी पासवर्ड',
        'enterTempPassword': 'आपको दिया गया अस्थायी पासवर्ड दर्ज करें',
        'newPassword': 'नया पासवर्ड',
        'passwordRequirements': 'कम से कम 8 अक्षर',
        'confirmPassword': 'पासवर्ड की पुष्टि करें',
        'confirmNewPassword': 'नए पासवर्ड की पुष्टि करें',
        'setPassword': 'पासवर्ड सेट करें',
        'backToLogin': '← लॉगिन पर वापस',
        'currentPassword': 'वर्तमान पासवर्ड',
        'updatePassword': 'पासवर्ड अपडेट करें',
        'backToDashboard': '← डैशबोर्ड पर वापस',
        'doctor.patient_queue': 'मरीज़ों की कतार',
        'doctor.refresh': 'रिफ्रेश करें',
        'doctor.loading_queue': 'कतार लोड हो रही है...',
        'doctor.no_patients': 'कतार में कोई मरीज़ नहीं',
        'doctor.connecting': 'लाइव अपडेट से कनेक्ट हो रहा है...',
        'doctor.live_active': 'लाइव अपडेट सक्रिय',
        'doctor.connection_lost': 'कनेक्शन टूटा - पुनः कनेक्ट हो रहा है...',
        
        'doctor.token': 'टोकन',
        'doctor.patient': 'मरीज़',
        'doctor.complaint': 'शिकायत',
        'doctor.waiting': 'प्रतीक्षा',
        'doctor.actions': 'कार्रवाई',
        'doctor.years_short': 'वर्ष',
        'doctor.min_ago': 'मिनट पहले',
        'doctor.hour_ago': 'घंटा पहले',
        'doctor.just_now': 'अभी-अभी',
        
        'doctor.view_details': 'विवरण देखें',
        'doctor.patient_details': 'मरीज़ विवरण',
        'doctor.clinical_data': 'क्लिनिकल डेटा',
        'doctor.triage_result': 'ट्राइएज परिणाम',
        'doctor.red_flags': 'रेड फ्लैग्स',
        'doctor.no_red_flags': 'कोई नहीं मिला',
        
        'doctor.override': 'प्राथमिकता बदलें',
        'doctor.current_priority': 'वर्तमान प्राथमिकता',
        'doctor.new_priority': 'नई प्राथमिकता',
        'doctor.select_priority': 'नई प्राथमिकता चुनें...',
        'doctor.justification': 'कारण',
        'doctor.justification_placeholder': 'कृपया इस बदलाव का नैदानिक कारण बताएं (न्यूनतम 10 अक्षर)...',
        'doctor.override_warning': 'यह बदलाव ऑडिट ट्रेल में स्थायी रूप से लॉग किया जाएगा।',
        'doctor.confirm_override': 'बदलाव की पुष्टि करें',
        'doctor.cancel': 'रद्द करें',
        
        'doctor.login_title': 'डॉक्टर लॉगिन',
        'doctor.username': 'यूज़रनेम',
        'doctor.password': 'पासवर्ड',
        'doctor.login_btn': 'लॉगिन',
        
        // ==================== WAITING ROOM ADDITIONAL ====================
        'wait.loading_status': 'आपकी स्थिति लोड हो रही है...',
        'wait.position_label': 'स्थिति',
        'wait.name': 'नाम',
        'wait.age_gender': 'उम्र / लिंग',
        'wait.complaint': 'शिकायत',
        'wait.registered': 'पंजीकृत',
        'wait.relax': 'आपको चेक-इन कर लिया गया है। कृपया आराम करें और अपनी बारी का इंतजार करें।',
        'wait.immediate_attention': 'तत्काल ध्यान आवश्यक',
        'wait.stay_alert': 'कृपया प्रतीक्षा करें, जल्द ही बुलाया जाएगा',

        // ==================== CLINIC LANDING PAGE ====================
        'clinic.walkin.title': 'वॉक-इन विजिट',
        'clinic.walkin.desc': 'मैं अभी यहाँ हूँ और आज डॉक्टर से मिलना चाहता/चाहती हूँ',
        'clinic.walkin.feat1': '2 मिनट में त्वरित पंजीकरण',
        'clinic.walkin.feat2': 'लक्षणों के आधार पर प्राथमिकता पाएं',
        'clinic.walkin.feat3': 'लाइव कतार अपडेट',
        'clinic.book.title': 'अपॉइंटमेंट बुक करें',
        'clinic.book.desc': 'मैं बाद के लिए विजिट शेड्यूल करना चाहता/चाहती हूँ',
        'clinic.book.feat1': 'अपनी पसंदीदा तारीख चुनें',
        'clinic.book.feat2': 'अपना डॉक्टर चुनें',
        'clinic.book.feat3': 'आने पर प्रतीक्षा नहीं',
        'btn.book_apt': 'अपॉइंटमेंट बुक करें',
        'clinic.existing.label': 'पहले से अपॉइंटमेंट है?',
        'btn.view_appointments': 'मेरे अपॉइंटमेंट देखें',
        'clinic.track.label': 'नोंदणी की है? अपनी स्थिति या अपॉइंटमेंट देखें',
        'clinic.track.btn': 'मेरी स्थिति खोजें',

        // ==================== APPOINTMENT BOOKING PAGE ====================
        'apt.title': 'अपॉइंटमेंट बुक करें',
        'apt.select_date_doctor': 'तारीख और डॉक्टर चुनें',
        'apt.choose_date': 'तारीख चुनें',
        'apt.choose_doctor': 'डॉक्टर चुनें',
        'apt.available_slots_title': 'उपलब्ध समय स्लॉट',
        'apt.select_to_see': 'स्लॉट देखने के लिए तारीख और डॉक्टर चुनें',
        'apt.batch_info': 'हर स्लॉट एक बैच है — कई मरीज़ एक ही समय बुक कर सकते हैं। अपने निर्धारित समय पर आएं।',
        'apt.book_slot': 'यह स्लॉट बुक करें',
        'apt.full': 'भरा हुआ',
        'apt.slots_left': 'स्लॉट बाकी',
        'apt.confirm_title': 'अपॉइंटमेंट की पुष्टि करें',
        'apt.date': 'तारीख:',
        'apt.time': 'समय:',
        'apt.doctor': 'डॉक्टर:',
        'apt.patient': 'मरीज़:',
        'apt.arrive_early': 'कृपया 10 मिनट पहले पहुंचें',
        'apt.cancel_btn': 'रद्द करें',
        'apt.confirm_btn': 'बुकिंग की पुष्टि करें',
        'apt.loading': 'अपॉइंटमेंट विवरण लोड हो रहा है...',
        'apt.confirmed_title': 'अपॉइंटमेंट की पुष्टि हो गई!',
        'apt.confirmed_sub': 'आपका अपॉइंटमेंट सफलतापूर्वक बुक हो गया है',
        'apt.arrive_note': 'कृपया अपने अपॉइंटमेंट समय से 10 मिनट पहले आएं',
        'apt.patient_details': 'मरीज़ का विवरण',
        'apt.appointment_details': 'अपॉइंटमेंट विवरण',
        'apt.name': 'नाम:',
        'apt.phone': 'फोन:',
        'apt.age': 'उम्र:',
        'apt.batch': 'बैच #:',
        'apt.reason': 'यात्रा का कारण',
        'apt.save_info': 'यह जानकारी सुरक्षित रखें!',
        'apt.my_appointments': 'मेरे अपॉइंटमेंट',
        'apt.print': 'विवरण प्रिंट करें',
        'apt.back_home': 'होम पेज पर जाएं',

        // ==================== DIRECT BOOKING PAGE ====================
        'bk.your_info': 'आपकी जानकारी',
        'bk.step_info': 'जानकारी',
        'bk.step_slot': 'समय चुनें',
        'bk.step_confirm': 'पुष्टि करें',
        'bk.check': 'जाँचें',
        'bk.check_hint': 'हम देखेंगे कि आप पहले आ चुके हैं',
        'bk.welcome_back': 'फिर स्वागत है!',
        'bk.reason_label': 'मिलने का कारण',
        'bk.reason_placeholder': 'अपने आने का कारण संक्षेप में बताएं',
        'bk.select_time_slot': 'समय स्लॉट चुनें',
        'bk.apt_date': 'अपॉइंटमेंट की तारीख',
        'bk.select_doctor': 'डॉक्टर चुनें',
        'bk.find_slots': 'उपलब्ध स्लॉट खोजें',
        'bk.confirm_heading': 'अपॉइंटमेंट की पुष्टि करें',
        'bk.your_details': 'आपका विवरण',
        'bk.age_gender': 'उम्र / लिंग',
        'bk.change_slot': 'स्लॉट बदलें',
        'bk.to_time': 'से',
        'bk.no_slots': 'इस तारीख के लिए कोई स्लॉट उपलब्ध नहीं है। कृपया दूसरी तारीख चुनें।',
        'bk.past_slot_err': 'बीते हुए समय के लिए अपॉइंटमेंट नहीं बुक कर सकते',
        'bk.visit_count': 'बार। अंतिम यात्रा:',

        // ==================== MY APPOINTMENTS (ma.*) ====================
        'ma.title': 'मेरी अपॉइंटमेंट',
        'ma.book_new': 'अपॉइंटमेंट बुक करें',
        'ma.phone_label': 'फोन नंबर दर्ज करें',
        'ma.phone_hint': 'अपनी अपॉइंटमेंट देखने के लिए अपना पंजीकृत फोन नंबर दर्ज करें',
        'ma.find_btn': 'अपॉइंटमेंट खोजें',
        'ma.loading': 'आपकी अपॉइंटमेंट लोड हो रही हैं...',
        'ma.none_found': 'कोई अपॉइंटमेंट नहीं मिली',
        'ma.none_hint': 'इस क्लिनिक में अभी तक आपकी कोई अपॉइंटमेंट नहीं है।',
        'ma.book_now': 'अभी बुक करें',
        'ma.upcoming': 'आगामी अपॉइंटमेंट',
        'ma.no_upcoming': 'कोई आगामी अपॉइंटमेंट नहीं',
        'ma.past': 'पिछली अपॉइंटमेंट',
        'ma.no_past': 'कोई पिछली अपॉइंटमेंट नहीं',
        'ma.booked_on': 'बुकिंग की तारीख:',

        // ==================== CHECK-IN (ci.*) ====================
        'ci.title': 'अपॉइंटमेंट चेक-इन',
        'ci.subtitle': 'अपनी पूर्व-यात्रा जानकारी पूरी करें',
        'ci.your_appointment': 'आपकी अपॉइंटमेंट',
        'ci.already_checked': 'आप पहले से चेक-इन हैं!',
        'ci.wait_area': 'कृपया प्रतीक्षा क्षेत्र में बैठें। जब डॉक्टर तैयार होंगे तो आपको बुलाया जाएगा।',
        'ci.pre_visit': 'पूर्व-यात्रा प्रश्न',
        'ci.pre_visit_hint': 'कुछ प्रश्नों का उत्तर देकर हमें आपकी यात्रा के लिए तैयार करने में मदद करें',
        'ci.chief_complaint': 'आज आप यहाँ क्यों आए हैं?',
        'ci.symptoms_label': 'क्या आप इनमें से कोई लक्षण अनुभव कर रहे हैं?',
        'ci.symptoms_hint': 'जो भी लागू हो उसे चुनें',
        'ci.vitals_label': 'जीवन संकेत (यदि आप जानते हैं)',
        'ci.vitals_hint': 'वैकल्पिक - डॉक्टर को तैयारी में मदद करता है',
        'ci.temp': 'तापमान (°F)',
        'ci.bp': 'रक्तचाप',
        'ci.hr': 'हृदय गति (bpm)',
        'ci.duration_label': 'ये लक्षण कितने समय से हैं?',
        'ci.dur_today': 'आज से शुरू हुआ',
        'ci.dur_1_3': '1-3 दिन',
        'ci.dur_4_7': '4-7 दिन',
        'ci.dur_1_2w': '1-2 सप्ताह',
        'ci.dur_2plus': '2 सप्ताह से अधिक',
        'ci.dur_chronic': 'चल रहा / पुराना',
        'ci.complete_btn': 'चेक-इन पूरा करें',
        'ci.quick_btn': 'त्वरित चेक-इन (प्रश्न छोड़ें)',
        'ci.checked_in': 'आपका चेक-इन हो गया!',
        'ci.notified': 'डॉक्टर को सूचित कर दिया गया है और वे जल्द ही आपसे मिलेंगे।',
        'ci.wait_note': 'कृपया प्रतीक्षा क्षेत्र में बैठें। जब आपकी बारी होगी तो हम आपका नाम पुकारेंगे।',
        'ci.priority_label': 'प्राथमिकता:',

        // ==================== TRIAGE RESULT (res.*) ====================
        'res.loading': 'आपका ट्राइएज परिणाम लोड हो रहा है...',
        'res.patient_info': 'मरीज़ की जानकारी',
        'res.token': 'टोकन नंबर:',
        'res.status_label': 'स्थिति:',
        'res.complaint': 'शिकायत',
        'res.registered': 'पंजीकरण:',
        'res.red_flags': 'लाल झंडे मिले',
        'res.assessment': 'मूल्यांकन के कारण',
        'res.what_to_do': 'आप क्या करना चाहेंगे?',
        'res.walk_in_now': 'अभी आएं',
        'res.walk_in_desc': 'कतार में शामिल हों और अपनी बारी का इंतज़ार करें',
        'res.go_waiting': 'प्रतीक्षा कक्ष जाएं',
        'res.book_appt': 'अपॉइंटमेंट बुक करें',
        'res.book_desc': 'बाद के लिए समय स्लॉट चुनें',
        'res.select_slot': 'समय स्लॉट चुनें',
        'res.emergency_msg': 'तुरंत ध्यान देने की आवश्यकता है',
        'res.red_msg': 'कृपया ट्राइएज डेस्क पर तुरंत जाएं',
        'res.amber_msg': 'आपको जल्द ही देखा जाएगा',
        'res.green_msg': 'बुलाए जाने का इंतज़ार करें'
    },
    
    mr: {
        // ==================== COMMON ====================
        'app.name': 'स्वस्थAI',
        'app.tagline': 'जलद आणि स्मार्ट वैद्यकीय ट्रायएज',
        'app.subtitle': 'जलद, निष्पक्ष आणि अचूक रुग्ण प्राधान्य',
        
        // Buttons
        'btn.register': 'आता नोंदणी करा',
        'btn.doctor_login': 'डॉक्टर लॉगिन',
        'btn.next': 'पुढे',
        'btn.back': 'मागे',
        'btn.submit': 'सबमिट करा',
        'btn.continue': 'सुरू ठेवा',
        'btn.complete': 'नोंदणी पूर्ण करा',
        'btn.refresh': 'रिफ्रेश करा',
        'btn.close': 'बंद करा',
        
        // ==================== LANDING PAGE ====================
        'landing.queue': 'रांगेत',
        'landing.wait': 'मिनिट प्रतीक्षा',
        'landing.reg_time': 'नोंदणीसाठी 2 मिनिटांपेक्षा कमी वेळ लागतो',
        'landing.how_it_works': 'हे कसे काम करते',
        
        // ==================== WELCOME / HOMEPAGE ====================
        'welcome.title': 'स्वागत आहे! तुम्ही कसे पुढे जाऊ इच्छिता?',
        'welcome.findNearby': 'जवळपासचे क्लिनिक शोधा',
        'welcome.findNearbyDesc': 'तुमच्या ठिकाणाजवळील क्लिनिक शोधा',
        'welcome.scanQR': 'QR कोड स्कॅन करा',
        'welcome.scanQRDesc': 'QR कोड वापरा किंवा क्लिनिक कोड प्रविष्ट करा',
        'welcome.provider': 'तुम्ही आरोग्य सेवा प्रदाता आहात का?',
        
        // ==================== NEARBY CLINICS ====================
        'nearby.title': 'तुमच्या जवळपासचे क्लिनिक',
        'nearby.useLocation': 'माझे वर्तमान स्थान वापरा',
        'nearby.sampleLocation': 'नमुना स्थान: मुंबई',
        
        // ==================== QR CODE ====================
        'qr.title': 'क्लिनिक कोड प्रविष्ट करा',
        'qr.scanDesc': 'क्लिनिक रिसेप्शनवर QR कोड स्कॅन करा किंवा खाली कोड प्रविष्ट करा',
        'qr.placeholder': 'क्लिनिक कोड प्रविष्ट करा',
        'qr.go': 'जा',
        'qr.scanCamera': 'कॅमेऱ्याने QR स्कॅन करा',
        'qr.stopCamera': 'कॅमेरा थांबवा',
        
        // ==================== LOGIN ====================
        'login.doctor': 'डॉक्टर लॉगिन',
        'login.admin': 'प्रशासक लॉगिन',
        
        'landing.feature1_title': 'जलद चेक-इन',
        'landing.feature1_desc': 'तुम्हाला कसे वाटते याबद्दल काही सोप्या प्रश्नांची उत्तरे द्या. टाइप करण्याची गरज नाही - फक्त टॅप करा!',
        
        'landing.feature2_title': 'त्वरित प्राधान्य',
        'landing.feature2_desc': 'तुमचे प्राधान्य स्तर लगेच मिळवा. जास्त प्राधान्य = लवकर भेट.',
        
        'landing.feature3_title': 'लाइव्ह अपडेट',
        'landing.feature3_desc': 'रांगेतील तुमची स्थिती पहा. तुमची पाळी आल्यावर लगेच सूचना मिळवा.',
        
        // ==================== REGISTRATION - GENERAL ====================
        'reg.title': 'रुग्ण नोंदणी',
        'reg.quick_reg': 'जलद नोंदणी',
        'reg.step1': 'मूलभूत माहिती',
        'reg.step2': 'लक्षणे',
        'reg.step3': 'वैद्यकीय इतिहास',
        'reg.required': 'आवश्यक',
        'reg.optional': 'पर्यायी',
        'reg.select': 'निवडा...',
        'reg.processing': 'तुमची नोंदणी प्रक्रिया होत आहे...',
        'reg.please_wait': 'कृपया प्रतीक्षा करा',
        'reg.error': 'त्रुटी',
        'reg.network_error': 'नेटवर्क त्रुटी. कृपया पुन्हा प्रयत्न करा.',
        'reg.select_all': 'लागू असलेले सर्व निवडा',
        
        // ==================== REGISTRATION - STEP 1 ====================
        'reg.about_you': 'तुमच्याबद्दल सांगा',
        'reg.name': 'पूर्ण नाव',
        'reg.name_placeholder': 'तुमचे पूर्ण नाव टाका',
        'reg.age': 'वय',
        'reg.age_years': 'वर्षे',
        'reg.gender': 'लिंग',
        'reg.gender_male': 'पुरुष',
        'reg.gender_female': 'स्त्री',
        'reg.gender_other': 'इतर',
        'reg.phone': 'फोन नंबर',
        'reg.phone_placeholder': '10 अंकी मोबाइल नंबर',
        
        // ==================== REGISTRATION - STEP 2 ====================
        'reg.how_feeling': 'तुम्हाला आत्ता कसे वाटत आहे?',
        'reg.main_complaint': 'तुम्ही आज इथे का आलात?',
        'reg.complaint_pain': 'वेदना / अस्वस्थता',
        'reg.complaint_fever': 'ताप / संसर्ग',
        'reg.complaint_breathing': 'श्वासोच्छवासाची समस्या',
        'reg.complaint_injury': 'दुखापत / अपघात',
        'reg.complaint_stomach': 'पोट / पचन समस्या',
        'reg.complaint_skin': 'त्वचा समस्या / पुरळ',
        'reg.complaint_other': 'इतर',
        
        'reg.pain_level': 'तुम्हाला किती वेदना होत आहेत?',
        'reg.pain_0': 'वेदना नाही',
        'reg.pain_2': 'सौम्य',
        'reg.pain_4': 'मध्यम',
        'reg.pain_6': 'वाईट',
        'reg.pain_8': 'तीव्र',
        'reg.pain_10': 'सर्वात वाईट',
        
        'reg.emergency_title': 'तुम्हाला आत्ता यापैकी काही अनुभवत आहे का?',
        'reg.emergency_chest': 'छातीत दुखणे किंवा दाब',
        'reg.emergency_breathing': 'श्वास घेण्यास त्रास',
        'reg.emergency_bleeding': 'जास्त रक्तस्राव',
        'reg.emergency_confusion': 'गोंधळ / चक्कर येणे',
        
        'reg.duration': 'ही समस्या तुम्हाला किती काळापासून आहे?',
        'reg.duration_now': 'आत्ताच',
        'reg.duration_hours': '1 तासापेक्षा कमी',
        'reg.duration_today': 'आज (1-6 तास)',
        'reg.duration_yesterday': 'कालपासून',
        'reg.duration_days': '1-3 दिवस',
        'reg.duration_week': '4-7 दिवस',
        'reg.duration_longer': 'एका आठवड्यापेक्षा जास्त',
        
        'reg.anything_else': 'आणखी काही आम्हाला माहित असावे?',
        'reg.describe_briefly': 'तुमच्या लक्षणांचे थोडक्यात वर्णन करा...',
        
        // ==================== REGISTRATION - STEP 3 ====================
        'reg.medical_history': 'तुमचा वैद्यकीय इतिहास',
        'reg.conditions': 'तुम्हाला यापैकी कोणता आजार आहे का?',
        'reg.condition_diabetes': 'मधुमेह (डायबिटीज)',
        'reg.condition_heart': 'हृदयरोग',
        'reg.condition_bp': 'उच्च रक्तदाब (बीपी)',
        'reg.condition_asthma': 'दमा / फुफ्फुसाचा आजार',
        'reg.condition_kidney': 'मूत्रपिंडाचा आजार',
        'reg.condition_allergies': 'अॅलर्जी',
        'reg.condition_none': 'यापैकी काहीही नाही',
        
        'reg.pregnant': 'तुम्ही गर्भवती आहात का?',
        'reg.pregnant_yes': 'हो',
        'reg.pregnant_no': 'नाही',
        'reg.pregnant_maybe': 'कदाचित / माहित नाही',
        
        'reg.fever': 'तुम्हाला ताप आहे का?',
        'reg.fever_no': 'ताप नाही',
        'reg.fever_mild': 'सौम्य (उबदार वाटणे)',
        'reg.fever_high': 'जास्त ताप',
        
        'reg.vitals_note': 'टीप: तुम्ही आल्यावर आमचे कर्मचारी तुमचे व्हायटल्स (बीपी, तापमान इ.) घेतील.',
        
        // ==================== WAITING ROOM ====================
        'wait.title': 'प्रतीक्षा कक्ष',
        'wait.loading': 'तुमची स्थिती लोड होत आहे...',
        'wait.error_loading': 'माहिती लोड करण्यात त्रुटी. कृपया पेज रिफ्रेश करा.',
        
        'wait.your_priority': 'तुमचे प्राधान्य',
        'wait.token': 'टोकन #',
        'wait.status': 'स्थिती',
        'wait.position': 'रांगेतील तुमची स्थिती',
        'wait.position_short': 'स्थिती',
        'wait.patients_ahead': 'रुग्ण तुमच्या पुढे आहेत',
        'wait.no_one_ahead': 'कोणी पुढे नाही!',
        
        'wait.please_wait': 'कृपया प्रतीक्षा करा',
        'wait.stay_nearby': 'कृपया जवळच रहा',
        'wait.youre_next': 'तुम्ही पुढचे आहात!',
        'wait.being_called': 'तुम्हाला बोलावले जात आहे!',
        'wait.go_now': 'कृपया आता सल्लामसलत कक्षात जा.',
        'wait.consultation_complete': 'तुमची सल्लामसलत पूर्ण झाली',
        
        'wait.est_wait': 'अंदाजे प्रतीक्षा',
        'wait.estimated': 'अंदाजे प्रतीक्षा वेळ',
        'wait.approximate': 'सध्याच्या रांगेवर आधारित अंदाजे वेळ',
        'wait.your_turn_next': 'आता तुमची पाळी!',
        'wait.minutes': 'मिनिटे',
        'wait.connected': 'लाइव्ह अपडेट सक्रिय',
        'wait.connecting': 'लाइव्ह अपडेटशी कनेक्ट होत आहे...',
        'wait.reconnecting': 'कनेक्शन तुटले - पुन्हा कनेक्ट होत आहे...',
        'wait.auto_update': 'हे पेज आपोआप अपडेट होईल',
        
        'wait.your_details': 'तुमचा तपशील',
        'wait.prefer_book': 'वेगळ्या दिवशी भेट द्यायची आहे?',
        'wait.book_instead': 'भेट बुक करा',
        'wait.detail_age': 'वय / लिंग',
        'wait.detail_complaint': 'तक्रार',
        'wait.detail_registered': 'नोंदणीकृत',
        'wait.years': 'वर्षे',
        
        'wait.important': 'महत्त्वाचे',
        
        // ==================== PRIORITY LEVELS ====================
        'priority.emergency': 'आणीबाणी',
        'priority.emergency_msg': 'त्वरित लक्ष आवश्यक',
        'priority.emergency_sub': 'कृपया लगेच आणीबाणी डेस्कवर जा',
        
        'priority.red': 'अत्यावश्यक',
        'priority.red_msg': 'उच्च प्राधान्य',
        'priority.red_sub': 'तुम्हाला लवकरच भेटवले जाईल',
        
        'priority.amber': 'अर्ध-आणीबाणी',
        'priority.amber_msg': 'मध्यम प्राधान्य',
        'priority.amber_sub': 'कृपया प्रतीक्षा करा, लवकरच बोलावले जाईल',
        
        'priority.green': 'सामान्य',
        'priority.green_msg': 'सामान्य रांग',
        'priority.green_sub': 'कृपया आरामात बसा, आम्ही तुम्हाला बोलावू',
        
        // ==================== STATUS LABELS ====================
        'status.waiting': 'प्रतीक्षेत',
        'status.consulting': 'सल्लामसलतीत',
        'status.completed': 'पूर्ण',
        
        // ==================== NOTIFICATIONS ====================
        'notif.your_turn': 'तुमची पाळी!',
        'notif.proceed': 'कृपया सल्लामसलत कक्षात जा',
        
        // ==================== ERRORS ====================
        'error.required_field': 'हे फील्ड आवश्यक आहे',
        'error.invalid_phone': 'कृपया वैध फोन नंबर टाका',
        'error.invalid_age': 'कृपया वैध वय टाका',
        'error.select_option': 'कृपया एक पर्याय निवडा',
        'error.try_again': 'कृपया पुन्हा प्रयत्न करा',
        
        // ==================== DOCTOR DASHBOARD ====================
        'doctor.title': 'डॉक्टर डॅशबोर्ड',
        'doctor.portal': 'डॉक्टर पोर्टल',
        'doctor.logout': 'लॉगआउट',
        'changePassword': 'पासवर्ड बदला',
        'setupPassword': 'पासवर्ड सेट करा',
        'setupPasswordDesc': 'तुमच्या खात्यासाठी सुरक्षित पासवर्ड तयार करा',
        'email': 'ईमेल',
        'tempPassword': 'तात्पुरता पासवर्ड',
        'enterTempPassword': 'तुम्हाला दिलेला तात्पुरता पासवर्ड टाका',
        'newPassword': 'नवीन पासवर्ड',
        'passwordRequirements': 'किमान 8 अक्षरे',
        'confirmPassword': 'पासवर्ड पुष्टी करा',
        'confirmNewPassword': 'नवीन पासवर्ड पुष्टी करा',
        'setPassword': 'पासवर्ड सेट करा',
        'backToLogin': '← लॉगिनवर परत',
        'currentPassword': 'सध्याचा पासवर्ड',
        'updatePassword': 'पासवर्ड अपडेट करा',
        'backToDashboard': '← डॅशबोर्डवर परत',
        'doctor.patient_queue': 'रुग्णांची रांग',
        'doctor.refresh': 'रिफ्रेश करा',
        'doctor.loading_queue': 'रांग लोड होत आहे...',
        'doctor.no_patients': 'रांगेत रुग्ण नाहीत',
        'doctor.connecting': 'लाइव्ह अपडेटशी कनेक्ट होत आहे...',
        'doctor.live_active': 'लाइव्ह अपडेट सक्रिय',
        'doctor.connection_lost': 'कनेक्शन तुटले - पुन्हा कनेक्ट होत आहे...',
        
        'doctor.token': 'टोकन',
        'doctor.patient': 'रुग्ण',
        'doctor.complaint': 'तक्रार',
        'doctor.waiting': 'प्रतीक्षा',
        'doctor.actions': 'कृती',
        'doctor.years_short': 'वर्षे',
        'doctor.min_ago': 'मिनिटांपूर्वी',
        'doctor.hour_ago': 'तासापूर्वी',
        'doctor.just_now': 'आत्ताच',
        
        'doctor.view_details': 'तपशील पहा',
        'doctor.patient_details': 'रुग्ण तपशील',
        'doctor.clinical_data': 'क्लिनिकल डेटा',
        'doctor.triage_result': 'ट्रायएज निकाल',
        'doctor.red_flags': 'रेड फ्लॅग्स',
        'doctor.no_red_flags': 'काहीही आढळले नाही',
        
        'doctor.override': 'प्राधान्य बदला',
        'doctor.current_priority': 'सध्याचे प्राधान्य',
        'doctor.new_priority': 'नवीन प्राधान्य',
        'doctor.select_priority': 'नवीन प्राधान्य निवडा...',
        'doctor.justification': 'कारण',
        'doctor.justification_placeholder': 'कृपया या बदलाचे वैद्यकीय कारण द्या (किमान 10 अक्षरे)...',
        'doctor.override_warning': 'हा बदल ऑडिट ट्रेलमध्ये कायमस्वरूपी लॉग केला जाईल.',
        'doctor.confirm_override': 'बदल निश्चित करा',
        'doctor.cancel': 'रद्द करा',
        
        'doctor.login_title': 'डॉक्टर लॉगिन',
        'doctor.username': 'युजरनेम',
        'doctor.password': 'पासवर्ड',
        'doctor.login_btn': 'लॉगिन',
        
        // ==================== WAITING ROOM ADDITIONAL ====================
        'wait.loading_status': 'तुमची स्थिती लोड होत आहे...',
        'wait.position_label': 'स्थिती',
        'wait.name': 'नाव',
        'wait.age_gender': 'वय / लिंग',
        'wait.complaint': 'तक्रार',
        'wait.registered': 'नोंदणीकृत',
        'wait.relax': 'तुम्हाला चेक-इन केले आहे. कृपया आराम करा आणि तुमच्या वेळेची प्रतीक्षा करा.',
        'wait.immediate_attention': 'त्वरित लक्ष आवश्यक',
        'wait.stay_alert': 'कृपया प्रतीक्षा करा, लवकरच बोलावले जाईल',

        // ==================== CLINIC LANDING PAGE ====================
        'clinic.walkin.title': 'वॉक-इन भेट',
        'clinic.walkin.desc': 'मी आत्ता इथे आहे आणि आज डॉक्टरांना भेटायचे आहे',
        'clinic.walkin.feat1': '2 मिनिटांत जलद नोंदणी',
        'clinic.walkin.feat2': 'लक्षणांवर आधारित प्राधान्य मिळवा',
        'clinic.walkin.feat3': 'लाइव्ह रांग अपडेट',
        'clinic.book.title': 'भेट बुक करा',
        'clinic.book.desc': 'मला नंतरसाठी भेट शेड्यूल करायची आहे',
        'clinic.book.feat1': 'तुमची पसंतीची तारीख निवडा',
        'clinic.book.feat2': 'तुमचे डॉक्टर निवडा',
        'clinic.book.feat3': 'येताना प्रतीक्षा नाही',
        'btn.book_apt': 'भेट बुक करा',
        'clinic.existing.label': 'आधीपासून भेट आहे?',
        'btn.view_appointments': 'माझ्या भेटी पहा',
        'clinic.track.label': 'नोंदणी केली आहे? तुमची स्थिती किंवा भेट पहा',
        'clinic.track.btn': 'माझी स्थिती शोधा',

        // ==================== APPOINTMENT BOOKING PAGE ====================
        'apt.title': 'भेट बुक करा',
        'apt.select_date_doctor': 'तारीख आणि डॉक्टर निवडा',
        'apt.choose_date': 'तारीख निवडा',
        'apt.choose_doctor': 'डॉक्टर निवडा',
        'apt.available_slots_title': 'उपलब्ध वेळ स्लॉट',
        'apt.select_to_see': 'स्लॉट पाहण्यासाठी तारीख आणि डॉक्टर निवडा',
        'apt.batch_info': 'प्रत्येक स्लॉट एक बॅच आहे — अनेक रुग्ण एकाच वेळी बुक करू शकतात. ठरलेल्या वेळी या.',
        'apt.book_slot': 'हा स्लॉट बुक करा',
        'apt.full': 'भरलेला',
        'apt.slots_left': 'स्लॉट शिल्लक',
        'apt.confirm_title': 'भेट पुष्ट करा',
        'apt.date': 'तारीख:',
        'apt.time': 'वेळ:',
        'apt.doctor': 'डॉक्टर:',
        'apt.patient': 'रुग्ण:',
        'apt.arrive_early': 'कृपया 10 मिनिटे आधी या',
        'apt.cancel_btn': 'रद्द करा',
        'apt.confirm_btn': 'बुकिंग पुष्ट करा',
        'apt.loading': 'भेट तपशील लोड होत आहे...',
        'apt.confirmed_title': 'भेट पुष्ट झाली!',
        'apt.confirmed_sub': 'तुमची भेट यशस्वीरित्या बुक झाली आहे',
        'apt.arrive_note': 'कृपया भेटीच्या वेळेआधी 10 मिनिटे या',
        'apt.patient_details': 'रुग्ण तपशील',
        'apt.appointment_details': 'भेट तपशील',
        'apt.name': 'नाव:',
        'apt.phone': 'फोन:',
        'apt.age': 'वय:',
        'apt.batch': 'बॅच #:',
        'apt.reason': 'भेटीचे कारण',
        'apt.save_info': 'ही माहिती सुरक्षित ठेवा!',
        'apt.my_appointments': 'माझ्या भेटी',
        'apt.print': 'तपशील प्रिंट करा',
        'apt.back_home': 'मुख पृष्ठावर जा',

        // ==================== DIRECT BOOKING PAGE ====================
        'bk.your_info': 'तुमची माहिती',
        'bk.step_info': 'माहिती',
        'bk.step_slot': 'वेळ निवडा',
        'bk.step_confirm': 'पुष्टी करा',
        'bk.check': 'तपासा',
        'bk.check_hint': 'आम्ही तपासू की तुम्ही आधी आला आहात',
        'bk.welcome_back': 'पुन्हा स्वागत आहे!',
        'bk.reason_label': 'भेटीचे कारण',
        'bk.reason_placeholder': 'तुमच्या भेटीचे कारण थोडक्यात सांगा',
        'bk.select_time_slot': 'वेळ स्लॉट निवडा',
        'bk.apt_date': 'भेटीची तारीख',
        'bk.select_doctor': 'डॉक्टर निवडा',
        'bk.find_slots': 'उपलब्ध स्लॉट शोधा',
        'bk.confirm_heading': 'तुमची भेट निश्चित करा',
        'bk.your_details': 'तुमचा तपशील',
        'bk.age_gender': 'वय / लिंग',
        'bk.change_slot': 'स्लॉट बदला',
        'bk.to_time': 'ते',
        'bk.no_slots': 'या तारखेसाठी कोणतेही स्लॉट उपलब्ध नाहीत. कृपया दुसरी तारीख निवडा.',
        'bk.past_slot_err': 'भूतकाळातील वेळेसाठी भेट बुक करता येत नाही',
        'bk.visit_count': 'वेळा. शेवटची भेट:',

        // ==================== MY APPOINTMENTS (ma.*) ====================
        'ma.title': 'माझ्या भेटी',
        'ma.book_new': 'भेट बुक करा',
        'ma.phone_label': 'फोन नंबर टाका',
        'ma.phone_hint': 'तुमच्या भेटी पाहण्यासाठी तुमचा नोंदणीकृत फोन नंबर टाका',
        'ma.find_btn': 'भेटी शोधा',
        'ma.loading': 'तुमच्या भेटी लोड होत आहेत...',
        'ma.none_found': 'कोणत्याही भेटी आढळल्या नाहीत',
        'ma.none_hint': 'या क्लिनिकमध्ये अद्याप तुमची कोणतीही भेट नाही.',
        'ma.book_now': 'आता बुक करा',
        'ma.upcoming': 'आगामी भेटी',
        'ma.no_upcoming': 'कोणत्याही आगामी भेटी नाहीत',
        'ma.past': 'मागील भेटी',
        'ma.no_past': 'कोणत्याही मागील भेटी नाहीत',
        'ma.booked_on': 'बुकिंग तारीख:',

        // ==================== CHECK-IN (ci.*) ====================
        'ci.title': 'भेट चेक-इन',
        'ci.subtitle': 'तुमची पूर्व-भेट माहिती पूर्ण करा',
        'ci.your_appointment': 'तुमची भेट',
        'ci.already_checked': 'तुम्ही आधीच चेक-इन केले आहे!',
        'ci.wait_area': 'कृपया प्रतीक्षा क्षेत्रात बसा. डॉक्टर तयार होतील तेव्हा तुम्हाला बोलावले जाईल.',
        'ci.pre_visit': 'पूर्व-भेट प्रश्न',
        'ci.pre_visit_hint': 'काही प्रश्नांची उत्तरे देऊन आम्हाला तुमच्या भेटीसाठी तयार होण्यास मदत करा',
        'ci.chief_complaint': 'आज तुम्ही येथे का आलात?',
        'ci.symptoms_label': 'तुम्हाला यापैकी कोणती लक्षणे जाणवत आहेत का?',
        'ci.symptoms_hint': 'लागू असतील ते सर्व निवडा',
        'ci.vitals_label': 'जीवन चिन्हे (जर माहीत असतील तर)',
        'ci.vitals_hint': 'पर्यायी - डॉक्टरांना तयारी करण्यास मदत करते',
        'ci.temp': 'तापमान (°F)',
        'ci.bp': 'रक्तदाब',
        'ci.hr': 'हृदय गती (bpm)',
        'ci.duration_label': 'ही लक्षणे किती काळापासून आहेत?',
        'ci.dur_today': 'आज सुरू झाले',
        'ci.dur_1_3': '1-3 दिवस',
        'ci.dur_4_7': '4-7 दिवस',
        'ci.dur_1_2w': '1-2 आठवडे',
        'ci.dur_2plus': '2 आठवड्यांपेक्षा जास्त',
        'ci.dur_chronic': 'चालू / जुनाट',
        'ci.complete_btn': 'चेक-इन पूर्ण करा',
        'ci.quick_btn': 'त्वरित चेक-इन (प्रश्न वगळा)',
        'ci.checked_in': 'तुमचा चेक-इन झाला!',
        'ci.notified': 'डॉक्टरांना सूचित करण्यात आले आहे आणि ते लवकरच तुम्हाला भेटतील.',
        'ci.wait_note': 'कृपया प्रतीक्षा क्षेत्रात बसा. तुमचा नंबर आल्यावर आम्ही तुम्हाला बोलावू.',
        'ci.priority_label': 'प्राधान्य:',

        // ==================== TRIAGE RESULT (res.*) ====================
        'res.loading': 'तुमचा ट्रायएज निकाल लोड होत आहे...',
        'res.patient_info': 'रुग्णाची माहिती',
        'res.token': 'टोकन क्रमांक:',
        'res.status_label': 'स्थिती:',
        'res.complaint': 'तक्रार',
        'res.registered': 'नोंदणी:',
        'res.red_flags': 'लाल धोक्याचे इशारे आढळले',
        'res.assessment': 'मूल्यांकनाची कारणे',
        'res.what_to_do': 'तुम्हाला काय करायचे आहे?',
        'res.walk_in_now': 'आत्ता या',
        'res.walk_in_desc': 'रांगेत सामील व्हा आणि तुमच्या वेळाची प्रतीक्षा करा',
        'res.go_waiting': 'प्रतीक्षा कक्षात जा',
        'res.book_appt': 'भेट बुक करा',
        'res.book_desc': 'नंतरसाठी वेळ स्लॉट निवडा',
        'res.select_slot': 'वेळ स्लॉट निवडा',
        'res.emergency_msg': 'तात्काळ लक्ष आवश्यक आहे',
        'res.red_msg': 'कृपया ट्रायएज डेस्ककडे त्वरित जा',
        'res.amber_msg': 'तुम्हाला लवकरच पाहिले जाईल',
        'res.green_msg': 'बोलावण्याची प्रतीक्षा करा'
    }
};

// Language order for cycling
const languageOrder = ['en', 'hi', 'mr'];
const languageNames = {
    'en': 'English',
    'hi': 'हिंदी',
    'mr': 'मराठी'
};

// Translation Manager
const TranslationManager = {
    currentLang: 'en',
    
    init() {
        // Load saved language preference
        const savedLang = localStorage.getItem('swasthai_lang') || 'en';
        this.setLanguage(savedLang, false);
        
        // Setup language toggle buttons
        document.querySelectorAll('[data-lang-toggle]').forEach(btn => {
            btn.addEventListener('click', () => this.cycleLanguage());
        });
    },
    
    setLanguage(lang, save = true) {
        if (!translations[lang]) {
            lang = 'en';
        }
        this.currentLang = lang;
        if (save) {
            localStorage.setItem('swasthai_lang', lang);
        }
        this.updatePage();
        document.documentElement.lang = lang;
    },
    
    cycleLanguage() {
        const currentIndex = languageOrder.indexOf(this.currentLang);
        const nextIndex = (currentIndex + 1) % languageOrder.length;
        this.setLanguage(languageOrder[nextIndex]);
    },
    
    getNextLanguage() {
        const currentIndex = languageOrder.indexOf(this.currentLang);
        const nextIndex = (currentIndex + 1) % languageOrder.length;
        return languageNames[languageOrder[nextIndex]];
    },
    
    getCurrentLanguageName() {
        return languageNames[this.currentLang];
    },
    
    get(key) {
        return translations[this.currentLang]?.[key] || translations['en']?.[key] || key;
    },
    
    updatePage() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.get(key);
            el.textContent = translation;
        });
        
        // Update elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.get(key);
        });
        
        // Update elements with data-i18n-title
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = this.get(key);
        });
        
        // Update language toggle button - show next language
        document.querySelectorAll('[data-lang-toggle]').forEach(btn => {
            btn.textContent = this.getNextLanguage();
        });
        
        // Dispatch event for dynamic content
        document.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { language: this.currentLang } 
        }));
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    TranslationManager.init();
});

// Export for use in other scripts
window.TranslationManager = TranslationManager;
window.t = (key) => TranslationManager.get(key);
window.currentLang = () => TranslationManager.currentLang;
