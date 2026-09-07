"""
Write styles.css and script.js for Sankalp Mishra's portfolio
with Ditto Insurance emphasis
"""
import os

PORTFOLIO_DIR = r"C:\Users\home\OneDrive\Desktop\Job\Portfolio"
CSS_PATH = os.path.join(PORTFOLIO_DIR, "styles.css")
JS_PATH = os.path.join(PORTFOLIO_DIR, "script.js")

CSS_CONTENT = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap');

:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-heading: 'Plus Jakarta Sans', var(--font-sans);
  --font-mono: 'JetBrains Mono', monospace;
  
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --primary-light: #60a5fa;
  --primary-subtle: #eff6ff;
  
  --accent: #06b6d4;
  --accent-purple: #7c3aed;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  
  --slate-950: #020617;
  --slate-900: #0f172a;
  --slate-800: #1e293b;
  --slate-700: #334155;
  --slate-600: #475569;
  --slate-500: #64748b;
  --slate-400: #94a3b8;
  --slate-300: #cbd5e1;
  --slate-200: #e2e8f0;
  --slate-100: #f1f5f9;
  --slate-50: #f8fafc;
  
  --card-bg: rgba(255, 255, 255, 0.85);
  --card-border: rgba(226, 232, 240, 0.8);
  --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
  --card-shadow-hover: 0 20px 40px -15px rgba(37, 99, 235, 0.12), 0 8px 16px -4px rgba(0, 0, 0, 0.04);
}

* {
  box-sizing: border-box;
}

html {
  font-family: var(--font-sans);
  scroll-behavior: smooth;
  -webkit-tap-highlight-color: transparent;
}

body {
  font-family: var(--font-sans);
  color: var(--slate-900);
  background-color: #fafbfc;
  overflow-x: hidden;
  position: relative;
}

h1, h2, h3, h4, h5, h6, .font-heading {
  font-family: var(--font-heading);
  letter-spacing: -0.025em;
}

code, kbd, samp, pre, .font-mono {
  font-family: var(--font-mono);
}

/* Scroll Progress Bar */
#scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #2563eb, #06b6d4, #7c3aed);
  z-index: 9999;
  width: 0%;
  transition: width 0.1s ease-out;
  box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
}

/* Ambient Mesh Glows */
.mesh-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.45;
  pointer-events: none;
  z-index: 0;
  animation: pulseGlow 12s ease-in-out infinite alternate;
}

.mesh-glow-blue {
  background: radial-gradient(circle, rgba(37, 99, 235, 0.35) 0%, rgba(37, 99, 235, 0) 70%);
}

.mesh-glow-cyan {
  background: radial-gradient(circle, rgba(6, 182, 212, 0.3) 0%, rgba(6, 182, 212, 0) 70%);
}

.mesh-glow-purple {
  background: radial-gradient(circle, rgba(124, 58, 237, 0.25) 0%, rgba(124, 58, 237, 0) 70%);
}

@keyframes pulseGlow {
  0% { transform: scale(1) translate(0, 0); opacity: 0.35; }
  50% { transform: scale(1.15) translate(20px, -20px); opacity: 0.55; }
  100% { transform: scale(0.95) translate(-15px, 15px); opacity: 0.35; }
}

/* Interactive Cursor Glow */
.cursor-glow-dot {
  position: fixed;
  width: 350px;
  height: 350px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.08) 0%, rgba(6, 182, 212, 0.04) 40%, transparent 70%);
  pointer-events: none;
  z-index: 9990;
  transform: translate(-50%, -50%);
  transition: transform 0.06s ease-out;
}

