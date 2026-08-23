import urllib.request
import json
import ssl

url = "https://api.brevo.com/v3/smtp/email"
api_key = "INSERT_API_KEY_HERE"

data = {
    "sender": {"name": "Sankalp Mishra", "email": "swasthai.founder@gmail.com"},
    "to": [{"email": "mishrasankalp04@gmail.com", "name": "Sankalp Mishra"}],
    "replyTo": {"email": "swasthai.founder@gmail.com", "name": "Sankalp Mishra"},
    "subject": "[TEST] Question about pediatric intake at Strong Bones Clinic",
    "textContent": """Dr. Ashish Ranade,

I was curious how your team at Strong Bones Clinic currently handles queue prioritization when an acute walk-in arrives during busy consultative sessions in Pune (Deccan Gymkhana).

I built SwasthAI to help clinics organize patient intake. Patients scan a QR code and answer a few structured questions about their symptoms. SwasthAI then shows a recommended priority order on the clinic screen, while the doctor remains in full control of the final queue.

We offer a free 2-day trial with zero setup fee or commitment.

Would it be useful if I sent you a 2-minute screen recording first?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you'd rather not hear from me, just reply 'no' and I won't follow up."""
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
req.add_header('api-key', api_key)
req.add_header('Content-Type', 'application/json')

try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print("Success:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Error:", e.read().decode('utf-8'))
except Exception as e:
    print("Exception:", str(e))
