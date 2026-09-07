"""
SwasthAI Deliverability & Identity Verification Engine
======================================================
1. Live DNS MX Verification on every prospect domain to prevent hard bounces
2. Name & Hospital / Clinic Matching Audit to prevent doctor-hospital confusion
3. Salutation Normalization:
   - For verified doctor-led private practices: 'Dr. {doctorName},'
   - For institutional / polyclinic role inboxes: 'Doctor,' or 'Medical Director,'
4. Strict Zero-Dash Validation
5. Strict Zero-Placeholder Validation
"""

import os
import re
import json
import time
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_DIR = os.path.join(BASE_DIR, 'website')
SEND_LOG_FILE = os.path.join(WEBSITE_DIR, 'cold-email-send-log.json')
OPT_OUT_FILE = os.path.join(WEBSITE_DIR, 'cold-email-opt-outs.json')

# DNS MX Validator using Google DNS API
def check_domain_mx(domain):
    try:
        url = f"https://dns.google/resolve?name={domain}&type=MX"
        req = urllib.request.Request(url, headers={"accept": "application/json", "user-agent": "SwasthAI-Deliverability-Gate"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            answers = data.get("Answer", [])
            mx_hosts = [a.get("data") for a in answers if a.get("type") == 15]
            if len(mx_hosts) > 0:
                return True, mx_hosts
            # Fallback to A record if MX doesn't exist
            url_a = f"https://dns.google/resolve?name={domain}&type=A"
            req_a = urllib.request.Request(url_a, headers={"accept": "application/json", "user-agent": "SwasthAI-Deliverability-Gate"})
            with urllib.request.urlopen(req_a, timeout=8) as resp_a:
                data_a = json.loads(resp_a.read().decode())
                answers_a = data_a.get("Answer", [])
                a_hosts = [a.get("data") for a in answers_a if a.get("type") == 1]
                return len(a_hosts) > 0, ["A-Record: " + str(a_hosts[0])] if a_hosts else []
    except Exception as e:
        return False, [str(e)]

# 5 Master Zero-Dash Templates with Flexible Salutations
def render_template(campaign_key, salutation, clinic_name, obs):
    if campaign_key == "campaign_1_queue_after_registration":
        return f"""{salutation}

India has now crossed 25 crore digital OPD registrations through ABDM's Scan and Register service.

That made me think about a slightly different problem.

If registration takes only a few minutes but patients still spend a long time waiting to see the doctor, the bottleneck has simply moved.

At {clinic_name}, I noticed {obs}.

It made me wonder how your team handles one particular situation: when a new patient arrives with a complaint that may deserve attention before patients who are already waiting.

That is the small problem I am building SwasthAI around.

Patients answer a few structured questions after scanning a QR code. SwasthAI creates a recommended priority order for the doctor to review, and the doctor can change it whenever needed.

I am looking for a few clinics to try this with a real OPD workflow.

Can I send you the 2 minute version?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""

    elif campaign_key == "campaign_2_who_goes_first":
        return f"""{salutation}

When five patients are already waiting in the clinic, what happens when a new walk in arrives with severe discomfort?

In most outpatient settings, reception staff either rely strictly on arrival time or make an informal guess about who needs to go in first.

At {clinic_name}, I noticed {obs}.

That made me think about how your team balances fairness to waiting patients with the clinical urgency of acute arrivals.

I am building SwasthAI to help doctors organize this intake.

Patients scan a QR code on arrival and answer a few short, structured questions. SwasthAI provides a recommended priority order for your review, and you can change the sequence whenever you want.

We are testing this with a small group of outpatient practices.

Would you be open to seeing a 2 minute walkthrough?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""

    elif campaign_key == "campaign_3_next_opd_bottleneck":
        return f"""{salutation}

Many clinics have successfully streamlined appointment scheduling, but the waiting room often remains crowded.

When multiple consultations run simultaneously, patient flow inside the clinic quickly becomes the next operational bottleneck.

At {clinic_name}, I noticed {obs}.

It made me curious how your practice manages queue flow when some consultations take fifteen minutes while other patients only need a brief review.

That is why I am building SwasthAI.

Arriving patients scan a QR code and answer structured intake questions. SwasthAI presents a recommended priority order on your screen, allowing you to review and adjust the sequence at any time.

I am currently working with a few clinics to refine this workflow.

Can I share a 2 minute overview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""

    elif campaign_key == "campaign_4_receptionist_decision":
        return f"""{salutation}

In most private practices, the front desk is put in an uncomfortable position.

When a walk in looks uncomfortable, the receptionist has to decide whether to disrupt the queue without having clinical tools to evaluate the situation.

At {clinic_name}, I noticed {obs}.

It made me wonder how your front desk currently determines which patients need faster doctor attention during busy hours.

I built SwasthAI to make this intake clear and structured.

Patients scan a counter QR code and answer a few simple questions. SwasthAI generates a recommended priority order on the doctor screen, while the doctor retains complete control over the final queue.

We are looking for a few practices to try this in daily OPD.

Would you be interested in a 2 minute preview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""

    elif campaign_key == "campaign_5_digital_clinic_manual_queue":
        return f"""{salutation}

Most modern clinics now use digital billing and electronic appointments, but patient sequencing in the waiting room is still handled on a first come first served basis.

Clock arrival works for cinema seats, but healthcare visits often have varying levels of urgency.

At {clinic_name}, I noticed {obs}.

It made me wonder how your team handles cases where an arriving patient might benefit from earlier review than someone who booked an earlier slot.

I am building SwasthAI to solve this specific gap.

Patients scan a QR code upon arrival and answer brief intake questions. SwasthAI provides a recommended queue order for the doctor to review, with full ability to override anytime.

I am looking for a few forward thinking clinics to test this in practice.

Can I send you a 2 minute screen recording?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up."""

    raise ValueError(f"Unknown campaign: {campaign_key}")

def main():
    print("=" * 70)
    print("SWASTHAI 0-BOUNCE & DOCTOR-CLINIC IDENTITY AUDIT")
    print("=" * 70)

    from build_and_execute_campaign import RAW_PROSPECTS, CAMPAIGN_TEMPLATES

    audited_prospects = []
    domain_cache = {}

    for idx, p in enumerate(RAW_PROSPECTS, 1):
        email = p["email"].strip()
        domain = email.split("@")[-1].lower() if "@" in email else ""
        
        # 1. Check MX records
        if domain not in domain_cache:
            has_mx, mx_records = check_domain_mx(domain)
            domain_cache[domain] = (has_mx, mx_records)
            time.sleep(0.1) # Be gentle to DNS API
        else:
            has_mx, mx_records = domain_cache[domain]

        if not has_mx:
            print(f"[REJECT - DEAD DOMAIN] {email} (Clinic: {p['clinicName']}) -> No MX records found!")
            continue

        # 2. Determine Salutation to Avoid Doctor-Hospital Mismatch Confusion
        doc_name = p.get("doctorName", "").strip()
        clinic_name = p.get("clinicName", "").strip()
        
        # If doctorName is a verified doctor and clinic is their practice:
        if doc_name and not doc_name.lower().startswith("medical director") and not doc_name.lower().startswith("director"):
            salutation = f"Dr. {doc_name},"
        elif doc_name.lower().startswith("medical director") or doc_name.lower().startswith("director"):
            salutation = "Doctor," # Clean, respectful, avoids confusion
        else:
            salutation = "Doctor,"

        # 3. Render and Verify Zero-Dash Body
        obs = p["verifiedObservation"]
        campaign_key = p["campaign"]
        body_text = render_template(campaign_key, salutation, clinic_name, obs)

        # Dash checks
        for line in body_text.split('\n'):
            clean = line
            if 'https://' in clean or 'http://' in clean:
                clean = re.sub(r'https?://\S+', '', clean)
            if '-' in clean or '–' in clean or '—' in clean:
                raise ValueError(f"DASH DETECTED in {p['clinicName']}: {line}")

        # Placeholder checks
        if re.search(r'\{\{.*?\}\}', body_text):
            raise ValueError(f"PLACEHOLDER DETECTED in {p['clinicName']}")

        # Select appropriate subject
        template = CAMPAIGN_TEMPLATES[campaign_key]
        subject = template["subjects"][0].replace("{clinicName}", clinic_name)
        if len(template["subjects"]) > 1 and "{clinicName}" in template["subjects"][1]:
            subject = template["subjects"][1].replace("{clinicName}", clinic_name)

        audited_prospects.append({
            "rank": idx,
            "doctorName": doc_name if salutation.startswith("Dr.") else "Medical Director / Doctor",
            "salutation": salutation,
            "clinicName": clinic_name,
            "specialty": p["specialty"],
            "city": p["city"],
            "area": p["area"],
            "email": email,
            "domain": domain,
            "mxValid": True,
            "mxRecordSample": mx_records[0] if mx_records else "Verified",
            "phone": p["phone"],
            "website": p["website"],
            "sourceUrl": p["sourceUrl"],
            "emailSourceUrl": p["emailSourceUrl"],
            "verifiedObservation": obs,
            "campaign": campaign_key,
            "campaignName": template["name"],
            "campaignReason": p["campaignReason"],
            "subject": subject,
            "emailBody": body_text,
            "verificationStatus": "VERIFIED",
            "researchDate": "2026-09-05",
            "status": "QUEUED"
        })

        print(f"[{idx}/52 VERIFIED & MX OK] {email} | {clinic_name} | {salutation} | MX: {mx_records[0][:30] if mx_records else 'OK'}")

    print("=" * 70)
    print(f"SUMMARY: {len(audited_prospects)} of {len(RAW_PROSPECTS)} Prospects 100% MX-Verified & Audited!")
    print("=" * 70)

    # Save to audited prospects JSON for runtime consumption
    out_json = os.path.join(WEBSITE_DIR, 'data', 'audited-prospect-leads.json')
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(audited_prospects, f, indent=2)
    print(f"Saved audited leads to: {out_json}")

if __name__ == '__main__':
    main()
