"""
SwasthAI Outbound Growth & Clinic Outreach Engine Rebuilder
===========================================================
Rebuilds the entire outreach system strictly following:
1. Authoritative Healthcare Trends (ABDM 25Cr, NABH, BMJ/AIIMS OPD studies, etc.)
2. 10 Campaign Concepts with Scoring & Top 5 Selection
3. 5 Distinct Campaign Angles / Templates (Zero-Dash Standard)
4. Comprehensive Verified Clinic Database (~100 Clinics with strict verification)
5. Strict Verification & Quality Gates
6. Brevo Transactional Email Engine
7. Sends ONE Test Email to swasthai.founder@gmail.com and STOPS
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_DIR = os.path.join(BASE_DIR, 'website')
ENV_FILE = os.path.join(WEBSITE_DIR, '.env.local')
SEND_LOG_FILE = os.path.join(WEBSITE_DIR, 'cold-email-send-log.json')
OPT_OUT_FILE = os.path.join(WEBSITE_DIR, 'cold-email-opt-outs.json')

# -------------------------------------------------------------
# 1. BREVO CONFIGURATION
# -------------------------------------------------------------
def get_brevo_config():
    brevo_api_key = None
    brevo_sender_email = "swasthai.founder@gmail.com"
    brevo_sender_name = "Sankalp Mishra"
    
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('BREVO_API_KEY='):
                    brevo_api_key = line.split('=', 1)[1].strip()
                elif line.startswith('BREVO_SENDER_EMAIL='):
                    brevo_sender_email = line.split('=', 1)[1].strip()
                elif line.startswith('BREVO_SENDER_NAME='):
                    brevo_sender_name = line.split('=', 1)[1].strip().strip('"')
                    
    if not brevo_api_key:
        raise ValueError("BREVO_API_KEY is not configured in website/.env.local")
        
    return brevo_api_key, brevo_sender_email, brevo_sender_name


# -------------------------------------------------------------
# 2. ZERO-DASH VALIDATION HELPER
# -------------------------------------------------------------
def validate_zero_dash(text):
    """
    Checks that the text contains NO hyphen (-), NO en-dash (–), NO em-dash (—).
    URLs like https://swasthai-three.vercel.app/ are excluded from the sentence dash check.
    """
    lines = text.split('\n')
    for line in lines:
        clean_line = line
        # Strip URL before checking dashes
        if 'https://' in clean_line or 'http://' in clean_line:
            clean_line = re.sub(r'https?://\S+', '', clean_line)
        if '-' in clean_line or '–' in clean_line or '—' in clean_line:
            return False, f"Found dash in line: {line.strip()}"
    return True, "Valid"

def validate_no_placeholders(text):
    if re.search(r'\{\{.*?\}\}', text):
        return False, "Unfilled placeholders found"
    return True, "Valid"


# -------------------------------------------------------------
# 3. 5 DISTINCT CAMPAIGN TEMPLATES (ZERO DASH STANDARD)
# -------------------------------------------------------------
CAMPAIGN_TEMPLATES = {
    "campaign_1_queue_after_registration": {
        "name": "The queue starts after registration",
        "description": "Targets polyclinics and digitally active clinics with high footfall looking beyond basic counter registration.",
        "subjects": [
            "The queue starts after registration",
            "What happens after registration?",
            "OPD queue flow at {clinicName}",
            "Beyond digital registration",
            "Post registration waiting times"
        ],
        "cta": "Can I send you the 2 minute version?",
        "render": lambda doc, clinic, obs: f"""Dr. {doc},

India has now crossed 25 crore digital OPD registrations through ABDM's Scan and Register service.

That made me think about a slightly different problem.

If registration takes only a few minutes but patients still spend a long time waiting to see the doctor, the bottleneck has simply moved.

At {clinicName}, I noticed {obs}.

It made me wonder how your team handles one particular situation: when a new patient arrives with a complaint that may deserve attention before patients who are already waiting.

That is the small problem I am building SwasthAI around.

Patients answer a few structured questions after scanning a QR code. SwasthAI creates a recommended priority order for the doctor to review, and the doctor can change it whenever needed.

I am looking for a few clinics to try this with a real OPD workflow.

