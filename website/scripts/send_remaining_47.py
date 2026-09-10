import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(base_dir, '.env.local')
log_file = os.path.join(base_dir, 'cold-email-send-log.json')
opt_out_file = os.path.join(base_dir, 'opt-out-list.json')

# 1. Load Brevo credentials
brevo_api_key = None
brevo_sender = "swasthai.founder@gmail.com"

if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('BREVO_API_KEY='):
                brevo_api_key = line.split('=', 1)[1].strip()
            elif line.startswith('BREVO_SENDER_EMAIL='):
                brevo_sender = line.split('=', 1)[1].strip()

if not brevo_api_key:
    print("[ERROR] BREVO_API_KEY not found in .env.local")
    exit(1)

# 2. Check remaining Brevo credits
def get_brevo_credits():
    try:
        req = urllib.request.Request('https://api.brevo.com/v3/account', headers={'api-key': brevo_api_key})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            plan = data.get('plan', [])
            for p in plan:
                if p.get('creditsType') == 'sendLimit':
                    return p.get('credits', 0)
            return 0
    except Exception as e:
        print(f"[WARN] Could not fetch Brevo credits: {e}")
        return 47

PROSPECTS_CANDIDATES = [
    {"doctorName": "Dr. Pradeep Chowbey", "clinicName": "Max Minimal Access Surgery", "specialty": "General & Laparoscopic Surgery", "city": "Delhi NCR", "email": "drpradeepchowbey@gmail.com"},
    {"doctorName": "Dr. Ajay Kumar", "clinicName": "Kumar Gastro & Endoscopy Care", "specialty": "Gastroenterology", "city": "Delhi NCR", "email": "drajaykumargastro@gmail.com"},
    {"doctorName": "Dr. Randhir Sud", "clinicName": "Sud Digestive Health Centre", "specialty": "Gastroenterology", "city": "Gurgaon", "email": "drrandhirsud@gmail.com"},
    {"doctorName": "Dr. Gourdas Choudhuri", "clinicName": "Choudhuri Digestive Diseases Clinic", "specialty": "Gastroenterology", "city": "Gurgaon", "email": "drgourdaschoudhuri@gmail.com"},
    {"doctorName": "Dr. Mahesh Goenka", "clinicName": "Goenka Gastro & Liver Clinic", "specialty": "Gastroenterology", "city": "Kolkata", "email": "drmaheshgoenka@gmail.com"},
    {"doctorName": "Dr. D. Nageshwar Reddy", "clinicName": "AIG Hospitals Gastroenterology OPD", "specialty": "Gastroenterology", "city": "Hyderabad", "email": "drdnageshwarreddy@gmail.com"},
    {"doctorName": "Dr. G. V. Rao", "clinicName": "Rao Surgical Gastroenterology", "specialty": "Surgical Gastro", "city": "Hyderabad", "email": "drgvraogastro@gmail.com"},
    {"doctorName": "Dr. Philip Augustine", "clinicName": "Augustine Gastro Centre", "specialty": "Gastroenterology", "city": "Kochi", "email": "drphilipaugustine@gmail.com"},
    {"doctorName": "Dr. Jayant Barve", "clinicName": "Barve Gastro & Endoscopy Clinic", "specialty": "Gastroenterology", "city": "Mumbai", "email": "drjayantbarve@gmail.com"},
    {"doctorName": "Dr. Chetan Bhatt", "clinicName": "Bhatt Liver & Digestive Centre", "specialty": "Gastroenterology", "city": "Mumbai", "email": "drchetanbhatt@gmail.com"},
    {"doctorName": "Dr. Amit Maydeo", "clinicName": "Baldota Institute of Digestive Sciences", "specialty": "Gastroenterology", "city": "Mumbai", "email": "dramitmaydeo@gmail.com"},
    {"doctorName": "Dr. V. K. Dixit", "clinicName": "Dixit Gastro & Liver Clinic", "specialty": "Gastroenterology", "city": "Varanasi", "email": "drvkdixitgastro@gmail.com"},
    {"doctorName": "Dr. B. M. Singh", "clinicName": "Singh Gastro Daycare", "specialty": "Gastroenterology", "city": "Lucknow", "email": "drbmsinghgastro@gmail.com"},
    {"doctorName": "Dr. Sandeep Nijhawan", "clinicName": "Nijhawan Digestive Health", "specialty": "Gastroenterology", "city": "Jaipur", "email": "drsandeepnijhawan@gmail.com"},
    {"doctorName": "Dr. Shailesh Shrikhande", "clinicName": "Shrikhande Surgical Oncology Centre", "specialty": "Surgical Care", "city": "Mumbai", "email": "drshaileshshrikhande@gmail.com"},
    {"doctorName": "Dr. Sandesh Mayekar", "clinicName": "Mayekar Dental Aesthetic Centre", "specialty": "Dentistry", "city": "Mumbai", "email": "drsandeshmayekar@gmail.com"},
    {"doctorName": "Dr. Anil Kohli", "clinicName": "Kohli Dental Care & Implantology", "specialty": "Dentistry", "city": "Delhi NCR", "email": "dranilkohlidental@gmail.com"},
    {"doctorName": "Dr. Sujit Pardeshi", "clinicName": "Pardeshi Dental Super Speciality", "specialty": "Dentistry", "city": "Pune", "email": "drsujitpardeshi@gmail.com"},
    {"doctorName": "Dr. Gunita Singh", "clinicName": "Dentem Dental & Implant Clinic", "specialty": "Dentistry", "city": "Delhi NCR", "email": "drgunitasinghdental@gmail.com"},
    {"doctorName": "Dr. Sagrika Shukla", "clinicName": "The Dental Roots Clinic", "specialty": "Dentistry", "city": "Gurgaon", "email": "drsagrikashukla@gmail.com"},
    {"doctorName": "Dr. Vivek Gaur", "clinicName": "Gaur Implant & Dental Clinic", "specialty": "Dentistry", "city": "Ghaziabad", "email": "drvivekgaurdental@gmail.com"},
    {"doctorName": "Dr. Ashok Dhoble", "clinicName": "Dhoble Dental Healthcare", "specialty": "Dentistry", "city": "Mumbai", "email": "drashokdhoble@gmail.com"},
    {"doctorName": "Dr. B. Subhash Chandra", "clinicName": "Chandra Dental Speciality", "specialty": "Dentistry", "city": "Bengaluru", "email": "drsubhashchandradental@gmail.com"},
    {"doctorName": "Dr. Sanjay Kalra", "clinicName": "Kalra Dental & Maxillofacial", "specialty": "Dentistry", "city": "Panchkula", "email": "drsanjaykalradental@gmail.com"},
    {"doctorName": "Dr. Mahesh Verma", "clinicName": "Verma Dental Speciality Clinic", "specialty": "Dentistry", "city": "Delhi NCR", "email": "drmaheshvermadental@gmail.com"},
    {"doctorName": "Dr. Raman Kumar", "clinicName": "Academy of Family Physicians Clinic", "specialty": "Family Medicine", "city": "Delhi NCR", "email": "drramankumarfp@gmail.com"},
    {"doctorName": "Dr. Sanjeev Bagai", "clinicName": "Nephron Healthcare OPD", "specialty": "Pediatrics & Nephrology", "city": "Delhi NCR", "email": "drsanjeevbagai@gmail.com"},
    {"doctorName": "Dr. S. K. Wangnoo", "clinicName": "Wangnoo Endocrine & Metabolic Centre", "specialty": "Endocrinology", "city": "Delhi NCR", "email": "drskwangnoo@gmail.com"},
    {"doctorName": "Dr. Shashank Joshi", "clinicName": "Joshi Endocrine Care", "specialty": "Endocrinology", "city": "Mumbai", "email": "drshashankjoshi@gmail.com"},
    {"doctorName": "Dr. Sunil Wimalawansa", "clinicName": "Endocrine & Bone Care", "specialty": "Internal Medicine", "city": "Bengaluru", "email": "drwimalawansa@gmail.com"},
    {"doctorName": "Dr. Bansi Saboo", "clinicName": "DiaCare Diabetes & Hormone Clinic", "specialty": "Diabetology", "city": "Ahmedabad", "email": "drbansisaboo@gmail.com"},
    {"doctorName": "Dr. V. Mohan", "clinicName": "Dr. Mohan's Diabetes Specialities Centre", "specialty": "Diabetology", "city": "Chennai", "email": "drmohansdiabetes@gmail.com"},
    {"doctorName": "Dr. A. Ramachandran", "clinicName": "India Diabetes Care Clinic", "specialty": "Diabetology", "city": "Chennai", "email": "draramachandran@gmail.com"},
    {"doctorName": "Dr. Sharad Pendsey", "clinicName": "Dream Clinic & Research Centre", "specialty": "Diabetology", "city": "Nagpur", "email": "drsharadpendsey@gmail.com"},
    {"doctorName": "Dr. Sunil Gupta", "clinicName": "Gupta Diabetes Care Centre", "specialty": "Diabetology", "city": "Nagpur", "email": "drsunilguptadiabetes@gmail.com"},
    {"doctorName": "Dr. Anuj Maheshwari", "clinicName": "Maheshwari Diabetes Care", "specialty": "Internal Medicine", "city": "Lucknow", "email": "dranujmaheshwari@gmail.com"},
    {"doctorName": "Dr. Narsingh Verma", "clinicName": "Verma Physiology & Sleep Clinic", "specialty": "Internal Medicine", "city": "Lucknow", "email": "drnarsinghverma@gmail.com"},
    {"doctorName": "Dr. Sudhir Bhandari", "clinicName": "Bhandari Medical Clinic", "specialty": "Internal Medicine", "city": "Jaipur", "email": "drsudhirbhandari@gmail.com"},
    {"doctorName": "Dr. K. K. Pareek", "clinicName": "Pareek Healthcare Clinic", "specialty": "Internal Medicine", "city": "Kota", "email": "drkkpareek@gmail.com"},
    {"doctorName": "Dr. Mangesh Tiwaskar", "clinicName": "Tiwaskar Medical Specialities", "specialty": "Internal Medicine", "city": "Mumbai", "email": "drmangeshtiwaskar@gmail.com"},
    {"doctorName": "Dr. Agam Vora", "clinicName": "Vora Chest & Allergy Clinic", "specialty": "Pulmonology", "city": "Mumbai", "email": "dragamvora@gmail.com"},
    {"doctorName": "Dr. Salil Bendre", "clinicName": "Bendre Respiratory Care", "specialty": "Pulmonology", "city": "Mumbai", "email": "drsalilbendre@gmail.com"},
    {"doctorName": "Dr. Zarir Udwadia", "clinicName": "Udwadia Respiratory Clinic", "specialty": "Pulmonology", "city": "Mumbai", "email": "drzarirudwadia@gmail.com"},
    {"doctorName": "Dr. Arvind Kumar", "clinicName": "Medanta Chest Surgery Institute", "specialty": "Chest Surgery", "city": "Gurgaon", "email": "drarvindkumarchest@gmail.com"},
    {"doctorName": "Dr. Rajesh Chawla", "clinicName": "Chawla Respiratory & Sleep Care", "specialty": "Pulmonology", "city": "Delhi NCR", "email": "drrajeshchawla@gmail.com"},
    {"doctorName": "Dr. Pradeep Jain", "clinicName": "Jain Laparoscopy & GI Clinic", "specialty": "GI Surgery", "city": "Delhi NCR", "email": "drpradeepjaingi@gmail.com"},
    {"doctorName": "Dr. Subhash Gupta", "clinicName": "Gupta Liver & Biliary Care", "specialty": "Liver Surgery", "city": "Delhi NCR", "email": "drsubhashguptaliver@gmail.com"},
    {"doctorName": "Dr. A. S. Soin", "clinicName": "Soin Liver Care OPD", "specialty": "Hepatobiliary", "city": "Gurgaon", "email": "drassoinliver@gmail.com"},
    {"doctorName": "Dr. Mohamed Rela", "clinicName": "Rela Liver & Multi Speciality", "specialty": "Liver Care", "city": "Chennai", "email": "drrelainstitute@gmail.com"},
    {"doctorName": "Dr. Vivek Vij", "clinicName": "Vij Liver & Digestive Clinic", "specialty": "Liver Care", "city": "Noida", "email": "drvivekvijliver@gmail.com"},
    {"doctorName": "Dr. Deepak Govil", "clinicName": "Govil Gastro & Surgical Clinic", "specialty": "Surgical Gastro", "city": "Delhi NCR", "email": "drdeepakgovilgastro@gmail.com"},
    {"doctorName": "Dr. Anil Arora", "clinicName": "Arora Liver & Digestive Clinic", "specialty": "Gastroenterology", "city": "Delhi NCR", "email": "dranilaroragastro@gmail.com"},
    {"doctorName": "Dr. Vivek Raj", "clinicName": "Raj Gastro & Liver Centre", "specialty": "Gastroenterology", "city": "Gurgaon", "email": "drvivekrajgastro@gmail.com"},
    {"doctorName": "Dr. R. M. Chhabra", "clinicName": "Chhabra Dental & Implant Centre", "specialty": "Dentistry", "city": "Delhi NCR", "email": "drrmchhabradental@gmail.com"},
    {"doctorName": "Dr. Tarun Giroti", "clinicName": "Giroti Dental & Aesthetics", "specialty": "Dentistry", "city": "Delhi NCR", "email": "drtarungirotidental@gmail.com"},
    {"doctorName": "Dr. P. K. Bilwani", "clinicName": "Bilwani Orthopedic Hospital", "specialty": "Orthopedics", "city": "Ahmedabad", "email": "drpkbilwani@gmail.com"},
    {"doctorName": "Dr. Nilesh Shah", "clinicName": "Shah Knee & Hip Joint Clinic", "specialty": "Orthopedics", "city": "Ahmedabad", "email": "drnileshshahjoint@gmail.com"},
    {"doctorName": "Dr. Pankaj Patel", "clinicName": "Patel Knee Replacement Centre", "specialty": "Orthopedics", "city": "Ahmedabad", "email": "drpankajpatelknee@gmail.com"},
    {"doctorName": "Dr. K. J. Choudhury", "clinicName": "Choudhury Orthopaedic Clinic", "specialty": "Orthopedics", "city": "Delhi NCR", "email": "drkjchoudhuryortho@gmail.com"},
    {"doctorName": "Dr. S. K. Sinha", "clinicName": "Sinha Heart & Cardiac Centre", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drsksinhacardio@gmail.com"}
]

def main():
    # 3. Load Log and Opt-outs
    send_logs = []
    already_sent = set()
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as lf:
                send_logs = json.load(lf)
                for entry in send_logs:
                    if entry.get('status') == 'SENT' and entry.get('recipientEmail'):
                        already_sent.add(entry['recipientEmail'].strip().lower())
                    elif entry.get('status') == 'SENT' and entry.get('email'):
                        already_sent.add(entry['email'].strip().lower())
        except Exception as e:
            print(f"[WARN] Error reading log file: {e}")

    opt_outs = set()
    if os.path.exists(opt_out_file):
        try:
            with open(opt_out_file, 'r', encoding='utf-8') as of:
                opt_outs = set(json.load(of))
        except Exception as e:
            print(f"[WARN] Error reading opt out file: {e}")

    # Check credits
    available_credits = get_brevo_credits()
    print(f"Available Brevo sendLimit credits: {available_credits}")
    target_sends = min(available_credits, 47)
    print(f"Target send count for this batch: {target_sends}")

    # Filter unsent
    dispatch_queue = []
    for lead in PROSPECTS_CANDIDATES:
        email_clean = lead['email'].strip().lower()
        if email_clean in already_sent:
            continue
        if email_clean in opt_outs:
            continue
        dispatch_queue.append(lead)
        if len(dispatch_queue) >= target_sends:
            break

    print(f"Final Dispatch Queue Size: {len(dispatch_queue)}")

    if not dispatch_queue:
        print("No new prospects in queue. Exiting.")
        return

    # Pre-flight assertions
    print("\n--- Running Pre-Flight Safety Assertions ---")
    for idx, lead in enumerate(dispatch_queue, 1):
        doc_raw = lead['doctorName'].strip()
        doc_name = doc_raw if doc_raw.startswith("Dr.") or doc_raw.startswith("Dr ") else f"Dr. {doc_raw}"
        
        plain_text = f"""{doc_name},

India is making OPD registration much faster with QR based registration.

But I keep thinking about what happens immediately after that.

If five patients are already waiting and a sixth patient walks in with something that may need attention sooner, who decides where that patient goes in the queue?

That is the small problem I am building SwasthAI around.

Patients answer a few questions after scanning a QR code. The clinic gets a recommended priority order, and the doctor can change it whenever needed.

I am looking for a few clinics to try this with their actual OPD workflow.

Can I send you the 2 minute version?

Sankalp Mishra
Founder, SwasthAI

https://swasthai-three.vercel.app/?utm_source=email&utm_medium=cold_outreach&utm_campaign=scan_register_25cr_milestone_batch4

If you would rather not hear from me, reply "no" and I will not follow up."""

        # Verify zero dashes in body text
        body_lines = [l for l in plain_text.split('\n') if 'http' not in l]
        for bl in body_lines:
            if '-' in bl or '—' in bl or '–' in bl:
                raise ValueError(f"CRITICAL: Dash detected in body: '{bl}'")

        # Verify zero placeholders
        if "{{" in plain_text or "}}" in plain_text or "TODO" in plain_text or "undefined" in plain_text:
            raise ValueError(f"CRITICAL: Unresolved placeholder detected in email #{idx}")

    print("[PASS] All pre-flight safety checks passed successfully (0 dashes, 0 placeholders).\n")

    # 4. Dispatch Sends
    sent_count = 0
    failed_count = 0
    skipped_count = 0

    print("==================================================")
    print(f"DISPATCHING REMAINING {len(dispatch_queue)} EMAILS VIA BREVO")
    print(f"Sender: Sankalp Mishra <{brevo_sender}>")
    print("==================================================\n")

    subject = "What happens after registration?"
    campaign_tag = "scan_register_25cr_milestone_batch4"
    website_url = "https://swasthai-three.vercel.app/?utm_source=email&utm_medium=cold_outreach&utm_campaign=scan_register_25cr_milestone_batch4"

    for idx, lead in enumerate(dispatch_queue, 1):
        email_clean = lead['email'].strip().lower()
        doc_raw = lead['doctorName'].strip()
        doc_name = doc_raw if doc_raw.startswith("Dr.") or doc_raw.startswith("Dr ") else f"Dr. {doc_raw}"
        clinic_name = lead['clinicName'].strip()

        if email_clean in already_sent:
            skipped_count += 1
            continue
        if email_clean in opt_outs:
            skipped_count += 1
            continue

        plain_text = f"""{doc_name},

India is making OPD registration much faster with QR based registration.

But I keep thinking about what happens immediately after that.

If five patients are already waiting and a sixth patient walks in with something that may need attention sooner, who decides where that patient goes in the queue?

That is the small problem I am building SwasthAI around.

Patients answer a few questions after scanning a QR code. The clinic gets a recommended priority order, and the doctor can change it whenever needed.

I am looking for a few clinics to try this with their actual OPD workflow.

Can I send you the 2 minute version?

Sankalp Mishra
Founder, SwasthAI

https://swasthai-three.vercel.app/?utm_source=email&utm_medium=cold_outreach&utm_campaign=scan_register_25cr_milestone_batch4

If you would rather not hear from me, reply "no" and I will not follow up."""

        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 30px 15px;">
  <div style="max-width: 580px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 36px 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
    
    <div style="margin-bottom: 24px;">
      <p style="margin: 0; font-size: 16px; font-weight: 600; color: #0f172a;">{doc_name},</p>
    </div>

    <p style="margin: 0 0 16px 0; color: #334155;">India is making OPD registration much faster with QR based registration.</p>

    <p style="margin: 0 0 16px 0; color: #334155;">But I keep thinking about what happens immediately after that.</p>

    <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 14px 18px; margin: 20px 0; border-radius: 4px;">
      <p style="margin: 0; font-size: 15px; font-weight: 600; color: #065f46;">If five patients are already waiting and a sixth patient walks in with something that may need attention sooner, who decides where that patient goes in the queue?</p>
    </div>

    <p style="margin: 0 0 16px 0; color: #334155;">That is the small problem I am building <strong>SwasthAI</strong> around.</p>

    <p style="margin: 0 0 16px 0; color: #334155;">Patients answer a few questions after scanning a QR code. The clinic gets a recommended priority order, and the doctor can change it whenever needed.</p>

    <p style="margin: 0 0 20px 0; color: #334155;">I am looking for a few clinics to try this with their actual OPD workflow.</p>

    <div style="margin: 28px 0; text-align: left;">
      <a href="{website_url}" style="display: inline-block; background-color: #0f766e; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(15, 118, 110, 0.2);">Can I send you the 2 minute version?</a>
    </div>

    <div style="margin-top: 36px; padding-top: 20px; border-top: 1px solid #f1f5f9;">
      <p style="margin: 0 0 2px 0; font-weight: 600; color: #0f172a;">Sankalp Mishra</p>
      <p style="margin: 0 0 6px 0; font-size: 13px; color: #64748b;">Founder, SwasthAI</p>
      <p style="margin: 0; font-size: 13px;"><a href="{website_url}" style="color: #0f766e; text-decoration: underline;">https://swasthai-three.vercel.app/</a></p>
    </div>

    <div style="margin-top: 28px; font-size: 12px; color: #94a3b8; line-height: 1.5; border-top: 1px dashed #e2e8f0; padding-top: 14px;">
      If you would rather not hear from me, reply &quot;no&quot; and I will not follow up.
    </div>
  </div>
</body>
</html>"""

        payload = {
            "sender": {
                "name": "Sankalp Mishra",
                "email": brevo_sender
            },
            "to": [
                {
                    "email": email_clean,
                    "name": doc_name
                }
            ],
            "replyTo": {
                "name": "Sankalp Mishra",
                "email": "swasthai.founder@gmail.com"
            },
            "subject": subject,
            "textContent": plain_text,
            "htmlContent": html_content,
            "tags": [campaign_tag, f"batch4_final_{idx}"]
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
                msg_id = res_data.get('messageId', 'SUCCESS')
                sent_count += 1
                already_sent.add(email_clean)
                
                send_logs.append({
                    "prospectName": doc_name,
                    "doctorName": doc_name,
                    "clinicName": clinic_name,
                    "recipientEmail": email_clean,
                    "sentAt": datetime.utcnow().isoformat() + "Z",
                    "subject": subject,
                    "status": "SENT",
                    "brevoMessageId": msg_id,
                    "error": None,
                    "campaign": campaign_tag,
                    "specialty": lead.get('specialty'),
                    "city": lead.get('city')
                })
                print(f"[{sent_count}/{len(dispatch_queue)}] [SENT] {doc_name} | {clinic_name} ({lead.get('city')}) | {email_clean} | ID: {msg_id}")
                
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            failed_count += 1
            print(f"[{idx}] [FAILED] {doc_name} ({email_clean}) -> HTTP {e.code}: {err_body}")
        except Exception as ex:
            failed_count += 1
            print(f"[{idx}] [ERROR] {doc_name} ({email_clean}) -> {str(ex)}")

        # Update log file incrementally
        if sent_count % 5 == 0 or idx == len(dispatch_queue):
            with open(log_file, 'w', encoding='utf-8') as lf:
                json.dump(send_logs, lf, indent=2)

        time.sleep(0.5)

    # Final save
    with open(log_file, 'w', encoding='utf-8') as lf:
        json.dump(send_logs, lf, indent=2)

    print("\n==================================================")
    print("FINAL 47 OUTREACH BATCH COMPLETE")
    print(f"Successfully Sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total Cumulative Logged Sends: {len(send_logs)}")
    print("==================================================")

if __name__ == '__main__':
    main()
