/**
 * SwasthAI Master Research-Driven Cold Acquisition Template Engine
 * =================================================================
 * Structured around 5 Core Campaign Angles:
 * - Campaign 1: The queue starts after registration (ABDM 25 Crore milestone)
 * - Campaign 2: Who goes first? (Walk-in triage and clinical urgency)
 * - Campaign 3: The next OPD bottleneck (Polyclinic and multi-doctor pacing)
 * - Campaign 4: The receptionist's decision (Front-desk triage stress)
 * - Campaign 5: Digital clinic, manual queue (Online booking vs physical queue)
 * 
 * Strict Formatting Rules:
 * - ZERO DASHES in body text (no em-dash, no en-dash, no hyphen in sentences).
 * - Founder tone (Sankalp Mishra).
 * - Single low-pressure CTA.
 * - Website URL: https://swasthai-three.vercel.app/
 * - Plain text and clean personal HTML.
 */

export type CampaignKey = 
  | 'campaign_1_queue_after_registration'
  | 'campaign_2_who_goes_first'
  | 'campaign_3_next_opd_bottleneck'
  | 'campaign_4_receptionist_decision'
  | 'campaign_5_digital_clinic_manual_queue';

export interface TemplateParams {
  doctorName: string;
  clinicName: string;
  specialty: string;
  city: string;
  campaign: CampaignKey;
  verifiedObservation?: string;
}

export function generateSubjectVariants(campaign: CampaignKey, clinicName: string): {
  A: string;
  B: string;
  C: string;
  D: string;
  E: string;
} {
  switch (campaign) {
    case 'campaign_1_queue_after_registration':
      return {
        A: 'The queue starts after registration',
        B: 'What happens after registration?',
        C: `OPD queue flow at ${clinicName}`,
        D: 'Beyond digital registration',
        E: 'Post registration waiting times'
      };

    case 'campaign_2_who_goes_first':
      return {
        A: 'Who goes first?',
        B: `Handling acute walk ins at ${clinicName}`,
        C: 'Prioritizing patients in busy OPD sessions',
        D: 'Walk ins versus scheduled appointments',
        E: 'Queue order during peak hours'
      };

    case 'campaign_3_next_opd_bottleneck':
      return {
        A: 'The next OPD bottleneck',
        B: 'Managing clinic patient flow',
        C: 'When the waiting room fills up',
        D: `Consultation pacing at ${clinicName}`,
        E: 'OPD operations beyond scheduling'
      };

    case 'campaign_4_receptionist_decision':
      return {
        A: "The receptionist's decision",
        B: `Front desk triage at ${clinicName}`,
        C: 'Helping reception manage the queue',
        D: 'When patients ask who is next',
        E: 'Objective queue intake for clinics'
      };

    case 'campaign_5_digital_clinic_manual_queue':
      return {
        A: 'Digital clinic, manual queue',
        B: 'Modernizing the OPD waiting room',
        C: `Beyond token numbers at ${clinicName}`,
        D: 'Clinical priority versus arrival time',
        E: 'Organizing the physical queue'
      };
  }
}

