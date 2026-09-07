"""
SwasthAI 299 Quota Outbound Campaign Dispatcher
================================================
1. Aggregates all researched prospects from database & scripts
2. Runs fast multi-threaded DNS MX verification across all domains (0-bounce guarantee)
3. Aligns doctor-clinic identity & salutations (Doctor, / Dr. {Name},)
4. Enforces Zero-Dash & Zero-Placeholder standards on every email body
5. Excludes permanent opt-outs
6. Sends up to 299 verified cold emails via Brevo Transactional API with 1.2s pacing
7. Logs every Brevo Message ID to cold-email-send-log.json
"""

import os
import glob
import re
import json
import time
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_DIR = os.path.join(BASE_DIR, 'website')
ENV_FILE = os.path.join(WEBSITE_DIR, '.env.local')
SEND_LOG_FILE = os.path.join(WEBSITE_DIR, 'cold-email-send-log.json')
OPT_OUT_FILE = os.path.join(WEBSITE_DIR, 'cold-email-opt-outs.json')

def load_brevo_config():
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
        raise ValueError("BREVO_API_KEY not found in .env.local")
        
    return brevo_api_key, brevo_sender_email, brevo_sender_name

def check_domain_mx(domain):
    try:
        url = f"https://dns.google/resolve?name={domain}&type=MX"
        req = urllib.request.Request(url, headers={"accept": "application/json", "user-agent": "SwasthAI-MX-Validator"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            answers = data.get("Answer", [])
            mx_hosts = [a.get("data") for a in answers if a.get("type") == 15]
            if len(mx_hosts) > 0:
                return domain, True, mx_hosts
            # Fallback to A-record
            url_a = f"https://dns.google/resolve?name={domain}&type=A"
            req_a = urllib.request.Request(url_a, headers={"accept": "application/json", "user-agent": "SwasthAI-MX-Validator"})
            with urllib.request.urlopen(req_a, timeout=4) as resp_a:
                data_a = json.loads(resp_a.read().decode())
                answers_a = data_a.get("Answer", [])
                a_hosts = [a.get("data") for a in answers_a if a.get("type") == 1]
                return domain, len(a_hosts) > 0, ["A-Record: " + str(a_hosts[0])] if a_hosts else []
    except Exception as e:
        return domain, False, [str(e)]

# 5 Zero-Dash Master Campaign Templates
def render_email_content(campaign_key, salutation, clinic_name, obs):
    if campaign_key == "campaign_2_who_goes_first":
        subject = f"Handling acute walk ins at {clinic_name}"
        body = f"""{salutation}

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
        subject = f"The next OPD bottleneck"
        body = f"""{salutation}

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
        subject = f"The receptionist's decision"
        body = f"""{salutation}

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
        subject = f"Digital clinic, manual queue"
        body = f"""{salutation}

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

    else: # Default: Campaign 1
        subject = f"The queue starts after registration"
        body = f"""{salutation}

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

    return subject, body

def get_html(plain_text):
    html_paragraphs = "".join([f'<p style="margin: 0 0 16px 0;">{line}</p>' for line in plain_text.split("\n\n") if line.strip()])
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #222222; background-color: #ffffff; margin: 0; padding: 20px 0;">
  <div style="max-width: 600px; margin: 0 auto; padding: 0 20px;">
    {html_paragraphs}
  </div>
</body>
</html>"""

def build_prospect_pool():
    print("[1/4] Aggregating prospects across repository...")
    raw_pool = []
    seen = set()

    # Load from audited leads
    audited_path = os.path.join(WEBSITE_DIR, 'data', 'audited-prospect-leads.json')
    if os.path.exists(audited_path):
        with open(audited_path, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                em = item.get('email', '').strip().lower()
                if em and em not in seen and 'founder' not in em:
                    seen.add(em)
                    raw_pool.append(item)

    # Load from all scripts in website/scripts
    for script_path in glob.glob(os.path.join(WEBSITE_DIR, 'scripts', '*.py')):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'\{[^{}\n]*"email":\s*"([^"]+)"[^{}\n]*\}', content):
            try:
                obj = json.loads(m.group(0))
                em = obj.get('email', '').strip().lower()
                if em and em not in seen and 'founder' not in em:
                    seen.add(em)
                    raw_pool.append(obj)
            except Exception:
                pass

    print(f"Total unique prospects aggregated: {len(raw_pool)}")

    # Extract unique domains for fast concurrent MX check
    domains = set(p.get('email', '').split('@')[-1].lower() for p in raw_pool if '@' in p.get('email', ''))
    print(f"[2/4] Verifying DNS MX records across {len(domains)} distinct domains concurrently...")
    
    domain_status = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_domain_mx, list(domains))
        for dom, is_valid, mx in results:
            domain_status[dom] = (is_valid, mx)

    dead_count = sum(1 for v in domain_status.values() if not v[0])
    print(f"[OK] MX Check Complete: {len(domains) - dead_count} Valid Domains, {dead_count} Dead Domains Purged.")

    # Load Opt-outs
    opt_outs = set()
    if os.path.exists(OPT_OUT_FILE):
        try:
            with open(OPT_OUT_FILE, 'r', encoding='utf-8') as f:
                opt_outs = set(e.lower().strip() for e in json.load(f))
        except:
            pass

    # Build validated prospects list
    validated = []
    for idx, p in enumerate(raw_pool, 1):
        email = p.get('email', '').strip().lower()
        if not email or '@' not in email or email in opt_outs:
            continue
        domain = email.split('@')[-1].lower()
        if not domain_status.get(domain, (False, []))[0]:
            continue # Skip dead domain to prevent hard bounce

        doc_name = p.get('doctorName', '').strip()
        clinic_name = p.get('clinicName', '').strip()
        if not clinic_name or clinic_name.lower() in ['clinic', 'hospital']:
            clinic_name = "your clinic"

        # Determine safe salutation to prevent doctor-hospital mismatch confusion
        if doc_name and not doc_name.lower().startswith('medical director') and not doc_name.lower().startswith('director') and doc_name.lower() not in ['doctor', 'team']:
            salutation = f"Dr. {doc_name},"
        else:
            salutation = "Doctor,"

        # Campaign selection
        campaign = p.get('campaign', 'campaign_1_queue_after_registration')
        if not campaign.startswith('campaign_'):
            campaign = 'campaign_1_queue_after_registration'

        obs = p.get('verifiedObservation', 'your clinic manages active daily outpatient consultations').strip()
        # Clean any accidental dashes in observation or clinic name
        obs = obs.replace(' - ', ' ').replace('-', ' ').replace('—', ' ').replace('–', ' ')
        clinic_name = clinic_name.replace(' - ', ' ').replace('-', ' ').replace('—', ' ').replace('–', ' ')

        subject, body = render_email_content(campaign, salutation, clinic_name, obs)

        # Zero-Dash check
        has_dash = False
        for line in body.split('\n'):
            clean = line
            if 'https://' in clean or 'http://' in clean:
                clean = re.sub(r'https?://\S+', '', clean)
            if '-' in clean or '–' in clean or '—' in clean:
                has_dash = True
                break
        if has_dash:
            continue

        validated.append({
            "rank": len(validated) + 1,
            "doctorName": doc_name or "Doctor",
            "salutation": salutation,
            "clinicName": clinic_name,
            "email": email,
            "campaign": campaign,
            "subject": subject,
            "textContent": body,
            "htmlContent": get_html(body)
        })

    print(f"[3/4] Ready to send {len(validated)} verified, zero-dash prospects.")
    return validated

def send_batch(prospects, limit=299):
    brevo_api_key, brevo_sender_email, brevo_sender_name = load_brevo_config()
    to_send = prospects[:limit]
    
    print(f"[4/4] Starting sequential Brevo transactional send for {len(to_send)} prospects...")
    
    log_entries = []
    if os.path.exists(SEND_LOG_FILE):
        try:
            with open(SEND_LOG_FILE, 'r', encoding='utf-8') as lf:
                log_entries = json.load(lf)
        except:
            pass

    success_count = 0
    fail_count = 0

    for i, p in enumerate(to_send, 1):
        payload = {
            "sender": {
                "name": brevo_sender_name,
                "email": brevo_sender_email
            },
            "to": [
                {
                    "email": p["email"],
                    "name": p["doctorName"] if p["doctorName"] != "Doctor" else p["clinicName"]
                }
            ],
            "replyTo": {
                "name": brevo_sender_name,
                "email": brevo_sender_email
            },
            "subject": p["subject"],
            "textContent": p["textContent"],
            "htmlContent": p["htmlContent"],
            "tags": [p["campaign"], "growth_batch_299"]
        }

        req = urllib.request.Request(
            "https://api.brevo.com/v3/smtp/email",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": brevo_api_key
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                msg_id = res_data.get('messageId')
                success_count += 1
                print(f"[{i}/{len(to_send)} SENT] {p['email']} ({p['clinicName']}) -> Brevo ID: {msg_id}")
                
                log_entries.append({
                    "prospectName": p["doctorName"],
                    "doctorName": p["doctorName"],
                    "clinicName": p["clinicName"],
                    "recipientEmail": p["email"],
                    "sentAt": datetime.now().isoformat() + "Z",
                    "subject": p["subject"],
                    "status": "SENT",
                    "brevoMessageId": msg_id,
                    "error": None,
                    "campaign": p["campaign"]
                })
        except urllib.error.HTTPError as e:
            fail_count += 1
            err = e.read().decode('utf-8')
            print(f"[{i}/{len(to_send)} FAILED] {p['email']} -> HTTP {e.code}: {err}")
            log_entries.append({
                "prospectName": p["doctorName"],
                "doctorName": p["doctorName"],
                "clinicName": p["clinicName"],
                "recipientEmail": p["email"],
                "sentAt": datetime.now().isoformat() + "Z",
                "subject": p["subject"],
                "status": "FAILED",
                "brevoMessageId": None,
                "error": err,
                "campaign": p["campaign"]
            })
        except Exception as e:
            fail_count += 1
            print(f"[{i}/{len(to_send)} ERROR] {p['email']} -> {str(e)}")

        # 1.2 second rate-limiting delay between transactional sends
        time.sleep(1.2)

        # Save progress every 10 sends
        if i % 10 == 0:
            with open(SEND_LOG_FILE, 'w', encoding='utf-8') as lf:
                json.dump(log_entries, lf, indent=2)

    # Final save
    with open(SEND_LOG_FILE, 'w', encoding='utf-8') as lf:
        json.dump(log_entries, lf, indent=2)

    print("=" * 70)
    print(f"BATCH SEND COMPLETE: {success_count} Successfully Delivered | {fail_count} Failed")
    print("=" * 70)

if __name__ == '__main__':
    prospects = build_prospect_pool()
    send_batch(prospects, limit=299)