/* Glassmorphism Classes */
.glass-card {
  background: var(--card-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--card-border);
  box-shadow: var(--card-shadow);
  border-radius: 1.25rem;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-card-hover:hover {
  transform: translateY(-4px);
  border-color: rgba(37, 99, 235, 0.3);
  box-shadow: var(--card-shadow-hover);
}

.glass-pill {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 9999px;
}

/* Gradient Text */
.gradient-text {
  background: linear-gradient(135deg, #0f172a 0%, #2563eb 50%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-text-blue {
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 50%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-text-emerald {
  background: linear-gradient(135deg, #047857 0%, #10b981 50%, #34d399 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Interactive Role Filter Chips */
.role-chip {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  user-select: none;
}

.role-chip.active {
  background: #2563eb;
  color: #ffffff !important;
  border-color: #2563eb;
  box-shadow: 0 4px 14px -2px rgba(37, 99, 235, 0.45);
  transform: translateY(-1px);
}

.role-chip.active svg {
  color: #ffffff;
}

/* Skill badges */
.tech-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 0.5rem;
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.tech-badge:hover {
  background: #e2e8f0;
  color: #0f172a;
  border-color: #cbd5e1;
}

/* Highlighted project card in role lens */
.project-card {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.project-card.lens-highlighted {
  border-color: #3b82f6;
  box-shadow: 0 16px 36px -10px rgba(37, 99, 235, 0.22), 0 0 0 2px rgba(59, 130, 246, 0.15);
  transform: translateY(-4px) scale(1.01);
}

.project-card.lens-dimmed {
  opacity: 0.55;
  filter: grayscale(20%);
}

/* Stat Counters */
.counter-value {
  display: inline-block;
  font-variant-numeric: tabular-nums;
  font-weight: 800;
}

/* Modal System */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.25s ease, visibility 0.25s ease;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal-window {
  background: #ffffff;
  border-radius: 1.5rem;
  max-width: 48rem;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(226, 232, 240, 0.8);
  transform: scale(0.95) translateY(10px);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-overlay.active .modal-window {
  transform: scale(1) translateY(0);
}

/* Toast System */
#toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 10050;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  background: #0f172a;
  color: #ffffff;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transform: translateY(20px);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast.show {
  transform: translateY(0);
  opacity: 1;
}

/* Smooth custom scrollbars for modal */
.modal-window::-webkit-scrollbar {
  width: 6px;
}
.modal-window::-webkit-scrollbar-track {
  background: #f8fafc;
}
.modal-window::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 9999px;
}
.modal-window::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Print Styles */
@media print {
  .mesh-glow, #cursor-glow, #scroll-progress, .modal-overlay, #toast-container, header, footer, .role-chip {
    display: none !important;
  }
  body {
    background: #ffffff !important;
    color: #000000 !important;
  }
}
"""

JS_CONTENT = """/**
 * Sankalp Mishra Portfolio — Interactive Systems
 * Recruiter Role Lens, Metric Counters, STAR Modals, Cheat Sheet, Toast Notifications
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollProgress();
  initCursorGlow();
  initRoleLens();
  initMetricCounters();
  initModals();
  initQuickCopy();
  initMobileMenu();
});

/* 1. SCROLL PROGRESS BAR */
function initScrollProgress() {
  const progressBar = document.getElementById('scroll-progress');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) return;
    const progress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = `${progress}%`;
  }, { passive: true });
}

/* 2. AMBIENT CURSOR GLOW (Desktop) */
function initCursorGlow() {
  const cursorGlow = document.getElementById('cursor-glow');
  if (!cursorGlow || window.innerWidth < 1024) return;

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let currentX = mouseX;
  let currentY = mouseY;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  }, { passive: true });

  function render() {
    currentX += (mouseX - currentX) * 0.15;
    currentY += (mouseY - currentY) * 0.15;
    cursorGlow.style.left = `${currentX}px`;
    cursorGlow.style.top = `${currentY}px`;
    requestAnimationFrame(render);
  }
  render();
}

