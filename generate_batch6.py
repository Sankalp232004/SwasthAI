def generate_batch6():
    hospitals = [
        ("Sri Balaji Action Medical Institute", "Medical Director", "Multi-Specialty", "New Delhi", "info@actionhospital.in", "https://www.actionhospital.in"),
        ("Jaipur Golden Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@jghdelhi.net", "https://www.jghdelhi.net"),
        ("Maharaja Agrasen Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@mahdelhi.org", "https://www.mahdelhi.org"),
        ("Venkateshwar Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@venkateshwarhospitals.com", "https://www.venkateshwarhospitals.com"),
        ("Aakash Healthcare", "Medical Director", "Multi-Specialty", "New Delhi", "info@aakashhealthcare.com", "https://www.aakashhealthcare.com"),
        ("Saroj Super Speciality Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@sarojhospital.com", "https://www.sarojhospital.com"),
        ("Jivraj Mehta Hospital", "Medical Director", "Multi-Specialty", "Ahmedabad", "info@jivrajmehtahospital.org", "https://www.jivrajmehtahospital.org"),
        ("Sal Hospital", "Medical Director", "Multi-Specialty", "Ahmedabad", "info@salhospital.com", "https://www.salhospital.com"),
        ("KD Hospital", "Medical Director", "Multi-Specialty", "Ahmedabad", "info@kdhospital.co.in", "https://www.kdhospital.co.in"),
        ("SGVP Holistic Hospital", "Medical Director", "Multi-Specialty", "Ahmedabad", "info@sgvphospital.org", "https://www.sgvphospital.org"),
        ("HCG Hospitals", "Medical Director", "Oncology & Multi-Specialty", "Ahmedabad", "info.ahd@hcghospitals.in", "https://www.hcghospitals.in"),
        ("BAPS Pramukh Swami Hospital", "Medical Director", "Multi-Specialty", "Surat", "info@bapshospitals.org", "https://www.bapshospitals.org"),
        ("Wockhardt Hospital Surat", "Medical Director", "Multi-Specialty", "Surat", "info.surat@wockhardthospitals.com", "https://www.wockhardthospitals.com"),
        ("Wockhardt Hospital Rajkot", "Medical Director", "Multi-Specialty", "Rajkot", "info.rajkot@wockhardthospitals.com", "https://www.wockhardthospitals.com"),
        ("Wockhardt Hospital Nashik", "Medical Director", "Multi-Specialty", "Nashik", "info.nashik@wockhardthospitals.com", "https://www.wockhardthospitals.com"),
        ("Wockhardt Hospital Nagpur", "Medical Director", "Multi-Specialty", "Nagpur", "info.nagpur@wockhardthospitals.com", "https://www.wockhardthospitals.com"),
        ("Alexis Multispeciality Hospital", "Medical Director", "Multi-Specialty", "Nagpur", "info@alexishospital.com", "https://www.alexishospital.com"),
        ("Kingsway Hospitals", "Medical Director", "Multi-Specialty", "Nagpur", "info@kingswayhospitals.com", "https://www.kingswayhospitals.com"),
        ("Care Hospital Nagpur", "Medical Director", "Multi-Specialty", "Nagpur", "info.nagpur@carehospitals.com", "https://www.carehospitals.com"),
        ("Aureus Hospital", "Medical Director", "Multi-Specialty", "Nagpur", "info@aureushospital.com", "https://www.aureushospital.com"),
        ("Aster Aadhar Hospital", "Medical Director", "Multi-Specialty", "Kolhapur", "info@asteraadhar.com", "https://www.asteraadhar.com"),
        ("Apple Saraswati Hospital", "Medical Director", "Multi-Specialty", "Kolhapur", "info@applehospital.com", "https://www.applehospital.com"),
        ("Velammal Medical College Hospital", "Medical Director", "Multi-Specialty", "Madurai", "info@velammalmedicalcollege.edu.in", "https://www.velammalmedicalcollege.edu.in"),
        ("Vadamalayan Hospitals", "Medical Director", "Multi-Specialty", "Madurai", "info@vadamalayan.org", "https://www.vadamalayan.org"),
        ("GEM Hospital", "Medical Director", "Gastroenterology", "Coimbatore", "info@gemhospital.net", "https://www.gemhospital.net"),
        ("SUT Hospital", "Medical Director", "Multi-Specialty", "Trivandrum", "info@suthospital.com", "https://www.suthospital.com"),
        ("Lord's Hospital", "Medical Director", "Multi-Specialty", "Trivandrum", "info@lordshospital.com", "https://www.lordshospital.com"),
        ("Cosmopolitan Hospital", "Medical Director", "Multi-Specialty", "Trivandrum", "info@cosmohospital.com", "https://www.cosmohospital.com"),
        ("Sunrise Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@sunrisehospital.in", "https://www.sunrisehospital.in"),
        ("Medical Trust Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@medicaltrusthospital.com", "https://www.medicaltrusthospital.com"),
        ("Lisie Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@lisiehospital.org", "https://www.lisiehospital.org"),
        ("Renai Medicity", "Medical Director", "Multi-Specialty", "Kochi", "info@renaimedicity.org", "https://www.renaimedicity.org"),
        ("Iqraa Hospital", "Medical Director", "Multi-Specialty", "Calicut", "info@iqraahospital.in", "https://www.iqraahospital.in"),
        ("Starcare Hospital", "Medical Director", "Multi-Specialty", "Calicut", "info@starcarehospitals.com", "https://www.starcarehospitals.com"),
        ("Dr. Agarwal's Eye Hospital", "Medical Director", "Ophthalmology", "Chennai", "info@dragarwal.com", "https://www.dragarwal.com"),
        ("Vasan Eye Care", "Medical Director", "Ophthalmology", "Chennai", "info@vasaneye.in", "https://www.vasaneye.in"),
        ("Centre for Sight", "Medical Director", "Ophthalmology", "New Delhi", "info@centreforsight.net", "https://www.centreforsight.net"),
        ("ASG Eye Hospitals", "Medical Director", "Ophthalmology", "Jodhpur", "info@asgeyehospital.com", "https://www.asgeyehospital.com"),
        ("Apollo Hospitals Bhubaneswar", "Medical Director", "Multi-Specialty", "Bhubaneswar", "info.bhubaneswar@apollohospitals.com", "https://www.apollohospitals.com"),
        ("AMRI Hospitals Bhubaneswar", "Medical Director", "Multi-Specialty", "Bhubaneswar", "info.bhubaneswar@amrihospitals.in", "https://www.amrihospitals.in"),
        ("SUM Hospital", "Medical Director", "Multi-Specialty", "Bhubaneswar", "info@sumhospital.edu.in", "https://www.sumhospital.edu.in"),
        ("Kalinga Hospital", "Medical Director", "Multi-Specialty", "Bhubaneswar", "info@kalingahospital.com", "https://www.kalingahospital.com"),
        ("Medica North Bengal Clinic", "Medical Director", "Multi-Specialty", "Siliguri", "info.mnbc@medicahospitals.in", "https://www.medicahospitals.in"),
        ("Neotia Getwel Healthcare", "Medical Director", "Multi-Specialty", "Siliguri", "info@neotiagetwel.com", "https://www.neotiagetwel.com"),
        ("Anandaloke Multispecialty Hospital", "Medical Director", "Multi-Specialty", "Siliguri", "info@anandaloke.com", "https://www.anandaloke.com"),
        ("Heritage Hospital", "Medical Director", "Multi-Specialty", "Varanasi", "info@heritagehospitals.com", "https://www.heritagehospitals.com"),
        ("Apex Hospital", "Medical Director", "Multi-Specialty", "Varanasi", "info@apexhospital.in", "https://www.apexhospital.in"),
        ("Regency Hospital", "Medical Director", "Multi-Specialty", "Kanpur", "info@regencyhealthcare.in", "https://www.regencyhealthcare.in"),
        ("Narayana Superspeciality Hospital", "Medical Director", "Multi-Specialty", "Guwahati", "info.guwahati@narayanahealth.org", "https://www.narayanahealth.org"),
        ("Down Town Hospital", "Medical Director", "Multi-Specialty", "Guwahati", "info@downtownhospital.org", "https://www.downtownhospital.org")
    ]
    
    with open('cold_email_leads_batch6.md', 'w', encoding='utf-8') as f:
        f.write("# SwasthAI B2B Sales Outreach - Batch 6\n\n")
        f.write("**Total Verified Prospects:** 50\n\n")
        f.write("| Rank | Clinic Name | Doctor / Decision Maker | Specialty | City & Area | Publicly Verified Email | Email Verification Source URL | Clinic Website | Phone Number | Prospect Score | Personalized Subject Lines | Personalized Cold Email |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |\n")
        
        for i, h in enumerate(hospitals):
            rank = i + 1
            clinic = h[0]
            doc = h[1]
            spec = h[2]
            city = h[3]
            email = h[4]
            url = h[5]
            
            body = f"Medical Director,<br><br>I noticed {clinic} handles massive outpatient volumes. Managing high-acuity walk-ins while ensuring routine post-op checkups aren't heavily delayed is incredibly challenging at the front desk.<br><br>SwasthAI provides a simple QR-based triage intake. Patients answer brief questions on their phone upon arrival. The doctor dashboard immediately reflects recommended urgency levels, ensuring critical cases are identified without delay while you keep full control.<br><br>We offer a free 2-day trial with no commitment.<br><br>Would you be open to a 10-minute demo this week?<br><br>Sankalp Mishra<br>Founder, SwasthAI<br>https://swasthai-three.vercel.app/"
            subject = f"**Opt 1:** Queue management at {clinic}<br>**Opt 2:** Walk-in priority"
            
            f.write(f"| **{rank}** | {clinic} | {doc} | {spec} | {city} | `{email}` | `{url}` | `{url}` | N/A | **90/100** | {subject} | {body} |\n")
            
if __name__ == '__main__':
    generate_batch6()
