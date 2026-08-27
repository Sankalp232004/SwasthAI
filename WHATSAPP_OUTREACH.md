# SwasthAI WhatsApp Outreach System — Production Architecture & Operations Manual

This document is the master technical and operational guide for SwasthAI's **Production WhatsApp Outreach Engine**. It covers Meta Business Cloud API configuration, message templates, safety gates, CRM storage, CLI workflows, follow-up automations, opt-out management, and troubleshooting.

---

## 1. 🏗️ System Overview & Architecture

SwasthAI's WhatsApp Outreach Engine is a **high-precision, compliance-first, doctor-friendly communication platform** built directly into the SwasthAI ecosystem.

```
┌───────────────────────────────────────────────────────────────────────┐
│                      SWASTHAI OUTREACH PIPELINE                       │
└───────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────┐
│ 1. Prospect Ingestion   │──▶│ 2. Message Generation    │──▶│ 3. 14-Point Quality Gate │
│ (E.164 Normalization)   │   │ (Specialty + Tone Engine)│   │ (Placeholder & Hype Scan)│
└─────────────────────────┘   └──────────────────────────┘   └──────────────────────────┘
                                                                           │
                                                                           ▼
┌─────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────┐
│ 6. Response & Objection │◀──│ 5. Meta Cloud API Send   │◀──│ 4. Explicit Approval     │
│ Handling (Smart Playbook│   │ (Template / 24h Session) │   │ (CLI Command: SEND <ph>) │
└─────────────────────────┘   └──────────────────────────┘   └──────────────────────────┘
```

---

## 2. 🔑 Environment Variables & Security

All credentials must be stored in `.env.local` (server-side only, never committed to Git).

### Required Environment Variables:
```env
# Meta WhatsApp Business Platform / Cloud API Credentials
WHATSAPP_ACCESS_TOKEN=EAAG...your_meta_system_user_token_here
WHATSAPP_PHONE_NUMBER_ID=106294...your_phone_number_id_here
WHATSAPP_BUSINESS_ACCOUNT_ID=104820...your_waba_id_here
WHATSAPP_API_VERSION=v20.0

# Webhook Handshake Security Token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=swasthai_secure_webhook_token_2026

# Sandbox / Safety Testing (Directs test messages exclusively to founder)
WHATSAPP_TEST_NUMBER=+919140721395

# Daily Outreach Limit (Asia/Kolkata timezone quota)
WHATSAPP_DAILY_LIMIT=10
```

> [!IMPORTANT]
> Never hardcode or commit tokens to GitHub. The `.gitignore` file is pre-configured to strictly ignore all `.env` and `.env.local` files.

---

## 3. 🛠️ Meta Business Platform Setup Guide