export function renderEmail(params: TemplateParams): {
  subject: string;
  textContent: string;
  htmlContent: string;
} {
  const { doctorName, clinicName, campaign, verifiedObservation } = params;
  const obs = verifiedObservation || 'your clinic operates high volume daily consultation sessions';
  const subjects = generateSubjectVariants(campaign, clinicName);
  const selectedSubject = subjects.A;

  let textContent = '';

  switch (campaign) {
    case 'campaign_1_queue_after_registration':
      textContent = `Dr. ${doctorName},

India has now crossed 25 crore digital OPD registrations through ABDM's Scan and Register service.

That made me think about a slightly different problem.

If registration takes only a few minutes but patients still spend a long time waiting to see the doctor, the bottleneck has simply moved.

At ${clinicName}, I noticed ${obs}.

It made me wonder how your team handles one particular situation: when a new patient arrives with a complaint that may deserve attention before patients who are already waiting.

That is the small problem I am building SwasthAI around.

Patients answer a few structured questions after scanning a QR code. SwasthAI creates a recommended priority order for the doctor to review, and the doctor can change it whenever needed.

I am looking for a few clinics to try this with a real OPD workflow.

Can I send you the 2 minute version?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up.`;
      break;

    case 'campaign_2_who_goes_first':
      textContent = `Dr. ${doctorName},

When five patients are already waiting in the clinic, what happens when a new walk in arrives with severe discomfort?

In most outpatient settings, reception staff either rely strictly on arrival time or make an informal guess about who needs to go in first.

At ${clinicName}, I noticed ${obs}.

That made me think about how your team balances fairness to waiting patients with the clinical urgency of acute arrivals.

I am building SwasthAI to help doctors organize this intake.

Patients scan a QR code on arrival and answer a few short, structured questions. SwasthAI provides a recommended priority order for your review, and you can change the sequence whenever you want.

We are testing this with a small group of outpatient practices.

Would you be open to seeing a 2 minute walkthrough?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up.`;
      break;

    case 'campaign_3_next_opd_bottleneck':
      textContent = `Dr. ${doctorName},

Many clinics have successfully streamlined appointment scheduling, but the waiting room often remains crowded.

When multiple consultations run simultaneously, patient flow inside the clinic quickly becomes the next operational bottleneck.

At ${clinicName}, I noticed ${obs}.

It made me curious how your practice manages queue flow when some consultations take fifteen minutes while other patients only need a brief review.

That is why I am building SwasthAI.

Arriving patients scan a QR code and answer structured intake questions. SwasthAI presents a recommended priority order on your screen, allowing you to review and adjust the sequence at any time.

I am currently working with a few clinics to refine this workflow.

Can I share a 2 minute overview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up.`;
      break;

    case 'campaign_4_receptionist_decision':
      textContent = `Dr. ${doctorName},

In most private practices, the front desk is put in an uncomfortable position.

When a walk in looks uncomfortable, the receptionist has to decide whether to disrupt the queue without having clinical tools to evaluate the situation.

At ${clinicName}, I noticed ${obs}.

It made me wonder how your front desk currently determines which patients need faster doctor attention during busy hours.

I built SwasthAI to make this intake clear and structured.

Patients scan a counter QR code and answer a few simple questions. SwasthAI generates a recommended priority order on the doctor screen, while the doctor retains complete control over the final queue.

We are looking for a few practices to try this in daily OPD.

Would you be interested in a 2 minute preview?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up.`;
      break;

    case 'campaign_5_digital_clinic_manual_queue':
      textContent = `Dr. ${doctorName},

Most modern clinics now use digital billing and electronic appointments, but patient sequencing in the waiting room is still handled on a first come first served basis.

Clock arrival works for cinema seats, but healthcare visits often have varying levels of urgency.

At ${clinicName}, I noticed ${obs}.

It made me wonder how your team handles cases where an arriving patient might benefit from earlier review than someone who booked an earlier slot.

I am building SwasthAI to solve this specific gap.

Patients scan a QR code upon arrival and answer brief intake questions. SwasthAI provides a recommended queue order for the doctor to review, with full ability to override anytime.

I am looking for a few forward thinking clinics to test this in practice.

Can I send you a 2 minute screen recording?

Sankalp Mishra
Founder, SwasthAI
https://swasthai-three.vercel.app/

If you would rather not receive emails from me, just reply "no" and I will not follow up.`;
      break;
  }

  const htmlParagraphs = textContent
    .split('\n\n')
    .filter(p => p.trim())
    .map(p => {
      if (p.includes('https://swasthai-three.vercel.app/')) {
        const parts = p.split('https://swasthai-three.vercel.app/');
        return `<p style="margin: 0 0 16px 0;">${parts[0]}<a href="https://swasthai-three.vercel.app/" style="color: #008080; text-decoration: underline;">https://swasthai-three.vercel.app/</a>${parts[1] || ''}</p>`;
      }
      return `<p style="margin: 0 0 16px 0;">${p.replace(/\n/g, '<br>')}</p>`;
    })
    .join('');

  const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #222222; background-color: #ffffff; margin: 0; padding: 20px 0;">
  <div style="max-width: 600px; margin: 0 auto; padding: 0 20px;">
    ${htmlParagraphs}
  </div>
</body>
</html>`;

  return {
    subject: selectedSubject,
    textContent,
    htmlContent
  };
}

export function generateEmailContent(params: {
  doctorName: string;
  clinicName: string;
  specialty?: string;
  city?: string;
  campaignHook?: string;
  campaign?: CampaignKey;
  verifiedObservation?: string;
}): {
  subject: string;
  plainText: string;
  html: string;
} {
  const campaign = params.campaign || 'campaign_4_receptionist_decision';
  const rendered = renderEmail({
    doctorName: params.doctorName,
    clinicName: params.clinicName,
    specialty: params.specialty || 'General Practice',
    city: params.city || 'India',
    campaign: campaign,
    verifiedObservation: params.verifiedObservation || params.campaignHook
  });

  return {
    subject: rendered.subject,
    plainText: rendered.textContent,
    html: rendered.htmlContent
  };
}

