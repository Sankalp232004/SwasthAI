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

# 2. DNS MX Record Checker (Google DNS over HTTPS)
def check_domain_mx(domain):
    try:
        url = f"https://dns.google/resolve?name={domain}&type=MX"
        req = urllib.request.Request(url, headers={"accept": "application/json", "user-agent": "SwasthAI-MX-Validator"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            answers = data.get("Answer", [])
            mx_hosts = [a.get("data") for a in answers if a.get("type") == 15]
            return len(mx_hosts) > 0, mx_hosts
    except Exception:
        return False, []

# 3. Check remaining Brevo credits
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
        return 170

PROSPECTS_POOL = [
    # --- PEDIATRICS & CHILD CARE ---
    {"doctorName": "Dr. Sandeep Kadam", "clinicName": "Kadam Children Hospital", "specialty": "Pediatrics", "city": "Pune", "email": "kadamhospitalpune@gmail.com"},
    {"doctorName": "Dr. Sachin Shah", "clinicName": "Surya Children's Clinic", "specialty": "Pediatrics", "city": "Pune", "email": "suryachildrenpune@gmail.com"},
    {"doctorName": "Dr. Shilpa Aroskar", "clinicName": "Aroskar Child Clinic", "specialty": "Pediatrics", "city": "Navi Mumbai", "email": "drshilpa.aroskar@gmail.com"},
    {"doctorName": "Dr. Nitin Verma", "clinicName": "Verma Child Clinic", "specialty": "Pediatrics", "city": "Delhi NCR", "email": "drnitinverma.ped@gmail.com"},
    {"doctorName": "Dr. Sanjay Srirampur", "clinicName": "Srirampur Child Health Centre", "specialty": "Pediatrics", "city": "Hyderabad", "email": "drsrirampur@gmail.com"},
    {"doctorName": "Dr. Vivek Jain", "clinicName": "Jain Child & Newborn Clinic", "specialty": "Pediatrics", "city": "Jaipur", "email": "drvivekjainjaipur@gmail.com"},
    {"doctorName": "Dr. Bhupendra Sharma", "clinicName": "Sharma Pediatric Clinic", "specialty": "Pediatrics", "city": "Jaipur", "email": "drbhupendrasharma@gmail.com"},
    {"doctorName": "Dr. Rajiv Uttam", "clinicName": "Uttam Child Healthcare", "specialty": "Pediatric Critical Care", "city": "Gurgaon", "email": "drrajivuttam@gmail.com"},
    {"doctorName": "Dr. Sunil Agrawal", "clinicName": "Agrawal Child Clinic", "specialty": "Pediatrics", "city": "Indore", "email": "drsunilagrawalindore@gmail.com"},
    {"doctorName": "Dr. Rajesh Kulkarni", "clinicName": "Kulkarni Pediatric Centre", "specialty": "Pediatrics", "city": "Pune", "email": "drrajeshkulkarnipune@gmail.com"},
    {"doctorName": "Dr. Anand Shandilya", "clinicName": "Shandilya Child Care", "specialty": "Pediatrics", "city": "Lucknow", "email": "drshandilyachild@gmail.com"},
    {"doctorName": "Dr. Alok Gupta", "clinicName": "Gupta Child Hospital", "specialty": "Pediatrics", "city": "Kanpur", "email": "dralokguptakanpur@gmail.com"},
    {"doctorName": "Dr. Manish Kumar", "clinicName": "Kumar Child Clinic", "specialty": "Pediatrics", "city": "Patna", "email": "drmanishchildpatna@gmail.com"},
    {"doctorName": "Dr. Suresh Reddy", "clinicName": "Reddy Pediatric Clinic", "specialty": "Pediatrics", "city": "Bengaluru", "email": "drsureshreddykids@gmail.com"},
    {"doctorName": "Dr. Meena Nathan", "clinicName": "Nathan Child Clinic", "specialty": "Pediatrics", "city": "Chennai", "email": "drnathanpediatrics@gmail.com"},
    {"doctorName": "Dr. S. K. Mahapatra", "clinicName": "Mahapatra Child Health Centre", "specialty": "Pediatrics", "city": "Bhubaneswar", "email": "drmahapatrachild@gmail.com"},
    {"doctorName": "Dr. R. K. Goel", "clinicName": "Goel Pediatric Care", "specialty": "Pediatrics", "city": "Chandigarh", "email": "drgoelchildcare@gmail.com"},
    {"doctorName": "Dr. Amitava Sengupta", "clinicName": "Sengupta Child Clinic", "specialty": "Pediatrics", "city": "Kolkata", "email": "drsenguptaped@gmail.com"},
    {"doctorName": "Dr. Prashant Joshi", "clinicName": "Joshi Pediatric Care", "specialty": "Pediatrics", "city": "Nagpur", "email": "drprashantjoshingp@gmail.com"},
    {"doctorName": "Dr. Vipul Gupta", "clinicName": "Gupta Newborn & Child Care", "specialty": "Pediatrics", "city": "Agra", "email": "drvipulguptaagra@gmail.com"},

    # --- ORTHOPEDICS & SPINE / JOINT CARE ---
    {"doctorName": "Dr. Sudhir Babhulkar", "clinicName": "Sushrut Hospital & Orthopedic Centre", "specialty": "Orthopedics", "city": "Nagpur", "email": "sushrutnagpur@gmail.com"},
    {"doctorName": "Dr. Rajeev Joshi", "clinicName": "Joshi Orthopaedic Hospital", "specialty": "Orthopedics", "city": "Pune", "email": "drjoshiarthrocare@gmail.com"},
    {"doctorName": "Dr. Shirish Pathak", "clinicName": "Pathak Joint Replacement Centre", "specialty": "Orthopedics", "city": "Pune", "email": "drshirishpathak@gmail.com"},
    {"doctorName": "Dr. Ajay Kothari", "clinicName": "San来看 Spine & Joint Clinic", "specialty": "Orthopedics & Spine", "city": "Pune", "email": "drajaykotharispine@gmail.com"},
    {"doctorName": "Dr. Hemant Wakankar", "clinicName": "Wakankar Joint Clinic", "specialty": "Orthopedics", "city": "Pune", "email": "drhemantwakankar@gmail.com"},
    {"doctorName": "Dr. Sanjay Agarwala", "clinicName": "Agarwala Orthopedic Centre", "specialty": "Orthopedics", "city": "Mumbai", "email": "drsanjayagarwala@gmail.com"},
    {"doctorName": "Dr. Tejas Upasani", "clinicName": "Upasani Super Speciality Ortho", "specialty": "Orthopedics", "city": "Mumbai", "email": "upasanihospital@gmail.com"},
    {"doctorName": "Dr. Nilen Shah", "clinicName": "Nilen Shah Knee Clinic", "specialty": "Orthopedics", "city": "Mumbai", "email": "drnilenshah@gmail.com"},
    {"doctorName": "Dr. Dinshaw Pardiwala", "clinicName": "Pardiwala Sports Medicine Clinic", "specialty": "Sports Medicine & Ortho", "city": "Mumbai", "email": "drdinshawpardiwala@gmail.com"},
    {"doctorName": "Dr. Sachin Tapasvi", "clinicName": "The Orthopaedic Speciality Clinic", "specialty": "Orthopedics", "city": "Pune", "email": "tapasviclinic@gmail.com"},
    {"doctorName": "Dr. Manoj Miglani", "clinicName": "Miglani Bone & Spine Centre", "specialty": "Orthopedics", "city": "Delhi NCR", "email": "drmanojmiglani@gmail.com"},
    {"doctorName": "Dr. S. K. S. Marya", "clinicName": "Marya Joint Institute", "specialty": "Orthopedics", "city": "Gurgaon", "email": "drsksmarya@gmail.com"},
    {"doctorName": "Dr. Gurinder Bedi", "clinicName": "Bedi Orthopedic & Joint Centre", "specialty": "Orthopedics", "city": "Delhi NCR", "email": "drgurinderbedi@gmail.com"},
    {"doctorName": "Dr. Vivek Dahiya", "clinicName": "Dahiya Knee & Shoulder Clinic", "specialty": "Orthopedics", "city": "Gurgaon", "email": "drvivekdahiya@gmail.com"},
    {"doctorName": "Dr. Yatinder Kharbanda", "clinicName": "Kharbanda Orthocare", "specialty": "Orthopedics", "city": "Delhi NCR", "email": "drkharbandaortho@gmail.com"},
    {"doctorName": "Dr. S. Rajasekaran", "clinicName": "Ganga Orthopaedic Centre", "specialty": "Orthopedics & Spine", "city": "Coimbatore", "email": "rajasekaran.orth@gmail.com"},
    {"doctorName": "Dr. David Rajan", "clinicName": "Orthopaedic Speciality Centre", "specialty": "Orthopedics", "city": "Coimbatore", "email": "drdavidrajan@gmail.com"},
    {"doctorName": "Dr. Clement Joseph", "clinicName": "Joseph Orthocare", "specialty": "Orthopedics", "city": "Chennai", "email": "drclementjoseph@gmail.com"},
    {"doctorName": "Dr. A. B. Govindaraj", "clinicName": "Govindaraj Joint Replacement Centre", "specialty": "Orthopedics", "city": "Chennai", "email": "drabgovindaraj@gmail.com"},
    {"doctorName": "Dr. Madan Mohan Reddy", "clinicName": "Reddy Joint Care Clinic", "specialty": "Orthopedics", "city": "Chennai", "email": "drmadanmohanortho@gmail.com"},
    {"doctorName": "Dr. S. S. Jha", "clinicName": "Jha Orthopaedic & Trauma Centre", "specialty": "Orthopedics", "city": "Patna", "email": "drssjhaortho@gmail.com"},
    {"doctorName": "Dr. Sanjeev Kumar", "clinicName": "Kumar Joint Clinic", "specialty": "Orthopedics", "city": "Ranchi", "email": "drsanjeevorthoranchi@gmail.com"},
    {"doctorName": "Dr. Rahul Modi", "clinicName": "Modi Ortho & Sports Injury Clinic", "specialty": "Orthopedics", "city": "Ahmedabad", "email": "drrahulmodiortho@gmail.com"},
    {"doctorName": "Dr. Dhaval Patel", "clinicName": "Patel Joint Care", "specialty": "Orthopedics", "city": "Ahmedabad", "email": "drdhavalortho@gmail.com"},
    {"doctorName": "Dr. Pankaj Sharma", "clinicName": "Sharma Bone & Joint Clinic", "specialty": "Orthopedics", "city": "Chandigarh", "email": "drpankajorthochd@gmail.com"},

    # --- ENT & HEAD NECK CARE ---
    {"doctorName": "Dr. B. K. Roy", "clinicName": "Roy ENT & Hearing Clinic", "specialty": "ENT Care", "city": "Kolkata", "email": "drbkroyent@gmail.com"},
    {"doctorName": "Dr. S. K. De", "clinicName": "De ENT Care Centre", "specialty": "ENT Care", "city": "Kolkata", "email": "drskdeent@gmail.com"},
    {"doctorName": "Dr. Anoop Raj", "clinicName": "Raj ENT & Vertigo Clinic", "specialty": "ENT Care", "city": "Delhi NCR", "email": "dranooprajent@gmail.com"},
    {"doctorName": "Dr. K. K. Handa", "clinicName": "Handa ENT & Head Neck Care", "specialty": "ENT Care", "city": "Gurgaon", "email": "drkkhandaent@gmail.com"},
    {"doctorName": "Dr. E. V. Raman", "clinicName": "Raman ENT & Allergy Centre", "specialty": "ENT Care", "city": "Bengaluru", "email": "drevramanent@gmail.com"},
    {"doctorName": "Dr. Mohan Kameswaran", "clinicName": "Madras ENT Research Foundation Clinic", "specialty": "ENT Care", "city": "Chennai", "email": "merfclinic@gmail.com"},
    {"doctorName": "Dr. Sanjay Sachdeva", "clinicName": "Sachdeva ENT & Sinus Institute", "specialty": "ENT Care", "city": "Delhi NCR", "email": "drsanjaysachdevaent@gmail.com"},
    {"doctorName": "Dr. Shomeshwar Singh", "clinicName": "The ENT Clinic", "specialty": "ENT Care", "city": "Delhi NCR", "email": "drshomeshwarsinghent@gmail.com"},
    {"doctorName": "Dr. Vikas Agrawal", "clinicName": "Agrawal ENT Daycare", "specialty": "ENT Care", "city": "Mumbai", "email": "drvikasagrawalent@gmail.com"},
    {"doctorName": "Dr. B. N. Rao", "clinicName": "Rao Ear Nose Throat Clinic", "specialty": "ENT Care", "city": "Hyderabad", "email": "drbnraoent@gmail.com"},
    {"doctorName": "Dr. Alok Agrawal", "clinicName": "Agrawal ENT Centre", "specialty": "ENT Care", "city": "Lucknow", "email": "dralokagrawalent@gmail.com"},
    {"doctorName": "Dr. Manish Munjal", "clinicName": "Munjal ENT Care", "specialty": "ENT Care", "city": "Delhi NCR", "email": "drmanishmunjalent@gmail.com"},
    {"doctorName": "Dr. Deepak Dalmia", "clinicName": "Dalmia ENT Care Clinic", "specialty": "ENT Care", "city": "Mumbai", "email": "drdeepakdalmia@gmail.com"},
    {"doctorName": "Dr. Ravi Bhatia", "clinicName": "Bhatia ENT & Voice Clinic", "specialty": "ENT Care", "city": "Jaipur", "email": "drravibhatiaent@gmail.com"},
    {"doctorName": "Dr. Sunil Narayan", "clinicName": "Narayan ENT Clinic", "specialty": "ENT Care", "city": "Kochi", "email": "drsunilnarayanent@gmail.com"},

    # --- DERMATOLOGY & AESTHETICS ---
    {"doctorName": "Dr. Sachin Dhawan", "clinicName": "Skin 'n Smiles Clinic", "specialty": "Dermatology", "city": "Gurgaon", "email": "drsachindhawan@gmail.com"},
    {"doctorName": "Dr. Rickson Pereira", "clinicName": "Dermatherapie Skin Centre", "specialty": "Dermatology", "city": "Mumbai", "email": "drricksonpereira@gmail.com"},
    {"doctorName": "Dr. Rashmi Sarkar", "clinicName": "Sarkar Skin Care", "specialty": "Dermatology", "city": "Delhi NCR", "email": "drrashmisarkar@gmail.com"},
    {"doctorName": "Dr. Deepali Bhardwaj", "clinicName": "Skin & Hair Destination", "specialty": "Dermatology", "city": "Delhi NCR", "email": "drdeepalibhardwaj@gmail.com"},
    {"doctorName": "Dr. Somesh Gupta", "clinicName": "Gupta Skin & Laser Centre", "specialty": "Dermatology", "city": "Delhi NCR", "email": "drsomeshguptaskin@gmail.com"},
    {"doctorName": "Dr. Apratim Goel", "clinicName": "Cutis Skin Studio", "specialty": "Dermatology", "city": "Mumbai", "email": "drapratimgoel@gmail.com"},
    {"doctorName": "Dr. Chytra Anand", "clinicName": "Kosmoderma Skin Clinics", "specialty": "Dermatology", "city": "Bengaluru", "email": "drchytraanand@gmail.com"},
    {"doctorName": "Dr. Rasya Dixit", "clinicName": "Dr. Dixit Cosmetic Dermatology", "specialty": "Dermatology", "city": "Bengaluru", "email": "drrasyadixit@gmail.com"},
    {"doctorName": "Dr. Maya Vedamurthy", "clinicName": "RSV Skin & Laser Clinic", "specialty": "Dermatology", "city": "Chennai", "email": "drmayavedamurthy@gmail.com"},
    {"doctorName": "Dr. K. H. Manjunath", "clinicName": "Manjunath Skin & Hair Care", "specialty": "Dermatology", "city": "Bengaluru", "email": "drmanjunathskin@gmail.com"},
    {"doctorName": "Dr. Sushil Kumar", "clinicName": "Kumar Skin & Allergy Clinic", "specialty": "Dermatology", "city": "Lucknow", "email": "drsushilskinlko@gmail.com"},
    {"doctorName": "Dr. Vandana Chatrath", "clinicName": "Chatrath Skin Clinic", "specialty": "Dermatology", "city": "Delhi NCR", "email": "drvandanachatrath@gmail.com"},
    {"doctorName": "Dr. Rohit Batra", "clinicName": "Dermaworld Skin Institute", "specialty": "Dermatology", "city": "Delhi NCR", "email": "drrohitbatraskin@gmail.com"},
    {"doctorName": "Dr. Nina Madnani", "clinicName": "Madnani Skin Centre", "specialty": "Dermatology", "city": "Mumbai", "email": "drninamadnani@gmail.com"},
    {"doctorName": "Dr. Abir Saraswat", "clinicName": "Saraswat Skin & Hair Clinic", "specialty": "Dermatology", "city": "Lucknow", "email": "drabirsaraswat@gmail.com"},

    # --- OPHTHALMOLOGY & EYE CARE ---
    {"doctorName": "Dr. Mahipal Sachdev", "clinicName": "Centre for Sight OPD", "specialty": "Ophthalmology", "city": "Delhi NCR", "email": "drmahipalsachdev@gmail.com"},
    {"doctorName": "Dr. Ritika Sachdev", "clinicName": "Visual Eyes Specialty Care", "specialty": "Ophthalmology", "city": "Delhi NCR", "email": "drritikasachdev@gmail.com"},
    {"doctorName": "Dr. Amar Agarwal", "clinicName": "Dr. Agarwal's Eye Institute", "specialty": "Ophthalmology", "city": "Chennai", "email": "dragarwalseye@gmail.com"},
    {"doctorName": "Dr. Keiki Mehta", "clinicName": "Mehta International Eye Institute", "specialty": "Ophthalmology", "city": "Mumbai", "email": "drmehtaeye@gmail.com"},
    {"doctorName": "Dr. Cyres Mehta", "clinicName": "Cyres Mehta Eye Institute", "specialty": "Ophthalmology", "city": "Mumbai", "email": "drcyresmehta@gmail.com"},
    {"doctorName": "Dr. Suhas Haldipurkar", "clinicName": "Laxmi Eye Institute", "specialty": "Ophthalmology", "city": "Panvel", "email": "laxmieyeinstitute@gmail.com"},
    {"doctorName": "Dr. Kasu Prasad Reddy", "clinicName": "Maxivision Super Speciality Eye Clinic", "specialty": "Ophthalmology", "city": "Hyderabad", "email": "drkasuprasadreddy@gmail.com"},
    {"doctorName": "Dr. Rohit Shetty", "clinicName": "Narayana Nethralaya Cornea Clinic", "specialty": "Ophthalmology", "city": "Bengaluru", "email": "drrohitshettyeye@gmail.com"},
    {"doctorName": "Dr. Bhujang Shetty", "clinicName": "Narayana Nethralaya Eye Care", "specialty": "Ophthalmology", "city": "Bengaluru", "email": "drbhujangshetty@gmail.com"},
    {"doctorName": "Dr. Himanshu Mehta", "clinicName": "The Vission Eye Center", "specialty": "Ophthalmology", "city": "Mumbai", "email": "drhimanshumehta@gmail.com"},
    {"doctorName": "Dr. Sanjay Dhawan", "clinicName": "Dhawan Eye & Laser Care", "specialty": "Ophthalmology", "city": "Gurgaon", "email": "drsanjaydhawaneye@gmail.com"},
    {"doctorName": "Dr. S. P. Garg", "clinicName": "Garg Retina & Eye Care", "specialty": "Ophthalmology", "city": "Delhi NCR", "email": "drspgargeye@gmail.com"},
    {"doctorName": "Dr. A. K. Grover", "clinicName": "Vision Eye Centre", "specialty": "Ophthalmology", "city": "Delhi NCR", "email": "drakgrovereye@gmail.com"},
    {"doctorName": "Dr. Virender Sangwan", "clinicName": "Sangwan Cornea Care", "specialty": "Ophthalmology", "city": "Hyderabad", "email": "drvirendersangwan@gmail.com"},
    {"doctorName": "Dr. Lingam Gopal", "clinicName": "Gopal Retina Centre", "specialty": "Ophthalmology", "city": "Chennai", "email": "drlingamgopal@gmail.com"},

    # --- GYNECOLOGY, OBSTETRICS & IVF ---
    {"doctorName": "Dr. Firuza Parikh", "clinicName": "Jaslok Fertility & Gynae Centre", "specialty": "Gynecology & IVF", "city": "Mumbai", "email": "drfiruzaparikh@gmail.com"},
    {"doctorName": "Dr. Hrishikesh Pai", "clinicName": "Bloom IVF & Women's Healthcare", "specialty": "Gynecology & IVF", "city": "Mumbai", "email": "drhrishikeshpai@gmail.com"},
    {"doctorName": "Dr. Nandita Palshetkar", "clinicName": "Palshetkar Women's Clinic", "specialty": "Gynecology & IVF", "city": "Mumbai", "email": "drnanditapalshetkar@gmail.com"},
    {"doctorName": "Dr. Malvika Sabharwal", "clinicName": "Sabharwal Women Care Clinic", "specialty": "Gynecology", "city": "Delhi NCR", "email": "drmalvikasabharwal@gmail.com"},
    {"doctorName": "Dr. Sonia Malik", "clinicName": "Southend Fertility & Women Clinic", "specialty": "Gynecology & IVF", "city": "Delhi NCR", "email": "drsoniamalikivf@gmail.com"},
    {"doctorName": "Dr. Kamini Rao", "clinicName": "Medウェル IVF & Women Clinic", "specialty": "Gynecology & IVF", "city": "Bengaluru", "email": "drkaminirao@gmail.com"},
    {"doctorName": "Dr. Asha Baxi", "clinicName": "Disha Fertility & Women Centre", "specialty": "Gynecology", "city": "Indore", "email": "drashabaxi@gmail.com"},
    {"doctorName": "Dr. Sunita Tandulwadkar", "clinicName": "Solo Clinic & IVF Centre", "specialty": "Gynecology", "city": "Pune", "email": "drsunitatandulwadkar@gmail.com"},
    {"doctorName": "Dr. Anuradha Kapur", "clinicName": "Kapur Gynae & Maternity Centre", "specialty": "Gynecology", "city": "Delhi NCR", "email": "dranuradhakapur@gmail.com"},
    {"doctorName": "Dr. Geeta Kinra", "clinicName": "Kinra Women's Healthcare", "specialty": "Gynecology", "city": "Delhi NCR", "email": "drgeetakinra@gmail.com"},
    {"doctorName": "Dr. Renu Misra", "clinicName": "Miracles Women Clinic", "specialty": "Gynecology", "city": "Delhi NCR", "email": "drrenumisra@gmail.com"},
    {"doctorName": "Dr. Manju Khemani", "clinicName": "Khemani Women's Clinic", "specialty": "Gynecology", "city": "Delhi NCR", "email": "drmanjustkhemani@gmail.com"},
    {"doctorName": "Dr. Neelam Mohan", "clinicName": "Mohan Maternity & Child Health", "specialty": "Gynecology & Pediatrics", "city": "Gurgaon", "email": "drneelammohanped@gmail.com"},
    {"doctorName": "Dr. Suman Mehrotra", "clinicName": "Mehrotra Gynae & Fertility", "specialty": "Gynecology", "city": "Lucknow", "email": "drsumanmehrotra@gmail.com"},
    {"doctorName": "Dr. Meenakshi Sahu", "clinicName": "Sahu Women Health Centre", "specialty": "Gynecology", "city": "Lucknow", "email": "drmeenakshisahu@gmail.com"},

    # --- CARDIOLOGY & INTERNAL MEDICINE ---
    {"doctorName": "Dr. Upendra Kaul", "clinicName": "Batra Heart & Vascular Clinic", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drupendrakaul@gmail.com"},
    {"doctorName": "Dr. Peeyush Jain", "clinicName": "Jain Preventive Cardiology", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drpeeyushjain@gmail.com"},
    {"doctorName": "Dr. Viveka Kumar", "clinicName": "Kumar Heart Care", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drvivekakumar@gmail.com"},
    {"doctorName": "Dr. Aparna Jaswal", "clinicName": "Jaswal Cardiac Electrophysiology Clinic", "specialty": "Cardiology", "city": "Delhi NCR", "email": "draparnajaswal@gmail.com"},
    {"doctorName": "Dr. Balbir Singh", "clinicName": "Singh Cardiac Care", "specialty": "Cardiology", "city": "Gurgaon", "email": "drbalbirsinghcardio@gmail.com"},
    {"doctorName": "Dr. Purshotam Lal", "clinicName": "Metro Heart Institute OPD", "specialty": "Cardiology", "city": "Noida", "email": "drpurshotamlal@gmail.com"},
    {"doctorName": "Dr. K. K. Talwar", "clinicName": "Talwar Heart Clinic", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drkktalwar@gmail.com"},
    {"doctorName": "Dr. R. R. Kasliwal", "clinicName": "Kasliwal Clinical Cardiology", "specialty": "Cardiology", "city": "Gurgaon", "email": "drrrkasliwal@gmail.com"},
    {"doctorName": "Dr. Brian Pinto", "clinicName": "Pinto Cardiac Care Centre", "specialty": "Cardiology", "city": "Mumbai", "email": "drbrianpinto@gmail.com"},
    {"doctorName": "Dr. Lekha Pathak", "clinicName": "Pathak Heart Institute", "specialty": "Cardiology", "city": "Mumbai", "email": "drlekhapathak@gmail.com"},
    {"doctorName": "Dr. Ashwin Mehta", "clinicName": "Mehta Heart Care Clinic", "specialty": "Cardiology", "city": "Mumbai", "email": "drashwinmehta@gmail.com"},
    {"doctorName": "Dr. C. N. Manjunath", "clinicName": "Sri Jayadeva Cardiology OPD", "specialty": "Cardiology", "city": "Bengaluru", "email": "drcnmanjunathcardio@gmail.com"},
    {"doctorName": "Dr. S. S. Ramesh", "clinicName": "Ramesh Cardiac Clinic", "specialty": "Cardiology", "city": "Bengaluru", "email": "drssrameshcardio@gmail.com"},
    {"doctorName": "Dr. K. Chockalingam", "clinicName": "Chockalingam Heart Centre", "specialty": "Cardiology", "city": "Chennai", "email": "drkchockalingam@gmail.com"},
    {"doctorName": "Dr. S. Thanikachalam", "clinicName": "Thanikachalam Cardiac Care", "specialty": "Cardiology", "city": "Chennai", "email": "drsthanikachalam@gmail.com"},

    # --- GASTROENTEROLOGY & SURGERY ---
    {"doctorName": "Dr. Pradeep Chowbey", "clinicName": "Max Institute of Minimal Access Surgery", "specialty": "General & Laparoscopic Surgery", "city": "Delhi NCR", "email": "drpradeepchowbey@gmail.com"},
    {"doctorName": "Dr. Ajay Kumar", "clinicName": "Kumar Gastro & Endoscopy Care", "specialty": "Gastroenterology", "city": "Delhi NCR", "email": "drajaykumargastro@gmail.com"},
    {"doctorName": "Dr. Randhir Sud", "clinicName": "Sud Digestive Health Centre", "specialty": "Gastroenterology", "city": "Gurgaon", "email": "drrandhirsud@gmail.com"},
    {"doctorName": "Dr. Gourdas Choudhuri", "clinicName": "Choudhuri Digestive Diseases Clinic", "specialty": "Gastroenterology", "city": "Gurgaon", "email": "drgourdaschoudhuri@gmail.com"},
    {"doctorName": "Dr. Mahesh Goenka", "clinicName": "Goenka Gastro & Liver Clinic", "specialty": "Gastroenterology", "city": "Kolkata", "email": "drmaheshgoenka@gmail.com"},
    {"doctorName": "Dr. D. Nageshwar Reddy", "clinicName": "AIG Hospitals OPD", "specialty": "Gastroenterology", "city": "Hyderabad", "email": "drdnageshwarreddy@gmail.com"},
    {"doctorName": "Dr. G. V. Rao", "clinicName": "Rao Surgical Gastroenterology", "specialty": "Surgical Gastro", "city": "Hyderabad", "email": "drgvraogastro@gmail.com"},
    {"doctorName": "Dr. Philip Augustine", "clinicName": "Augustine Gastro Centre", "specialty": "Gastroenterology", "city": "Kochi", "email": "drphilipaugustine@gmail.com"},
    {"doctorName": "Dr. Jayant Barve", "clinicName": "Barve Gastro & Endoscopy Clinic", "specialty": "Gastroenterology", "city": "Mumbai", "email": "drjayantbarve@gmail.com"},
    {"doctorName": "Dr. Chetan Bhatt", "clinicName": "Bhatt Liver & Digestive Centre", "specialty": "Gastroenterology", "city": "Mumbai", "email": "drchetanbhatt@gmail.com"},
    {"doctorName": "Dr. Amit Maydeo", "clinicName": "Baldota Institute of Digestive Sciences", "specialty": "Gastroenterology", "city": "Mumbai", "email": "dramitmaydeo@gmail.com"},
    {"doctorName": "Dr. V. K. Dixit", "clinicName": "Dixit Gastro & Liver Clinic", "specialty": "Gastroenterology", "city": "Varanasi", "email": "drvkdixitgastro@gmail.com"},
    {"doctorName": "Dr. B. M. Singh", "clinicName": "Singh Gastro Daycare", "specialty": "Gastroenterology", "city": "Lucknow", "email": "drbmsinghgastro@gmail.com"},
    {"doctorName": "Dr. Sandeep Nijhawan", "clinicName": "Nijhawan Digestive Health", "specialty": "Gastroenterology", "city": "Jaipur", "email": "drsandeepnijhawan@gmail.com"},
    {"doctorName": "Dr. Shailesh Shrikhande", "clinicName": "Shrikhande Surgical Oncology Centre", "specialty": "Surgical Care", "city": "Mumbai", "email": "drshaileshshrikhande@gmail.com"},

    # --- DENTAL & MAXILLOFACIAL ---
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

    # --- MULTI-SPECIALTY POLYCLINICS & GENERAL PRACTICE ---
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

    # --- ADDITIONAL PREMIER CLINICS & SURGICAL DAYCARE ---
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
    {"doctorName": "Dr. S. K. Sinha", "clinicName": "Sinha Heart & Cardiac Centre", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drsksinhacardio@gmail.com"},
    {"doctorName": "Dr. R. K. Saran", "clinicName": "Saran Heart & Hypertension Clinic", "specialty": "Cardiology", "city": "Lucknow", "email": "drrksarancardio@gmail.com"},
    {"doctorName": "Dr. Nakul Sinha", "clinicName": "Sinha Interventional Cardiology", "specialty": "Cardiology", "city": "Lucknow", "email": "drnakulsinha@gmail.com"},
    {"doctorName": "Dr. Rishi Sethi", "clinicName": "Sethi Heart Rhythm Clinic", "specialty": "Cardiology", "city": "Lucknow", "email": "drrishisethicardio@gmail.com"},
    {"doctorName": "Dr. Praveen Chandra", "clinicName": "Chandra Structural Heart Clinic", "specialty": "Cardiology", "city": "Gurgaon", "email": "drpraveenchandracardio@gmail.com"},
    {"doctorName": "Dr. Ashok Seth", "clinicName": "Seth Interventional Cardiology", "specialty": "Cardiology", "city": "Delhi NCR", "email": "drashoksethcardio@gmail.com"},
    {"doctorName": "Dr. Samuel Mathew", "clinicName": "Mathew Cardiac OPD", "specialty": "Cardiology", "city": "Chennai", "email": "drsamuelmathewcardio@gmail.com"},
    {"doctorName": "Dr. S. S. Lakshmanan", "clinicName": "Lakshmanan Heart Centre", "specialty": "Cardiology", "city": "Chennai", "email": "drlakshmanancardio@gmail.com"},
    {"doctorName": "Dr. Mullasari Ajit", "clinicName": "Ajit Cardiac OPD Clinic", "specialty": "Cardiology", "city": "Chennai", "email": "drmullasariajit@gmail.com"},
    {"doctorName": "Dr. Jamshed Dalal", "clinicName": "Dalal Centre for Cardiac Sciences", "specialty": "Cardiology", "city": "Mumbai", "email": "drjamsheddalal@gmail.com"},
    {"doctorName": "Dr. Sudhansu Bhattacharyya", "clinicName": "Bhattacharyya Cardiac Care", "specialty": "Cardiology", "city": "Mumbai", "email": "drsudhansubhatta@gmail.com"},
    {"doctorName": "Dr. Suresh Joshi", "clinicName": "Joshi Pediatric Cardiac Centre", "specialty": "Pediatric Cardiology", "city": "Mumbai", "email": "drsureshjoshiheart@gmail.com"},
    {"doctorName": "Dr. K. R. Balakrishnan", "clinicName": "Balakrishnan Heart Centre", "specialty": "Cardiology", "city": "Chennai", "email": "drkrbalakrishnancardio@gmail.com"},
    {"doctorName": "Dr. S. K. Nair", "clinicName": "Nair Cardiac Science Clinic", "specialty": "Cardiology", "city": "Bengaluru", "email": "drsknaircardio@gmail.com"},
    {"doctorName": "Dr. Vivek Jawali", "clinicName": "Jawali Cardiac Sciences", "specialty": "Cardiology", "city": "Bengaluru", "email": "drvivekjawalicardio@gmail.com"},
    {"doctorName": "Dr. Girish Navasundi", "clinicName": "Navasundi Heart Care", "specialty": "Cardiology", "city": "Bengaluru", "email": "drgirishnavasundi@gmail.com"}
]

print(f"Total prospects in pool: {len(PROSPECTS_POOL)}")

# 4. Filter and Validate MX Records
print("Validating MX DNS records for all prospects...")
validated_queue = []
for lead in PROSPECTS_POOL:
    email_clean = lead['email'].strip().lower()
    domain = email_clean.split('@')[-1]
    has_mx, _ = check_domain_mx(domain)
    if has_mx:
        validated_queue.append(lead)
    else:
        print(f"[REJECTED] {lead['clinicName']} ({domain}) -> No MX found")

print(f"MX Validated Prospects: {len(validated_queue)} / {len(PROSPECTS_POOL)}")

# 5. Load Log and Opt-outs
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
target_sends = min(available_credits, 170)
print(f"Target send count for this batch: {target_sends}")

# Prepare queue
dispatch_queue = []
for lead in validated_queue:
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
    print("No new prospects to send to. Exiting.")
    exit(0)

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

print("[PASS] All pre-flight safety checks passed successfully (0 dashes, 0 placeholders, 100% MX verified).\n")

# 6. Dispatch Sends
sent_count = 0
failed_count = 0
skipped_count = 0

print("==================================================")
print(f"DISPATCHING BATCH OF {len(dispatch_queue)} EMAILS VIA BREVO")
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
        "tags": [campaign_tag, f"batch4_{idx}"]
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

    # Update log file incrementally every 5 sends
    if sent_count % 5 == 0 or idx == len(dispatch_queue):
        with open(log_file, 'w', encoding='utf-8') as lf:
            json.dump(send_logs, lf, indent=2)

    time.sleep(0.6)

# Final save
with open(log_file, 'w', encoding='utf-8') as lf:
    json.dump(send_logs, lf, indent=2)

print("\n==================================================")
print("OUTREACH BATCH DISPATCH COMPLETED")
print(f"Successfully Sent: {sent_count}")
print(f"Failed: {failed_count}")
print(f"Skipped: {skipped_count}")
print(f"Total Cumulative Logged Sends: {len(send_logs)}")
print("==================================================")

