# SwasthAI B2B Cold Email Acquisition System (Brevo Engine)

**Official Sending Infrastructure:** Brevo (Sendinblue) Transactional REST API  
**Website:** [https://swasthai-three.vercel.app/](https://swasthai-three.vercel.app/)  
**Verified Sender:** `swasthai.founder@gmail.com`  
**Sender Name:** Sankalp Mishra, Founder @ SwasthAI  
**Target Audience:** Independent & Small/Medium Clinic Owners, Doctors, OPD Managers across Indian Metros & Tier-2/3 Cities  

---

## 1. System Architecture & Safeguards

```
[Researched Public Clinic Leads (100)]
                 │
                 ▼
[Source & Domain Verification Gate]
  • 100% Publicly Listed Contact URLs
  • Zero Guessed / Zero Placeholder Emails
  • Direct Doctor / Decision Maker Association
                 │
                 ▼
[Master Template & Zero-Dash Enforcement]
  • 100-140 words, mobile-friendly
  • Zero dashes / em-dashes (commas and periods only)
  • Single CTA: 2-minute video walkthrough
  • Strict Opt-Out Suppression Notice
                 │
                 ▼
[Brevo Transactional API Engine]
  • Server-side API key protection (BREVO_API_KEY)
  • Verified Reply-To (swasthai.founder@gmail.com)
  • Daily Send Limit: Max 10 cold emails/day
  • Rate Limiting: 2-10 second interval between sends
  • Duplicate Prevention via normalized email check
                 │
                 ▼
[Multi-Channel Attribution & Audit]
  • Timestamped Brevo Message ID logging
  • UTM tracking (email → website → demo → trial)
  • Admin Dashboard at /admin/outreach
```

---

## 2. Environment Variables

Expected in `website/.env.local`:
```env
BREVO_API_KEY=xkeysib-xxxxxxxxxxxxxxxxxxxx-xxxxxxxx
BREVO_SENDER_EMAIL=swasthai.founder@gmail.com
BREVO_SENDER_NAME="Sankalp Mishra"
```

---

## 3. Staged Sending Protocol

1. **Test Phase:**
   * Single test send to `swasthai.founder@gmail.com` with subject `[TEST] <Subject>`.
   * Real sample lead parameters filled (Dr. Ashish Ranade / Strong Bones Clinic).
   * Verifies Brevo delivery, format, HTML rendering, and message ID capture.
   * **Requires explicit user approval before stage 1.**

2. **Stage 1 (5 Verified Prospects):**
   * Top 5 high-priority clinics (Pune, Lucknow, Noida, Mumbai).
   * Verify open rates, bounce rate ($0\%$), and early responses.

3. **Stage 2 (10 Verified Prospects):**
   * Next 10 clinics across Orthopedics, Pediatrics, ENT, and Dermatology.

4. **Stage 3 (25 Verified Prospects):**
   * Scaled staged delivery within the 10/day Brevo rate limit.

---

## 4. Unsubscribe & Reply Handling

* **Permanent Opt-Out List:** Stored in `cold-email-opt-outs.json`. If any recipient responds with "no", "stop", or "unsubscribe", their email is permanently blocked.
* **Reply Tracking:** Inbound responses are classified as `INTERESTED`, `SEND_DEMO`, `PRICE`, `TRIAL`, `NOT_INTERESTED`, `BUSY`, or `OPT_OUT`.
