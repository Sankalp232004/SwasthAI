import re
import urllib.request
import urllib.error
import ssl
import json
import time

api_key = "INSERT_API_KEY_HERE"
url = "https://api.brevo.com/v3/smtp/email"

def send_email(to_email, to_name, subject, body):
    data = {
        "sender": {"name": "Sankalp Mishra", "email": "swasthai.founder@gmail.com"},
        "to": [{"email": to_email, "name": to_name}],
        "replyTo": {"email": "swasthai.founder@gmail.com", "name": "Sankalp Mishra"},
        "subject": subject,
        "textContent": body
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header('api-key', api_key)
    req.add_header('Content-Type', 'application/json')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"Failed to send to {to_email}. Error: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Exception sending to {to_email}: {e}")
        return None

def process_file():
    with open('cold_email_leads_batch6.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the table
    lines = content.split('\n')
    table_lines = [l for l in lines if l.startswith('| **')]
    
    success_count = 0
    for line in table_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 13:
            continue
            
        clinic_name = parts[2]
        doctor_name = parts[3]
        email_part = parts[6]
        
        # Extract email from `email`
        email_match = re.search(r'`([^`]+)`', email_part)
        if not email_match:
            continue
        email = email_match.group(1)
        
        subject_part = parts[11]
        body_part = parts[12]
        
        # Take Opt 1 for subject
        subject = subject_part.split('<br>')[0].replace('**Opt 1:** ', '').strip()
        
        # Replace <br> with newlines in body
        body = body_part.replace('<br>', '\n')
        
        # Proofread: remove placeholders and dashes
        body = re.sub(r'\[.*?\]', '', body)
        body = body.replace(' - ', ' ')
        
        print(f"Sending to {email} ({clinic_name})...")
        res = send_email(email, doctor_name, subject, body)
        if res:
            success_count += 1
            print(f"  Success: {res}")
            
        time.sleep(0.5)
        
    print(f"\\nFinished sending! Successfully sent {success_count} emails out of {len(table_lines)}.")

if __name__ == '__main__':
    process_file()