/* 3. RECRUITER ROLE LENS */
const roleData = {
  'all': {
    title: 'All-Round Profile',
    matchScore: 100,
    tagline: 'Bridging Economics, Data-Driven Analytics, and 0-to-1 Product Execution',
    highlightedProjects: ['swasth-ai', 'healthcare-cost', 'ipl-outcome', 'startup-funding', 'retail-churn'],
    skills: ['Cross-Functional Execution', 'SQL & Python Analytics', '0-to-1 Product Building', 'Consumer Advisory & Sales', 'Economics & Unit Economics', 'A/B Testing & EDA'],
    summary: 'Demonstrated ability to wear multiple hats: from building an end-to-end OPD triage system (SwasthAI) with zero-to-one clinic deployments to high-volume statistical predictive modeling in Python and 150+ direct advisory sessions at Ditto Insurance.'
  },
  'founders-office': {
    title: "Founder's Office / Generalist",
    matchScore: 98,
    tagline: '0-to-1 Execution, Cross-functional Speed, Unit Economics & Market Launch',
    highlightedProjects: ['swasth-ai', 'startup-funding'],
    skills: ['0-to-1 Product Building', 'Cold Outreach & Business Dev', 'Consumer Advisory & Objections', 'Unit Economics & Financial Modeling', 'Cross-Functional Execution', 'Clinical Workflow Design'],
    summary: 'Built SwasthAI from zero: architected queue prioritization algorithms, conducted live OPD hospital user interviews, and executed clinical outreach. Plus direct consumer BD & funnel analysis at Ditto Insurance.'
  },
  'business-analyst': {
    title: 'Business Analyst / Analytics',
    matchScore: 96,
    tagline: 'SQL, Python, Hypothesis Testing, EDA & Business Intelligence Dashboards',
    highlightedProjects: ['healthcare-cost', 'ipl-outcome', 'retail-churn'],
    skills: ['Exploratory Data Analysis (EDA)', 'Hypothesis Testing & Regression', 'SQL & Database Design', 'Predictive Modeling (XGBoost, Sklearn)', 'Churn & Cohort Analysis', 'Tableau / PowerBI'],
    summary: 'Engineered regression pipelines predicting healthcare treatment costs with R² of 0.88, optimized retail customer retention models with 84% accuracy, and synthesized millions of IPL event rows into match predictive signals.'
  },
  'product-ops': {
    title: 'Product Operations / Associate PM',
    matchScore: 94,
    tagline: 'Workflow Optimization, User Journey Mapping, Incident Triage & SOP Design',
    highlightedProjects: ['swasth-ai', 'retail-churn'],
    skills: ['Operational Bottleneck Triage', 'User Journey & Empathy Mapping', 'Advisory Funnel Optimization', 'Standard Operating Procedures (SOPs)', 'Event Tracking & Telemetry', 'Customer Retention Strategy'],
    summary: 'Identified OPD wait-time bottlenecks in Indian clinics, engineered automated QR-to-WhatsApp priority dispatch loops, and mapped consumer advisory hesitation drivers at Ditto Insurance.'
  }
};

function initRoleLens() {
  const chips = document.querySelectorAll('.role-chip');
  const lensTitle = document.getElementById('lens-title');
  const lensScore = document.getElementById('lens-score');
  const lensScoreBar = document.getElementById('lens-score-bar');
  const lensTagline = document.getElementById('lens-tagline');
  const lensSummary = document.getElementById('lens-summary');
  const lensSkills = document.getElementById('lens-skills');
  const projectCards = document.querySelectorAll('.project-card');

  if (!chips.length) return;

  function updateLens(roleKey) {
    const data = roleData[roleKey] || roleData['all'];

    // Update active chip styling
    chips.forEach(chip => {
      if (chip.dataset.role === roleKey) {
        chip.classList.add('active');
      } else {
        chip.classList.remove('active');
      }
    });

    // Update text
    if (lensTitle) lensTitle.textContent = data.title;
    if (lensScore) lensScore.textContent = `${data.matchScore}%`;
    if (lensScoreBar) lensScoreBar.style.width = `${data.matchScore}%`;
    if (lensTagline) lensTagline.textContent = data.tagline;
    if (lensSummary) lensSummary.textContent = data.summary;

    // Update skills list
    if (lensSkills) {
      lensSkills.innerHTML = data.skills.map(s => `
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200/80">
          <svg class="w-3 h-3 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
          ${s}
        </span>
      `).join('');
    }

    // Highlight / Dim project cards
    projectCards.forEach(card => {
      const pId = card.dataset.projectId;
      if (data.highlightedProjects.includes(pId)) {
        card.classList.add('lens-highlighted');
        card.classList.remove('lens-dimmed');
      } else {
        card.classList.remove('lens-highlighted');
        card.classList.add('lens-dimmed');
      }
    });
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const role = chip.dataset.role;
      updateLens(role);
    });
  });

  // Default initialize
  updateLens('all');
}

/* 4. METRIC NUMBER COUNTERS */
function initMetricCounters() {
  const counters = document.querySelectorAll('.counter-value');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseFloat(el.dataset.target || 0);
        const prefix = el.dataset.prefix || '';
        const suffix = el.dataset.suffix || '';
        const decimals = parseInt(el.dataset.decimals || 0, 10);
        const duration = 1600;
        const startTime = performance.now();

        function updateCounter(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          // Ease-out expo
          const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
          const currentVal = target * easeProgress;
          
          el.textContent = `${prefix}${currentVal.toFixed(decimals)}${suffix}`;

          if (progress < 1) {
            requestAnimationFrame(updateCounter);
          } else {
            el.textContent = `${prefix}${target.toFixed(decimals)}${suffix}`;
          }
        }

        requestAnimationFrame(updateCounter);
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  counters.forEach(c => observer.observe(c));
}

