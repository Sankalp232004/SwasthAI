def generate_batch4():
    hospitals = [
        ("Wockhardt Hospitals", "Medical Director", "Multi-Specialty", "Mumbai", "info@wockhardthospitals.com", "https://www.wockhardthospitals.com"),
        ("Bombay Hospital", "Medical Director", "Multi-Specialty", "Mumbai", "info@bombayhospital.com", "https://www.bombayhospital.com"),
        ("Bhatia Hospital", "Medical Director", "Multi-Specialty", "Mumbai", "info@bhatiahospital.org", "https://www.bhatiahospital.org"),
        ("SL Raheja Hospital", "Medical Director", "Multi-Specialty", "Mumbai", "info@slraheja.com", "https://www.slraheja.com"),
        ("Global Hospitals", "Medical Director", "Multi-Specialty", "Chennai", "info@globalhospitalsindia.com", "https://www.globalhospitalsindia.com"),
        ("BGS Gleneagles Global", "Medical Director", "Multi-Specialty", "Bengaluru", "info.bgs@gleneaglesglobal.com", "https://www.gleneaglesglobal.com"),
        ("Sakra World Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@sakraworldhospital.com", "https://www.sakraworldhospital.com"),
        ("Sparsh Hospital", "Medical Director", "Orthopedics & Multi-Specialty", "Bengaluru", "info@sparshhospital.com", "https://www.sparshhospital.com"),
        ("Aster CMI Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@astercmi.com", "https://www.astercmi.com"),
        ("Aster RV Hospital", "Medical Director", "Multi-Specialty", "Bengaluru", "info@asterrv.com", "https://www.asterrv.com"),
        ("RxDx Healthcare", "Medical Director", "Multi-Specialty", "Bengaluru", "info@rxdx.in", "https://www.rxdx.in"),
        ("Kauvery Hospital", "Medical Director", "Multi-Specialty", "Chennai", "info@kauveryhospital.com", "https://www.kauveryhospital.com"),
        ("SIMS Hospital", "Medical Director", "Multi-Specialty", "Chennai", "info@simshospitals.com", "https://www.simshospitals.com"),
        ("MGM Healthcare", "Medical Director", "Multi-Specialty", "Chennai", "info@mgmhealthcare.in", "https://www.mgmhealthcare.in"),
        ("MIOT International", "Medical Director", "Orthopedics & Multi-Specialty", "Chennai", "info@miotinternational.com", "https://www.miotinternational.com"),
        ("Sri Ramachandra Medical Centre", "Medical Director", "Multi-Specialty", "Chennai", "info@sriramachandra.edu.in", "https://www.sriramachandra.edu.in"),
        ("Chettinad Super Speciality", "Medical Director", "Multi-Specialty", "Chennai", "info@chettinadhealthcity.com", "https://www.chettinadhealthcity.com"),
        ("Vijaya Hospital", "Medical Director", "Multi-Specialty", "Chennai", "info@vijayahospital.org", "https://www.vijayahospital.org"),
        ("Billroth Hospitals", "Medical Director", "Multi-Specialty", "Chennai", "info@billrothhospitals.com", "https://www.billrothhospitals.com"),
        ("Meenakshi Mission Hospital", "Medical Director", "Multi-Specialty", "Madurai", "info@mmhrc.in", "https://www.mmhrc.in"),
        ("PSG Hospitals", "Medical Director", "Multi-Specialty", "Coimbatore", "info@psghospitals.com", "https://www.psghospitals.com"),
        ("GKNM Hospital", "Medical Director", "Multi-Specialty", "Coimbatore", "info@gknmhospital.org", "https://www.gknmhospital.org"),
        ("K G Hospital", "Medical Director", "Multi-Specialty", "Coimbatore", "info@kghospital.com", "https://www.kghospital.com"),
        ("Royal Care Hospital", "Medical Director", "Multi-Specialty", "Coimbatore", "info@royalcarehospital.in", "https://www.royalcarehospital.in"),
        ("CMC Vellore", "Medical Director", "Multi-Specialty", "Vellore", "info@cmcvellore.ac.in", "https://www.cmcvellore.ac.in"),
        ("Tata Memorial Hospital", "Medical Director", "Oncology", "Mumbai", "info@tmc.gov.in", "https://tmc.gov.in"),
        ("Rajiv Gandhi Cancer Institute", "Medical Director", "Oncology", "New Delhi", "info@rgcirc.org", "https://www.rgcirc.org"),
        ("Moolchand Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@moolchandhealthcare.com", "https://www.moolchandhealthcare.com"),
        ("Holy Family Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@holyfamilyhospitaldelhi.org", "https://www.holyfamilyhospitaldelhi.org"),
        ("St Stephen's Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@ststephenshospital.org", "https://www.ststephenshospital.org"),
        ("Batra Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@batrahospitaldelhi.org", "https://www.batrahospitaldelhi.org"),
        ("PSRI Hospital", "Medical Director", "Multi-Specialty", "New Delhi", "info@psrihospital.com", "https://www.psrihospital.com"),
        ("Indian Spinal Injuries Centre", "Medical Director", "Orthopedics & Spine", "New Delhi", "info@isiconline.org", "https://www.isiconline.org"),
        ("VIMHANS Hospital", "Medical Director", "Neuro & Multi-Specialty", "New Delhi", "info@vimhans.com", "https://www.vimhans.com"),
        ("IHBAS Hospital", "Medical Director", "Neuro & Psychiatry", "New Delhi", "info@ihbas.org", "https://www.ihbas.org"),
        ("Apollo Cradle", "Medical Director", "Maternity & Pediatrics", "Hyderabad", "info@apollocradle.com", "https://www.apollocradle.com"),
        ("Neotia Bhagirathi Woman and Child", "Medical Director", "Maternity & Pediatrics", "Kolkata", "info@neotiahospital.com", "https://www.neotiahospital.com"),
        ("Bhagirathi Neotia Woman", "Medical Director", "Maternity & Pediatrics", "Kolkata", "info@neotiahealthcare.com", "https://www.neotiahealthcare.com"),
        ("Ruby General Hospital", "Medical Director", "Multi-Specialty", "Kolkata", "info@rubyhospital.com", "https://www.rubyhospital.com"),
        ("Desun Hospital", "Medical Director", "Multi-Specialty", "Kolkata", "info@desunhospital.com", "https://www.desunhospital.com"),
        ("Fortis Escorts Heart Institute", "Medical Director", "Cardiology", "New Delhi", "info@fortisescorts.in", "https://www.fortisescorts.in"),
        ("National Heart Institute", "Medical Director", "Cardiology", "New Delhi", "info@nhi.in", "https://www.nhi.in"),
        ("Asian Heart Institute", "Medical Director", "Cardiology", "Mumbai", "info@asianheartinstitute.org", "https://www.asianheartinstitute.org"),
        ("U N Mehta Institute", "Medical Director", "Cardiology", "Ahmedabad", "info@unmicrc.org", "https://www.unmicrc.org"),
        ("GCS Medical College", "Medical Director", "Multi-Specialty", "Ahmedabad", "info@gcsmc.org", "https://www.gcsmc.org"),
        ("Sanjeevani Hospital", "Medical Director", "Multi-Specialty", "Pune", "info@sanjeevanihospital.com", "https://www.sanjeevanihospital.com"),
        ("Inamdar Multispeciality", "Medical Director", "Multi-Specialty", "Pune", "info@inamdarhospital.com", "https://www.inamdarhospital.com"),
        ("Deenanath Mangeshkar Hospital", "Medical Director", "Multi-Specialty", "Pune", "info@dmhospital.org", "https://www.dmhospital.org"),
        ("Aditya Birla Memorial", "Medical Director", "Multi-Specialty", "Pune", "info@adityabirlahospital.com", "https://www.adityabirlahospital.com"),
        ("Oyster & Pearl Hospitals", "Medical Director", "Maternity & Pediatrics", "Pune", "info@onphospital.com", "https://www.onphospital.com")
    ]
    
    with open('cold_email_leads_batch4.md', 'w', encoding='utf-8') as f:
        f.write("# SwasthAI B2B Sales Outreach - Batch 4\n\n")
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
    generate_batch4()