Can I send you the 2 minute version?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""
    },

    "campaign_2_who_goes_first": {
        "name": "Who goes first?",
        "description": "Targets high walk in clinics (Orthopedics, Pediatrics, Trauma, ENT) dealing with urgent cases.",
        "subjects": [
            "Who goes first?",
            "Handling acute walk ins at {clinicName}",
            "Prioritizing patients in busy OPD sessions",
            "Walk ins versus scheduled appointments",
            "Queue order during peak hours"
        ],
        "cta": "Would you be open to seeing a 2 minute walkthrough?",
        "render": lambda doc, clinic, obs: f"""Dr. {doc},

When five patients are already waiting in the clinic, what happens when a new walk in arrives with severe discomfort?

In most outpatient settings, reception staff either rely strictly on arrival time or make an informal guess about who needs to go in first.

At {clinicName}, I noticed {obs}.

That made me think about how your team balances fairness to waiting patients with the clinical urgency of acute arrivals.

I am building SwasthAI to help doctors organize this intake.

Patients scan a QR code on arrival and answer a few short, structured questions. SwasthAI provides a recommended priority order for your review, and you can change the sequence whenever you want.

We are testing this with a small group of outpatient practices.

Would you be open to seeing a 2 minute walkthrough?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""
    },

    "campaign_3_next_opd_bottleneck": {
        "name": "The next OPD bottleneck",
        "description": "Targets multi doctor clinics and established polyclinics experiencing waiting room pacing friction.",
        "subjects": [
            "The next OPD bottleneck",
            "Managing clinic patient flow",
            "When the waiting room fills up",
            "Consultation pacing at {clinicName}",
            "OPD operations beyond scheduling"
        ],
        "cta": "Can I share a 2 minute overview?",
        "render": lambda doc, clinic, obs: f"""Dr. {doc},

Many clinics have successfully streamlined appointment scheduling, but the waiting room often remains crowded.

When multiple consultations run simultaneously, patient flow inside the clinic quickly becomes the next operational bottleneck.

At {clinicName}, I noticed {obs}.

It made me curious how your practice manages queue flow when some consultations take fifteen minutes while other patients only need a brief review.

That is why I am building SwasthAI.

Arriving patients scan a QR code and answer structured intake questions. SwasthAI presents a recommended priority order on your screen, allowing you to review and adjust the sequence at any time.

I am currently working with a few clinics to refine this workflow.

Can I share a 2 minute overview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""
    },

    "campaign_4_receptionist_decision": {
        "name": "The receptionist's decision",
        "description": "Targets small independent clinics and single doctor practices where front desk staff carry informal triage stress.",
        "subjects": [
            "The receptionist's decision",
            "Front desk triage at {clinicName}",
            "Helping reception manage the queue",
            "When patients ask who is next",
            "Objective queue intake for clinics"
        ],
        "cta": "Would you be interested in a 2 minute preview?",
        "render": lambda doc, clinic, obs: f"""Dr. {doc},

In most private practices, the front desk is put in an uncomfortable position.

When a walk in looks uncomfortable, the receptionist has to decide whether to disrupt the queue without having clinical tools to evaluate the situation.

At {clinicName}, I noticed {obs}.

It made me wonder how your front desk currently determines which patients need faster doctor attention during busy hours.

I built SwasthAI to make this intake clear and structured.

Patients scan a counter QR code and answer a few simple questions. SwasthAI generates a recommended priority order on the doctor screen, while the doctor retains complete control over the final queue.

We are looking for a few practices to try this in daily OPD.

Would you be interested in a 2 minute preview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""
    },

    "campaign_5_digital_clinic_manual_queue": {
        "name": "Digital clinic, manual queue",
        "description": "Targets tech enabled clinics with digital records or online booking where physical waiting queues remain manual.",
        "subjects": [
            "Digital clinic, manual queue",
            "Modernizing the OPD waiting room",
            "Beyond token numbers at {clinicName}",
            "Clinical priority versus arrival time",
            "Organizing the physical queue"
        ],
        "cta": "Can I send you a 2 minute screen recording?",
        "render": lambda doc, clinic, obs: f"""Dr. {doc},

Most modern clinics now use digital billing and electronic appointments, but patient sequencing in the waiting room is still handled on a first come first served basis.

Clock arrival works for cinema seats, but healthcare visits often have varying levels of urgency.

At {clinicName}, I noticed {obs}.

It made me wonder how your team handles cases where an arriving patient might benefit from earlier review than someone who booked an earlier slot.

I am building SwasthAI to solve this specific gap.

Patients scan a QR code upon arrival and answer brief intake questions. SwasthAI provides a recommended queue order for the doctor to review, with full ability to override anytime.

I am looking for a few forward thinking clinics to test this in practice.

Can I send you a 2 minute screen recording?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""
    }
}

print("Loaded campaign templates.")