/* 5. STAR CASE STUDY MODALS & CHEAT SHEET */
const starCaseStudies = {
  'swasth-ai': {
    title: 'SwasthAI — Intelligent OPD Clinical Triage & Queue Optimization',
    subtitle: 'Founder & Product Lead • 0-to-1 Healthcare SaaS Architecture',
    liveUrl: 'https://swasthai-three.vercel.app/',
    tags: ["Founder's Office", 'Healthcare AI', 'Next.js', 'FastAPI', 'WhatsApp Cloud API'],
    situation: 'OPD registrations in Indian hospitals scaled dramatically via ABDM QR codes, but physical doctor wait times remained an acute bottleneck. Critical patients with high urgency sat waiting behind routine checkups because traditional queues operate strictly on first-come-first-serve.',
    task: 'Design, build, and deploy an automated, non-invasive digital triage system that allows patients to submit structured symptoms upon QR scan, classifies acuity levels, and generates real-time priority queues for physicians without increasing administrative overhead.',
    action: '1. Conducted qualitative workflow observations across urban and semi-urban Indian clinics to map physician triage patterns.\\n2. Built interactive patient intake questionnaire requiring <90 seconds completion.\\n3. Architected multi-factor clinical urgency scoring algorithm weighting symptom severity, vital flags, and age vulnerabilities.\\n4. Engineered doctor-facing dashboard with 1-click WhatsApp alerts, manual queue overrides, and full ABDM compliance data isolation.\\n5. Executed targeted 496+ hospital clinical outreach campaign validating clinician demand.',
    result: '1. Deployed functional cloud platform with <150ms triage response time.\\n2. 0 hard bounces across clinical outreach campaigns with verified institutional physician interest.\\n3. Live operational MVP providing measurable reduction in critical patient wait times.',
    metrics: [
      { label: 'Triage Response Time', value: '<150ms' },
      { label: 'Clinical Emails Verified', value: '496+' },
      { label: 'Doctor Override Rate', value: '100% Control' }
    ]
  },
  'healthcare-cost': {
    title: 'Healthcare Insurance Treatment Cost Prediction Engine',
    subtitle: 'Business Analytics & Predictive Modeling in Python',
    githubUrl: 'https://github.com/Sankalp232004/Portfolio',
    tags: ['Machine Learning', 'Regression Analysis', 'EDA', 'Scikit-Learn', 'Feature Engineering'],
    situation: 'Healthcare providers and insurance underwriters suffer from severe pricing variance and opacity when estimating patient claim payouts and treatment expenses across demographic cohorts.',
    task: 'Develop an end-to-end predictive machine learning model to estimate individual healthcare charges based on age, BMI, smoking habits, regional factors, and family dependents with maximum statistical interpretability.',
    action: '1. Conducted thorough exploratory data analysis (EDA), identifying smoking status and BMI interaction as the primary variance driver.\\n2. Implemented log transformations to normalize skewed cost distributions.\\n3. Evaluated Linear Regression, Ridge, Random Forest, and Gradient Boosted Regressors.\\n4. Engineered cross-validated hyperparameter tuning pipelines with SHAP value explainability for insurance underwriting.',
    result: 'Achieved R² score of 0.88 and reduced Mean Absolute Error (MAE) by 24% compared to baseline regression benchmarks.',
    metrics: [
      { label: 'Model R² Score', value: '0.88' },
      { label: 'MAE Error Reduction', value: '-24%' },
      { label: 'Key Factor', value: 'BMI × Smoker Interaction' }
    ]
  },
  'ipl-outcome': {
    title: 'IPL Match Winner & Win-Probability Prediction Model',
    subtitle: 'Sports Analytics & Classification Pipeline',
    githubUrl: 'https://github.com/Sankalp232004/Portfolio',
    tags: ['Sports Analytics', 'Classification', 'Python', 'XGBoost', 'Feature Engineering'],
    situation: 'T20 cricket is characterized by high intra-match volatility, where traditional win-probability indicators fail to account for pitch deterioration, dynamic run rates, and individual venue biases.',
    task: 'Synthesize ball-by-ball historical IPL datasets (over 200,000 deliveries) into dynamic in-game win-probability models that update after every ball.',
    action: '1. Aggregated ball-by-ball match data across 15+ IPL seasons.\\n2. Engineered contextual metrics: Required Run Rate (RRR), Current Run Rate (CRR), wickets remaining, venue-specific chase success rates, and head-to-head match-up weights.\\n3. Trained Logistic Regression and XGBoost classifiers calibrated with Brier score metrics for accurate probability distributions.',
    result: 'Delivered an 81.5% classification accuracy on out-of-sample test playoff fixtures with real-time ball-by-ball probability curve visualization.',
    metrics: [
      { label: 'Model Accuracy', value: '81.5%' },
      { label: 'Historical Deliveries', value: '200,000+' },
      { label: 'Calibration Metric', value: 'Brier Score < 0.14' }
    ]
  },
  'startup-funding': {
    title: 'Indian Startup Ecosystem Funding & Valuation Analytics',
    subtitle: 'Venture Capital Intelligence & Macroeconomic EDA',
    githubUrl: 'https://github.com/Sankalp232004/Portfolio',
    tags: ['Economic Analysis', 'Venture Capital', 'EDA', 'Data Visualization', 'Unit Economics'],
    situation: 'The Indian startup ecosystem underwent drastic funding cycle swings from 2021 bull peaks to 2023–2024 capital consolidation, making sector allocation trends opaque for founders and angel syndicates.',
    task: 'Analyze 3,000+ funding rounds across Indian startups to map sector-wise valuations, stage-wise cheque sizes, geographic hubs, and macroeconomic correlation with interest rate cycles.',
    action: '1. Cleaned and normalized messy multi-currency funding records spanning Pre-Seed to Series F.\\n2. Built granular sector taxonomy (Fintech, Healthtech, SaaS, Consumer, Deeptech).\\n3. Conducted cohort analysis to identify valuation multiples and runway sustainability indicators across deal stages.',
    result: 'Produced executive-ready visual intelligence dashboard and research memorandum detailing funding shifts toward positive unit economics.',
    metrics: [
      { label: 'Deals Analyzed', value: '3,000+' },
      { label: 'Sectors Mapped', value: '14 Verticals' },
      { label: 'Key Finding', value: 'Unit Economics Shift' }
    ]
  },
  'retail-churn': {
    title: 'Customer Churn Analytics & Retention Strategy Model',
    subtitle: 'Customer Lifetime Value (LTV) & Cohort Optimization',
    githubUrl: 'https://github.com/Sankalp232004/Portfolio',
    tags: ['Customer Analytics', 'Cohort Analysis', 'Random Forest', 'LTV Modeling', 'Product Ops'],
    situation: 'Subscription and e-commerce platforms experience silent customer attrition, where reactive discounting happens too late after customer intent has already degraded.',
    task: 'Build a proactive early-warning churn classification engine that identifies at-risk accounts 30 days prior to contract expiration or session inactivity.',
    action: '1. Constructed RFM (Recency, Frequency, Monetary) segmentation matrices across customer transaction logs.\\n2. Developed behavioral engagement decay metrics capturing declining login frequencies and customer support ticket sentiment.\\n3. Trained Random Forest and Balanced SMOTE classifiers to overcome class imbalance in churn events.',
    result: 'Achieved 84% ROC-AUC score, enabling automated segment-specific re-engagement campaigns capable of recovering an estimated 18% of at-risk accounts.',
    metrics: [
      { label: 'ROC-AUC Score', value: '84%' },
      { label: 'Account Recovery Est.', value: '18%' },
      { label: 'Early-Warning Window', value: '30 Days' }
    ]
  }
};