### Step 1: Create Meta App
1. Go to [Meta for Developers](https://developers.facebook.com/) and create a **Business App**.
2. Add the **WhatsApp** product to your application.
3. Obtain your **Phone Number ID**, **WhatsApp Business Account ID (WABA)**, and a **System User Access Token** with `whatsapp_business_messaging` permissions.

### Step 2: Register Official Meta Template
In your Meta WhatsApp Business Manager (Message Templates), submit the master template:

* **Template Name:** `swasthai_clinic_outreach_v1`
* **Category:** `UTILITY` (or `MARKETING`)
* **Language:** `English (en_US)`
* **Body:**
  ```text
  Hi Dr. {{1}},

  I came across {{2}} and wanted to ask how your team currently handles walk-in patients during busy OPD hours.

  I’m building SwasthAI, a simple system that collects a few patient inputs via QR and gives the clinic a recommended queue priority, while keeping the doctor in full control.

  Would you like me to send you a 2-minute demo?

  Sankalp
  Founder, SwasthAI
  ```
* **Variables:**
  - `{{1}}`: Doctor Name (e.g. `Ranade`)
  - `{{2}}`: Clinic Name & City (e.g. `Strong Bones Clinic in Pune`)

---

## 4. 🌐 Webhook Configuration

SwasthAI provides a native Next.js webhook route at:  
`https://swasthai-three.vercel.app/api/whatsapp/webhook`

### Configuration in Meta Developer Portal:
1. **Callback URL:** `https://swasthai-three.vercel.app/api/whatsapp/webhook`
2. **Verify Token:** Same value as `WHATSAPP_WEBHOOK_VERIFY_TOKEN` (e.g. `swasthai_secure_webhook_token_2026`)
3. **Webhook Subscriptions:** Subscribe to `messages` (inbound replies) and `message_deliveries` (status updates).

---

## 5. 🛡️ 14-Point Final Quality Gate

Before any message can be dispatched, the engine verifies 14 non-negotiable quality checks:

| Check # | Verification Rule | Failure Action |
| :---: | :--- | :--- |
| **01** | Valid E.164 Indian mobile format (`+91XXXXXXXXXX`) | ⛔ Blocks send |
| **02** | Recipient is **NOT** on the permanent opt-out registry | ⛔ Blocks send |
| **03** | Recipient was **NOT** contacted within the last 3 days | ⛔ Blocks send (Duplicate protection) |
| **04** | **Zero Placeholders:** `[Doctor Name]`, `{{1}}`, `{name}`, `<name>` | ⛔ Blocks send (PLACEHOLDER_SCAN) |
| **05** | **Zero Banned Hype Words:** "revolutionary", "game-changing", "cutting-edge", "seamless" | ⛔ Blocks send |
| **06** | **Zero Medical Claims:** No claims of diagnosis, cure, or replacing clinical judgment | ⛔ Blocks send |
| **07** | **Word Count Bounds:** Target 70–120 words (Strict maximum: 150 words) | ⛔ Blocks send |
| **08** | **Emoji Count:** Maximum 2 emojis allowed | ⛔ Blocks send |
| **09** | **Minimum Quality Score:** ≥ 70 / 100 on the automated scoring algorithm | ⛔ Blocks send |
| **10** | **Daily Quota Allowance:** Today's sends (IST) < `WHATSAPP_DAILY_LIMIT` | ⛔ Blocks send |
| **11** | Clean doctor & clinic name sanitization (removes double prefixes like `Dr. Dr.`) | Auto-sanitizes |
| **12** | Specialty-aligned operational problem included | Enforced in template |
| **13** | Low-friction 2-minute demo CTA included | Enforced in template |
| **14** | **Explicit User Approval:** Requires direct execution of `SEND <phone>` command | Never auto-sends |

---

## 6. 💻 Complete CLI Command Reference

Execute all operations from your terminal inside the `website/` directory:

### 1. Preview a Single Prospect
```bash
npx ts-node scripts/whatsapp-outreach.ts /whatsapp +919822038038
```
*Outputs: Complete prospect profile, exact rendered message, 100-point quality score, spam risk, duplicate check, and send readiness status.*

### 2. Send Approved Message (Explicit Confirmation)
```bash
npx ts-node scripts/whatsapp-outreach.ts SEND +919822038038
```
*Dispatches message via Meta Cloud API, increments daily quota, schedules Follow-up 1 in 3 days, and records full audit log.*

### 3. View Batch Queue of Ready Prospects
```bash
npx ts-node scripts/whatsapp-outreach.ts /whatsapp-batch
```
*Lists all uncontacted prospects in CRM with quality scores and one-click send commands.*

### 4. View Outreach Analytics & Daily Quotas
```bash
npx ts-node scripts/whatsapp-outreach.ts /whatsapp-status
```
*Displays today's send count, remaining quota, reply rates, demos booked, active trials, and objection breakdown.*

### 5. Check Follow-Ups Due
```bash
npx ts-node scripts/whatsapp-outreach.ts /followups
```
*Lists all scheduled follow-ups due today (Step 1 at Day 3/4, Step 2 at Day 8/9).*

### 6. View CRM Contacts
```bash
npx ts-node scripts/whatsapp-outreach.ts /contacts
```

### 7. Permanently Opt-Out a Number
```bash
npx ts-node scripts/whatsapp-outreach.ts /optout +919822038038 "Doctor replied not interested"
```
*Blocks all future outreach immediately.*

### 8. Admin Resume Contact (Explicit Override)
```bash
npx ts-node scripts/whatsapp-outreach.ts /resume +919822038038
```

### 9. Get Objection Handling Response
```bash
npx ts-node scripts/whatsapp-outreach.ts /objection +919822038038 PRICE
```
*(Supports: `PRICE`, `DEMO_REQUEST`, `TRIAL`, `ALREADY_HAVE_SYSTEM`, `TRUST`, `TECHNICAL`, `SEND_DETAILS`, `BUSY`)*

### 10. Import 50 Verified Clinic Leads
```bash
npx ts-node scripts/whatsapp-outreach.ts /import-leads
```
*Populates the WhatsApp CRM store from `cold_email_leads.md`.*

### 11. Run Full Dry-Run
```bash
npx ts-node scripts/whatsapp-outreach.ts /dry-run +919822038038
```

### 12. Run Founder Test Send
```bash
npx ts-node scripts/whatsapp-outreach.ts /test
```

---

## 7. 📊 Web Admin Dashboard

Access the interactive web dashboard locally or in production at:  
`https://swasthai-three.vercel.app/admin/whatsapp` (Local: `http://localhost:3000/admin/whatsapp`)

**Features:**
- Live pipeline tracker (`Prospect` ➔ `Outreach` ➔ `Conversation` ➔ `Trial` ➔ `Paid`)
- Real-time WhatsApp Message Sandbox with live quality score meter
- One-click copy Objection Playbook
- Audit logging & daily quota tracking.
