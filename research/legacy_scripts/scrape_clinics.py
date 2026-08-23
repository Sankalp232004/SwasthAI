import re
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlparse
import json
import time
import sys

def search_duckduckgo(query, num_results=10):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='ignore')
        # Extract URLs
        links = re.findall(r'class="result__url" href="([^"]+)"', html)
        # DuckDuckGo sometimes uses a redirect link, let's just parse href normally or via regex
        links = re.findall(r'href="//duckduckgo.com/l/\?uddg=([^"&]+)', html)
        decoded_links = [urllib.parse.unquote(link) for link in links]
        
        if not decoded_links:
            # Fallback regex if layout changed
            links = re.findall(r'a class="result__snippet[^"]*" href="([^"]+)"', html)
            decoded_links = links
            
        return decoded_links[:num_results]
    except Exception as e:
        print(f"Error searching DuckDuckGo for {query}: {e}")
        return []

def extract_emails_from_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': 'text/html'})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        html = urllib.request.urlopen(req, context=ctx, timeout=5).read().decode('utf-8', errors='ignore')
        
        # Regex for emails
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
        
        valid_emails = []
        for e in set(emails):
            e = e.lower()
            if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.js', '.css')) and not e.startswith('u00'):
                if 'sentry' not in e and 'wix' not in e and 'example' not in e and 'domain' not in e:
                    valid_emails.append(e)
                    
        return valid_emails
    except Exception as e:
        return []

def generate_prospects():
    queries = [
        "orthopedic clinic pune contact email",
        "pediatric clinic pune contact email",
        "orthopedic hospital lucknow email address",
        "ent clinic gurgaon email address",
        "mumbai knee clinic contact email",
        "hyderabad orthopedic clinic email address",
        "bangalore pediatric clinic contact email",
        "chennai ortho clinic email address",
        "jaipur joint replacement email address",
        "kolkata ent clinic contact email"
    ]
    
    prospects = []
    seen_emails = set()
    
    print("Starting scraping process. This may take a few minutes...")
    
    for q in queries:
        print(f"Searching: {q}")
        urls = search_duckduckgo(q, num_results=10)
        
        for url in urls:
            if len(prospects) >= 50:
                break
                
            domain = urlparse(url).netloc
            if 'justdial.com' in domain or 'practo.com' in domain or 'lybrate.com' in domain or 'facebook.com' in domain or 'instagram.com' in domain or 'linkedin.com' in domain:
                continue
                
            print(f"  Scraping: {url}")
            emails = extract_emails_from_url(url)
            
            for email in emails:
                if email not in seen_emails:
                    seen_emails.add(email)
                    
                    # Try to extract clinic name from domain
                    clinic_name = domain.replace('www.', '').split('.')[0].title() + " Clinic"
                    city = q.split()[2].title()
                    
                    prospects.append({
                        "rank": len(prospects) + 1,
                        "clinicName": clinic_name,
                        "doctorName": "Clinic Director",
                        "specialty": "Medical Practice",
                        "city": city,
                        "email": email,
                        "sourceUrl": url,
                        "subjectLine": f"Patient intake workflow at {clinic_name}",
                        "emailBody": f"Hello,\n\nI noticed {clinic_name} manages significant patient traffic in {city}. In busy clinics, managing walk-ins alongside pre-booked consultations can cause queue bottlenecks at the front desk.\n\nSwasthAI automates patient intake via a simple QR code at reception. Patients submit structured symptoms in 60 seconds, and your console receives a recommended priority order, ensuring acute cases are surfaced immediately while you retain full control.\n\nWe offer a 2-day trial with zero setup fee.\n\nWould it be useful if I showed you how it works in 10 minutes?\n\nSankalp Mishra\nFounder, SwasthAI\nhttps://swasthai-three.vercel.app/"
                    })
                    print(f"    Found email: {email}")
                    if len(prospects) >= 50:
                        break
        
        if len(prospects) >= 50:
            break
            
        time.sleep(2) # be nice to DDG
        
    return prospects

def write_markdown(prospects):
    with open('cold_email_leads_scraped.md', 'w', encoding='utf-8') as f:
        f.write("# SwasthAI B2B Sales Outreach - Scraped Batch\n\n")
        f.write(f"**Total Found:** {len(prospects)}\n\n")
        
        f.write("| Rank | Clinic Name | Doctor | City | Email | Source URL | Subject Line | Email Body |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        for p in prospects:
            body = p['emailBody'].replace('\n', '<br>')
            f.write(f"| **{p['rank']}** | {p['clinicName']} | {p['doctorName']} | {p['city']} | `{p['email']}` | `{p['sourceUrl']}` | {p['subjectLine']} | {body} |\n")

if __name__ == '__main__':
    prospects = generate_prospects()
    write_markdown(prospects)
    print(f"\\nFinished! Found {len(prospects)} prospects. Saved to cold_email_leads_scraped.md")
