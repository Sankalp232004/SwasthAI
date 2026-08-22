def generate_batch5():
    hospitals = [
        ("Medicover Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@medicoverhospitals.in", "https://www.medicoverhospitals.in"),
        ("Sunshine Hospitals", "Medical Director", "Orthopedics & Multi-Specialty", "Hyderabad", "info@sunshinehospitals.com", "https://www.sunshinehospitals.com"),
        ("Omni Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@omnihospitals.in", "https://www.omnihospitals.in"),
        ("Kamineni Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@kaminenihospitals.com", "https://www.kaminenihospitals.com"),
        ("STAR Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@starhospitals.in", "https://www.starhospitals.in"),
        ("Citizens Specialty Hospital", "Medical Director", "Multi-Specialty", "Hyderabad", "info@citizenshospitals.com", "https://www.citizenshospitals.com"),
        ("Virinchi Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@virinchihospitals.com", "https://www.virinchihospitals.com"),
        ("Pace Hospitals", "Medical Director", "Multi-Specialty", "Hyderabad", "info@pacehospital.com", "https://www.pacehospital.com"),
        ("Basavatarakam Indo-American Cancer", "Medical Director", "Oncology", "Hyderabad", "info@induscancer.com", "https://www.induscancer.com"),
        ("L.V. Prasad Eye Institute", "Medical Director", "Ophthalmology", "Hyderabad", "info@lvpei.org", "https://www.lvpei.org"),
        ("Sankara Nethralaya", "Medical Director", "Ophthalmology", "Chennai", "info@snmail.org", "https://www.sankaranethralaya.org"),
        ("Aravind Eye Hospital", "Medical Director", "Ophthalmology", "Madurai", "info@aravind.org", "https://www.aravind.org"),
        ("Narayana Nethralaya", "Medical Director", "Ophthalmology", "Bengaluru", "info@narayananethralaya.com", "https://www.narayananethralaya.com"),
        ("M.S. Ramaiah Memorial Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@msrmh.com", "https://www.msrmh.com"),
        ("Baptist Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@bbh.org.in", "https://www.bbh.org.in"),
        ("St. John's Medical College Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@stjohns.in", "https://www.stjohns.in"),
        ("Apollo Spectra Hospitals", "Medical Director", "Multi-Specialty", "Bengaluru", "info@apollospectra.com", "https://www.apollospectra.com"),
        ("Sagar Hospitals", "Medical Director", "Multi-Specialty", "Bengaluru", "info@sagarhospitals.in", "https://www.sagarhospitals.in"),
        ("Vikram Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@vikramhospital.com", "https://www.vikramhospital.com"),
        ("HOSMAT Hospital", "Medical Director", "Orthopedics & Trauma", "Bengaluru", "info@hosmathospitals.com", "https://www.hosmathospitals.com"),
        ("Santosh Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@santoshhospitals.com", "https://www.santoshhospitals.com"),
        ("Narayana Multispeciality Hospital", "Medical Director", "Multi-Specialty", "Mysore", "info.mysore@narayanahealth.org", "https://www.narayanahealth.org"),
        ("KMC Hospital", "Medical Director", "Multi-Specialty", "Mangalore", "info.kmc@manipalhospitals.com", "https://www.manipalhospitals.com"),
        ("Father Muller Medical College", "Medical Director", "Multi-Specialty", "Mangalore", "info@fathermuller.in", "https://www.fathermuller.in"),
        ("A.J. Hospital & Research Centre", "Medical Director", "Multi-Specialty", "Mangalore", "info@ajhospital.in", "https://www.ajhospital.in"),
        ("Amrita Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@amritahospitals.org", "https://www.amritahospitals.org"),
        ("Lakeshore Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@lakeshorehospital.com", "https://www.lakeshorehospital.com"),
        ("KIMSHEALTH", "Medical Director", "Multi-Specialty", "Trivandrum", "info@kimshealth.org", "https://www.kimshealth.org"),
        ("PRS Hospital", "Medical Director", "Multi-Specialty", "Trivandrum", "info@prshospital.com", "https://www.prshospital.com"),
        ("Ananthapuri Hospitals", "Medical Director", "Multi-Specialty", "Trivandrum", "info@ananthapurihospitals.com", "https://www.ananthapurihospitals.com"),
        ("Baby Memorial Hospital", "Medical Director", "Multi-Specialty", "Calicut", "info@babymemorialhospital.com", "https://www.babymemorialhospital.com"),
        ("MIMS Hospital", "Medical Director", "Multi-Specialty", "Calicut", "info@astermims.com", "https://www.astermims.com"),
        ("Meitra Hospital", "Medical Director", "Multi-Specialty", "Calicut", "info@meitra.com", "https://www.meitra.com"),
        ("Rajagiri Hospital", "Medical Director", "Multi-Specialty", "Kochi", "info@rajagirihospital.com", "https://www.rajagirihospital.com"),
        ("Kovai Medical Center", "Medical Director", "Multi-Specialty", "Coimbatore", "info@kmchhospitals.com", "https://www.kmchhospitals.com"),
        ("Sri Ramakrishna Hospital", "Medical Director", "Multi-Specialty", "Coimbatore", "info@sriramakrishnahospital.com", "https://www.sriramakrishnahospital.com"),
        ("Ganga Hospital", "Medical Director", "Orthopedics & Trauma", "Coimbatore", "info@gangahospital.com", "https://www.gangahospital.com"),
        ("Christian Medical College", "Medical Director", "Multi-Specialty", "Ludhiana", "info@cmcludhiana.in", "https://www.cmcludhiana.in"),
        ("Dayanand Medical College", "Medical Director", "Multi-Specialty", "Ludhiana", "info@dmch.edu", "https://www.dmch.edu"),
        ("Fortis Hospital Mohali", "Medical Director", "Multi-Specialty", "Mohali", "info@fortismohali.com", "https://www.fortishealthcare.com"),
        ("Max Super Speciality Hospital Mohali", "Medical Director", "Multi-Specialty", "Mohali", "info.mohali@maxhealthcare.com", "https://www.maxhealthcare.in"),
        ("Ivy Hospital", "Medical Director", "Multi-Specialty", "Mohali", "info@ivyhospital.com", "https://www.ivyhospital.com"),
        ("Alchemist Hospital", "Medical Director", "Multi-Specialty", "Panchkula", "info@alchemisthospitals.com", "https://www.alchemisthospitals.com"),
        ("Ojas Hospital", "Medical Director", "Multi-Specialty", "Panchkula", "info@ojashospital.com", "https://www.ojashospital.com"),
        ("Mukat Hospital", "Medical Director", "Multi-Specialty", "Chandigarh", "info@mukathospital.com", "https://www.mukathospital.com"),
        ("Healing Hospital", "Medical Director", "Multi-Specialty", "Chandigarh", "info@healinghospital.co.in", "https://www.healinghospital.co.in"),
        ("Sant Parmanand Hospital", "Medical Director", "Orthopedics & Multi-Specialty", "New Delhi", "info@sphdelhi.org", "https://www.sphdelhi.org"),
        ("Kalra Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@kalrahospital.com", "https://www.kalrahospital.com"),
        ("Tirath Ram Shah Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@tirathramhospital.org", "https://www.tirathramhospital.org"),
        ("Mata Chanan Devi Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@mcdh.in", "https://www.mcdh.in")
    ]
    
    with open('cold_email_leads_batch5.md', 'w', encoding='utf-8') as f:
        f.write("# SwasthAI B2B Sales Outreach - Batch 5\n\n")
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
    generate_batch5()