function initModals() {
  const modalOverlay = document.getElementById('case-study-modal');
  const modalContent = document.getElementById('modal-dynamic-content');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const cheatSheetModal = document.getElementById('cheat-sheet-modal');
  const cheatSheetBtn = document.getElementById('btn-cheat-sheet');
  const cheatSheetCloseBtn = document.getElementById('cheat-sheet-close-btn');

  function openStarModal(studyKey) {
    const study = starCaseStudies[studyKey];
    if (!study || !modalContent || !modalOverlay) return;

    modalContent.innerHTML = `
      <div class="p-6 sm:p-8 space-y-6">
        <!-- Header -->
        <div class="border-b border-slate-200 pb-5">
          <div class="flex flex-wrap gap-2 mb-3">
            ${study.tags.map(t => `<span class="px-2.5 py-0.5 rounded-md text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200">${t}</span>`).join('')}
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight font-heading">${study.title}</h2>
          <p class="text-sm font-medium text-slate-500 mt-1">${study.subtitle}</p>
        </div>

        <!-- Key Metrics Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200/80">
          ${study.metrics.map(m => `
            <div class="text-center sm:text-left">
              <span class="block text-xs font-semibold uppercase tracking-wider text-slate-500">${m.label}</span>
              <span class="text-lg sm:text-xl font-black text-blue-600 font-heading">${m.value}</span>
            </div>
          `).join('')}
        </div>

        <!-- STAR Framework Sections -->
        <div class="space-y-4 text-sm text-slate-700">
          <div class="p-4 rounded-xl bg-white border border-slate-200/80">
            <span class="inline-flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-amber-700 bg-amber-50 px-2 py-0.5 rounded mb-1.5">
              Situation
            </span>
            <p class="leading-relaxed mt-1">${study.situation}</p>
          </div>

          <div class="p-4 rounded-xl bg-white border border-slate-200/80">
            <span class="inline-flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-blue-700 bg-blue-50 px-2 py-0.5 rounded mb-1.5">
              Task & Objective
            </span>
            <p class="leading-relaxed mt-1">${study.task}</p>
          </div>

          <div class="p-4 rounded-xl bg-white border border-slate-200/80">
            <span class="inline-flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded mb-1.5">
              Action & Execution
            </span>
            <p class="leading-relaxed mt-1 whitespace-pre-line">${study.action}</p>
          </div>

          <div class="p-4 rounded-xl bg-white border border-slate-200/80">
            <span class="inline-flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded mb-1.5">
              Result & Business Impact
            </span>
            <p class="leading-relaxed mt-1">${study.result}</p>
          </div>
        </div>

        <!-- Action Links -->
        <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-slate-200">
          <div class="flex items-center gap-3">
            ${study.liveUrl ? `
              <a href="${study.liveUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white text-xs font-bold hover:bg-blue-700 transition shadow-md shadow-blue-500/20">
                <span>View Live Deployment</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            ` : ''}
            ${study.githubUrl ? `
              <a href="${study.githubUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition">
                <span>View Source Code</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            ` : ''}
          </div>
          <button type="button" class="close-modal-trigger text-xs font-bold text-slate-500 hover:text-slate-900 px-3 py-1.5">Close</button>
        </div>
      </div>
    `;

    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Hook internal close triggers
    modalContent.querySelectorAll('.close-modal-trigger').forEach(b => {
      b.addEventListener('click', closeModal);
    });
  }

  function closeModal() {
    if (modalOverlay) modalOverlay.classList.remove('active');
    if (cheatSheetModal) cheatSheetModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Bind project cards STAR buttons
  document.querySelectorAll('[data-star-target]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const target = btn.dataset.starTarget;
      openStarModal(target);
    });
  });

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  // Cheat Sheet Modal
  if (cheatSheetBtn && cheatSheetModal) {
    cheatSheetBtn.addEventListener('click', () => {
      cheatSheetModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  }

  if (cheatSheetCloseBtn && cheatSheetModal) {
    cheatSheetCloseBtn.addEventListener('click', closeModal);
    cheatSheetModal.addEventListener('click', (e) => {
      if (e.target === cheatSheetModal) closeModal();
    });
  }

  // ESC key to close
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

/* 6. INSTANT 1-CLICK COPY & TOAST NOTIFICATIONS */
function initQuickCopy() {
  function copyTextToClipboard(text, label) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => showToast(`Copied ${label} to clipboard!`));
    } else {
      const input = document.createElement('input');
      input.value = text;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      showToast(`Copied ${label} to clipboard!`);
    }
  }

  document.querySelectorAll('[data-copy]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const text = el.dataset.copy;
      const label = el.dataset.copyLabel || 'text';
      copyTextToClipboard(text, label);
    });
  });
}

function showToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg class="w-5 h-5 text-emerald-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
    </svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  // Trigger animation
  setTimeout(() => toast.classList.add('show'), 10);

  // Remove after 3.2s
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

/* 7. MOBILE NAVIGATION TOGGLE */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileNav = document.getElementById('mobile-nav');

  if (!menuBtn || !mobileNav) return;

  menuBtn.addEventListener('click', () => {
    const isHidden = mobileNav.classList.contains('hidden');
    if (isHidden) {
      mobileNav.classList.remove('hidden');
    } else {
      mobileNav.classList.add('hidden');
    }
  });

  // Close when clicking nav links
  mobileNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileNav.classList.add('hidden');
    });
  });
}
"""

with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(CSS_CONTENT)
print("[OK] Generated styles.css")

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(JS_CONTENT)
print("[OK] Generated script.js")
