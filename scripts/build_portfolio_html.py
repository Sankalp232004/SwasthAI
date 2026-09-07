"""
Generate the complete upgraded index.html for Sankalp Mishra's portfolio
incorporating verified LinkedIn profile details:
- B.A. Economics, Minor in Applied Mathematics (FLAME University)
- India Book of Records Holder (Fastest Cube Root Calculation)
- Ditto Insurance (Insurance Advisor)
- Discover India Program (14-member Research Team Lead) & WageIndicator Foundation
- HackerRank Python & Data Analysis Certifications
"""
import os

PORTFOLIO_DIR = r"C:\Users\home\OneDrive\Desktop\Job\Portfolio"
INDEX_PATH = os.path.join(PORTFOLIO_DIR, "index.html")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Primary SEO Meta Tags -->
  <title>Sankalp Mishra &mdash; Business Analyst &amp; Strategy | Founder's Office &amp; Product Operations</title>
  <meta name="title" content="Sankalp Mishra &mdash; Business Analyst &amp; Strategy | Founder's Office &amp; Product Operations" />
  <meta name="description" content="Economics &amp; Applied Mathematics at FLAME University, Founder of SwasthAI, and Insurance Advisor at Ditto Insurance. India Book of Records Holder. Specializing in Founder's Office, Business Analytics, and 0-to-1 Product Strategy." />
  <meta name="keywords" content="Business Analyst, Strategy, Product Operations, Founder's Office, Business Analytics, Economics, Applied Mathematics, Product Management, Sankalp Mishra, SwasthAI, Ditto Insurance, India Book of Records" />
  <meta name="author" content="Sankalp Mishra" />

  <!-- Open Graph / LinkedIn / Facebook -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://sankalp232004.github.io/Portfolio/" />
  <meta property="og:title" content="Sankalp Mishra &mdash; Business Analyst &amp; Strategy Portfolio" />
  <meta property="og:description" content="Economics &amp; Applied Math (FLAME University), Founder of SwasthAI &amp; Insurance Advisor at Ditto. Solving operational bottlenecks through quantitative analytics, product thinking, and 0-to-1 execution." />
  <meta property="og:image" content="Photo.jpeg" />

  <!-- Twitter Card -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://sankalp232004.github.io/Portfolio/" />
  <meta property="twitter:title" content="Sankalp Mishra &mdash; Business Analyst &amp; Strategy Portfolio" />
  <meta property="twitter:description" content="Economics &amp; Applied Math (FLAME University), Founder of SwasthAI &amp; Insurance Advisor at Ditto. Solving operational bottlenecks through quantitative analytics, product thinking, and 0-to-1 execution." />
  <meta property="twitter:image" content="Photo.jpeg" />

  <!-- Structured Data (Schema.org Person) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Sankalp Mishra",
    "url": "https://sankalp232004.github.io/Portfolio/",
    "image": "https://sankalp232004.github.io/Portfolio/Photo.jpeg",
    "jobTitle": "Founder & Business Analyst",
    "telephone": "+919140721395",
    "email": "mishrasankalp04@gmail.com",
    "alumniOf": {
      "@type": "EducationalOrganization",
      "name": "FLAME University"
    },
    "award": "India Book of Records Holder (Fastest Cube Root Calculation)",
    "knowsAbout": [
      "Business Analysis",
      "Product Strategy",
      "Product Operations",
      "Founder's Office",
      "Business Analytics",
      "Economics & Applied Mathematics",
      "SQL",
      "Python",
      "GTM Strategy",
      "Insurtech Underwriting & Advisory"
    ],
    "sameAs": [
      "https://www.linkedin.com/in/sankalp2329/",
      "https://github.com/Sankalp232004"
    ]
  }
  </script>

  <!-- TailwindCSS CDN & Custom Design System -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="styles.css" />
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col antialiased selection:bg-blue-600 selection:text-white relative">
  
  <!-- DESKTOP CURSOR GLOW -->
  <div id="cursor-glow" class="cursor-glow-dot hidden lg:block"></div>

  <!-- SCROLL PROGRESS BAR -->
  <div id="scroll-progress"></div>

  <!-- AMBIENT BACKGROUND GLOWS -->
  <div class="mesh-glow mesh-glow-blue w-[600px] h-[600px] top-[-100px] left-[-150px]"></div>
  <div class="mesh-glow mesh-glow-cyan w-[500px] h-[500px] top-[500px] right-[-150px]"></div>
  <div class="mesh-glow mesh-glow-purple w-[650px] h-[650px] top-[1800px] left-[-200px]"></div>

  <!-- STICKY GLASS NAVIGATION BAR -->
  <header class="sticky top-0 z-50 bg-white/85 backdrop-blur-xl border-b border-slate-200/80 transition-all duration-300">
    <nav class="max-w-7xl mx-auto px-5 sm:px-8 py-3.5 flex items-center justify-between">
      <a href="#hero" class="text-lg font-extrabold text-slate-900 tracking-tight hover:text-blue-600 transition-colors flex items-center gap-2.5 group">
        <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 text-white flex items-center justify-center text-xs font-black shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">SM</span>
        <span class="font-heading font-bold text-slate-900 group-hover:text-blue-600 transition-colors">Sankalp Mishra</span>
      </a>

      <!-- Desktop Nav Links -->
      <div class="hidden lg:flex items-center gap-6 text-sm font-medium text-slate-600">
        <a href="#about" class="hover:text-blue-600 transition-colors">About</a>
        <a href="#role-lens" class="hover:text-blue-600 transition-colors">Role Match</a>
        <a href="#featured-swasth" class="hover:text-blue-600 transition-colors font-semibold text-blue-600 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
          SwasthAI (Featured)
        </a>
        <a href="#projects" class="hover:text-blue-600 transition-colors">Analytics Projects</a>
        <a href="#skills" class="hover:text-blue-600 transition-colors">Skills</a>
        <a href="#experience" class="hover:text-blue-600 transition-colors">Experience</a>
        <a href="#honors" class="hover:text-blue-600 transition-colors">Honors</a>
        <a href="#contact" class="hover:text-blue-600 transition-colors">Contact</a>
      </div>

      <!-- Action Buttons -->
      <div class="hidden sm:flex items-center gap-3">
        <button type="button" id="btn-cheat-sheet" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-lg bg-amber-50 text-amber-900 border border-amber-300/80 hover:bg-amber-100 hover:border-amber-400 transition shadow-sm">
          <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          <span>30s Recruiter Cheat Sheet</span>
        </button>
        <a href="Resume.pdf" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition shadow-md shadow-blue-500/20">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          <span>Resume PDF</span>
        </a>
      </div>

      <!-- Mobile Hamburger Button -->
      <button type="button" id="mobile-menu-btn" class="lg:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition" aria-label="Toggle navigation menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
      </button>
    </nav>

    <!-- Mobile Slide-Down Menu -->
    <div id="mobile-nav" class="hidden lg:hidden border-t border-slate-200 bg-white/95 px-6 py-4 space-y-3">
      <a href="#about" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">About</a>
      <a href="#role-lens" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Role Match</a>
      <a href="#featured-swasth" class="block text-sm font-semibold text-blue-600">SwasthAI (Featured 0-to-1)</a>
      <a href="#projects" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Analytics Projects</a>
      <a href="#skills" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Skills &amp; Competencies</a>
      <a href="#experience" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Experience &amp; Education</a>
      <a href="#honors" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Honors &amp; Records</a>
      <a href="#contact" class="block text-sm font-semibold text-slate-700 hover:text-blue-600">Contact</a>
      <div class="pt-3 border-t border-slate-100 flex flex-col gap-2">
        <a href="Resume.pdf" target="_blank" class="w-full text-center py-2.5 rounded-lg bg-blue-600 text-white font-bold text-xs">Download Resume</a>
      </div>
    </div>
  </header>

  <main class="flex-grow">
    
    <!-- 1. HERO SECTION -->
    <section id="hero" class="relative pt-12 pb-16 lg:pt-20 lg:pb-24 overflow-hidden">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          
          <!-- Hero Left Column -->
          <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
            
            <!-- Badges Bar -->
            <div class="flex flex-wrap items-center justify-center lg:justify-start gap-2">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-bold tracking-wide shadow-sm">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                <span>Open for Roles &bull; Founder's Office / Business Analyst / Product Ops</span>
              </div>
              <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-300 text-amber-900 text-xs font-bold tracking-wide shadow-sm">
                <span>🏆 India Book of Records Holder</span>
              </div>
            </div>

            <!-- Main Headline -->
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-[1.1] font-heading">
              Turning Complex Operations &amp; Data into 
              <span class="gradient-text-blue block mt-1">High-Impact Decisions.</span>
            </h1>

            <!-- Bio Summary -->
            <p class="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto lg:mx-0">
              Economics &amp; Applied Mathematics at <strong class="text-slate-900 font-semibold">FLAME University</strong>, Founder of <strong class="text-blue-600 font-semibold">SwasthAI</strong>, and Insurance Advisor at <strong class="text-slate-900 font-semibold">Ditto Insurance</strong>. Bridging high-speed quantitative modeling (SQL, Python, Machine Learning) with 0-to-1 operational execution, client advisory empathy, and strategic business growth.
            </p>

            <!-- High-Impact Stat Badges -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
              <div class="glass-card p-3.5 text-center">
                <span class="block text-xl sm:text-2xl font-black text-blue-600 font-heading counter-value" data-target="496" data-suffix="+">0</span>
                <span class="text-xs font-semibold text-slate-500 mt-0.5 block">Clinical Outreaches</span>
              </div>
              <div class="glass-card p-3.5 text-center">
                <span class="block text-xl sm:text-2xl font-black text-indigo-600 font-heading counter-value" data-target="150" data-suffix="+">0</span>
                <span class="text-xs font-semibold text-slate-500 mt-0.5 block">Ditto Consultations</span>
              </div>
              <div class="glass-card p-3.5 text-center">
                <span class="block text-xl sm:text-2xl font-black text-cyan-600 font-heading counter-value" data-target="14" data-suffix="-Mbr">0</span>
                <span class="text-xs font-semibold text-slate-500 mt-0.5 block">Research Team Lead</span>
              </div>
              <div class="glass-card p-3.5 text-center">
                <span class="block text-xl sm:text-2xl font-black text-emerald-600 font-heading">Econ + Math</span>
                <span class="text-xs font-semibold text-slate-500 mt-0.5 block">FLAME University</span>
              </div>
            </div>

            <!-- Primary CTAs -->
            <div class="flex flex-wrap items-center justify-center lg:justify-start gap-3.5 pt-3">
              <a href="#featured-swasth" class="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm transition shadow-lg shadow-blue-500/25 flex items-center gap-2">
                <span>Explore SwasthAI (0-to-1)</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
              <a href="#projects" class="px-5 py-3 rounded-xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-bold text-sm transition shadow-sm flex items-center gap-2">
                <span>View Analytics Projects</span>
              </a>
              <button type="button" data-copy="mishrasankalp04@gmail.com" data-copy-label="Email" class="px-4 py-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-sm transition flex items-center gap-2" title="Copy Email">
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                <span>Copy Email</span>
              </button>
            </div>

          </div>

          <!-- Hero Right Column: Profile Card -->
          <div class="lg:col-span-5 flex justify-center">
            <div class="w-full max-w-md glass-card p-6 sm:p-7 relative group">
              
              <!-- Subtle glow halo -->
              <div class="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-3xl blur opacity-20 group-hover:opacity-35 transition duration-500"></div>

              <div class="relative space-y-5">
                <!-- Avatar & Status -->
                <div class="relative flex items-center gap-4">
                  <div class="relative w-24 h-24 sm:w-28 sm:h-28 rounded-2xl overflow-hidden border-2 border-white shadow-lg flex-shrink-0 bg-slate-200">
                    <img src="Photo.jpeg" alt="Sankalp Mishra" class="w-full h-full object-cover" />
                  </div>
                  <div>
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200/80 mb-1">
                      Founder &bull; Analyst &bull; Advisor
                    </span>
                    <h2 class="text-xl font-extrabold text-slate-900 font-heading">Sankalp Mishra</h2>
                    <p class="text-xs font-medium text-slate-500">Lucknow / Pune &bull; Open to Relocation</p>
                  </div>
                </div>

                <!-- Bio highlights -->
                <div class="space-y-2.5 text-xs text-slate-600 border-t border-b border-slate-100 py-3.5">
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-slate-500">Education</span>
                    <span class="font-bold text-slate-900">FLAME (Econ + Applied Math)</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-slate-500">Flagship SaaS</span>
                    <span class="font-bold text-blue-600">SwasthAI (<a href="https://swasthai-three.vercel.app/" target="_blank" class="underline">Live App</a>)</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-slate-500">Current Role</span>
                    <span class="font-bold text-slate-900">Ditto Insurance (Advisor)</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-slate-500">Quantitative Honors</span>
                    <span class="font-bold text-amber-700">India Book of Records</span>
                  </div>
                </div>

                <!-- Quick Direct Channels -->
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <a href="mailto:mishrasankalp04@gmail.com" class="p-2.5 rounded-lg bg-slate-50 hover:bg-blue-50 hover:text-blue-700 border border-slate-200 text-slate-700 font-semibold flex items-center gap-2 transition">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                    <span>Email Me</span>
                  </a>
                  <a href="tel:+919140721395" class="p-2.5 rounded-lg bg-slate-50 hover:bg-emerald-50 hover:text-emerald-700 border border-slate-200 text-slate-700 font-semibold flex items-center gap-2 transition">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                    <span>+91 9140721395</span>
                  </a>
                  <a href="https://www.linkedin.com/in/sankalp2329/" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-lg bg-slate-50 hover:bg-blue-50 hover:text-blue-700 border border-slate-200 text-slate-700 font-semibold flex items-center gap-2 transition">
                    <svg class="w-4 h-4 text-blue-700 fill-current" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.45a1.64 1.64 0 1 0 0 3.28 1.64 1.64 0 0 0 0-3.28z"></path></svg>
                    <span>LinkedIn</span>
                  </a>
                  <a href="https://github.com/Sankalp232004" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-lg bg-slate-50 hover:bg-slate-100 hover:text-slate-900 border border-slate-200 text-slate-700 font-semibold flex items-center gap-2 transition">
                    <svg class="w-4 h-4 text-slate-800 fill-current" viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"></path></svg>
                    <span>GitHub</span>
                  </a>
                </div>

              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- 2. RECRUITER ROLE LENS (Interactive Filter & Match Engine) -->
    <section id="role-lens" class="py-16 bg-white/70 border-y border-slate-200/80 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="text-center max-w-3xl mx-auto space-y-3 mb-10">
          <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-700 border border-blue-200">
            Recruiter Interactive Lens
          </span>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 font-heading">
            Tailor My Experience to Your Hiring Need
          </h2>
          <p class="text-sm sm:text-base text-slate-600">
            Select the role you are hiring for to see instant skill alignment, dynamic match score, and filtered case studies.
          </p>
        </div>

        <!-- Filter Chips -->
        <div class="flex flex-wrap items-center justify-center gap-2.5 sm:gap-4 mb-8">
          <button type="button" class="role-chip active px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs sm:text-sm flex items-center gap-2 transition" data-role="all">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
            <span>All-Round Profile</span>
          </button>
          <button type="button" class="role-chip px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs sm:text-sm flex items-center gap-2 transition" data-role="founders-office">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            <span>Founder's Office / Generalist</span>
          </button>
          <button type="button" class="role-chip px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs sm:text-sm flex items-center gap-2 transition" data-role="business-analyst">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <span>Business Analyst / Data</span>
          </button>
          <button type="button" class="role-chip px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs sm:text-sm flex items-center gap-2 transition" data-role="product-ops">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            <span>Product Operations / APM</span>
          </button>
        </div>

        <!-- Dynamic Role Intelligence Card -->
        <div class="glass-card p-6 sm:p-8 max-w-4xl mx-auto border-2 border-blue-500/20">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-200">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-blue-600">Active Lens Evaluation</span>
              <h3 id="lens-title" class="text-2xl font-black text-slate-900 font-heading mt-0.5">All-Round Profile</h3>
              <p id="lens-tagline" class="text-sm font-semibold text-slate-600 mt-1">Bridging Economics, Applied Mathematics, and 0-to-1 Product Execution</p>
            </div>
            <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200/80 min-w-[200px]">
              <div class="flex-1">
                <div class="flex justify-between text-xs font-bold mb-1.5">
                  <span class="text-slate-600">Role Match</span>
                  <span id="lens-score" class="text-blue-600 font-extrabold">100%</span>
                </div>
                <div class="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                  <div id="lens-score-bar" class="bg-blue-600 h-full rounded-full transition-all duration-500" style="width: 100%;"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-6 space-y-4">
            <p id="lens-summary" class="text-sm text-slate-700 leading-relaxed">
              Demonstrated ability to wear multiple hats: from building an end-to-end OPD triage system (SwasthAI) with zero-to-one clinic deployments to high-volume statistical predictive modeling in Python, Applied Math modeling, and direct consumer health insurance advisory at Ditto Insurance.
            </p>
            <div>
              <span class="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2.5">Key Core Competencies Activated:</span>
              <div id="lens-skills" class="flex flex-wrap gap-2">
                <!-- Dynamically injected -->
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- 3. FLAGSHIP 0-TO-1 CASE STUDY: SWASTHAI -->
    <section id="featured-swasth" class="py-16 sm:py-24 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-blue-600 text-white mb-2 shadow-md shadow-blue-500/20">
              <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
              <span>Flagship 0-to-1 Product Architecture</span>
            </div>
            <h2 class="text-3xl sm:text-4xl font-black text-slate-900 font-heading">
              SwasthAI &mdash; Intelligent OPD Triage SaaS
            </h2>
          </div>
          <a href="https://swasthai-three.vercel.app/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs sm:text-sm transition shadow-md">
            <span>Launch Live Deployment</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          </a>
        </div>

        <!-- Flagship Big Card -->
        <div class="glass-card p-6 sm:p-10 border-2 border-blue-500/30 shadow-xl relative overflow-hidden project-card" data-project-id="swasth-ai">
          
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10">
            
            <!-- Left 7 cols: Story & Highlights -->
            <div class="lg:col-span-7 space-y-6">
              
              <div>
                <span class="text-xs font-bold text-blue-600 uppercase tracking-wider">The Operational Bottleneck</span>
                <h3 class="text-xl sm:text-2xl font-bold text-slate-900 font-heading mt-1">
                  Why Fast Digital Registrations Didn't Fix Hospital OPD Waiting Lines
                </h3>
                <p class="text-sm sm:text-base text-slate-600 mt-2 leading-relaxed">
                  While ABDM Scan &amp; Share scaled digital registration to minutes, physical doctor queues still operated strictly on first-come-first-serve. Patients with urgent or deteriorating conditions sat waiting behind routine consultations.
                </p>
              </div>

              <!-- Key Solution Pillars -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="p-3.5 rounded-xl bg-white border border-slate-200">
                  <span class="font-bold text-slate-900 block mb-1 flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    QR Structured Intake
                  </span>
                  <p class="text-slate-600">Patients answer <strong class="text-slate-800">4 rapid clinical questions</strong> in &lt;90 seconds on their mobile browser with zero app installation.</p>
                </div>
                <div class="p-3.5 rounded-xl bg-white border border-slate-200">
                  <span class="font-bold text-slate-900 block mb-1 flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    Multi-Factor Triage
                  </span>
                  <p class="text-slate-600">Algorithmic scoring weights pain severity, red-flag symptoms, and patient age vulnerabilities into high/medium/routine tiers.</p>
                </div>
                <div class="p-3.5 rounded-xl bg-white border border-slate-200">
                  <span class="font-bold text-slate-900 block mb-1 flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    Doctor Control &amp; Overrides
                  </span>
                  <p class="text-slate-600">Doctors retain 100% autonomy with 1-click drag-and-drop queue reordering and automated patient SMS/WhatsApp updates.</p>
                </div>
                <div class="p-3.5 rounded-xl bg-white border border-slate-200">
                  <span class="font-bold text-slate-900 block mb-1 flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    Clinical GTM Campaign
                  </span>
                  <p class="text-slate-600">Engineered a 496+ hospital clinical outreach infrastructure with zero hard bounces and high physician interest.</p>
                </div>
              </div>

              <!-- Tech Stack Badges -->
              <div class="flex flex-wrap gap-2 pt-2">
                <span class="tech-badge">Next.js 14</span>
                <span class="tech-badge">FastAPI</span>
                <span class="tech-badge">PostgreSQL</span>
                <span class="tech-badge">WhatsApp Cloud API</span>
                <span class="tech-badge">ABDM Compliance Ready</span>
                <span class="tech-badge">Clinical Urgency Modeling</span>
              </div>

              <!-- CTA to open STAR Modal -->
              <div class="pt-2 flex items-center gap-3">
                <button type="button" data-star-target="swasth-ai" class="px-4 py-2.5 rounded-lg bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 transition flex items-center gap-2 shadow-md shadow-blue-500/20">
                  <span>Read Full STAR Case Study</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </button>
                <a href="https://swasthai-three.vercel.app/" target="_blank" rel="noopener noreferrer" class="px-4 py-2.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs transition">
                  Test Live Demo
                </a>
              </div>

            </div>

            <!-- Right 5 cols: Live Metrics & Flow Architecture -->
            <div class="lg:col-span-5 flex flex-col justify-between gap-4 bg-slate-50/80 p-6 rounded-2xl border border-slate-200">
              
              <div>
                <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-3">Live System Metrics</span>
                <div class="space-y-3">
                  <div class="p-3 bg-white rounded-xl border border-slate-200/80 flex items-center justify-between">
                    <span class="text-xs font-medium text-slate-600">Triage Latency</span>
                    <span class="text-sm font-black text-blue-600">&lt;150ms End-to-End</span>
                  </div>
                  <div class="p-3 bg-white rounded-xl border border-slate-200/80 flex items-center justify-between">
                    <span class="text-xs font-medium text-slate-600">Physician Control</span>
                    <span class="text-sm font-black text-emerald-600">100% Override Authority</span>
                  </div>
                  <div class="p-3 bg-white rounded-xl border border-slate-200/80 flex items-center justify-between">
                    <span class="text-xs font-medium text-slate-600">Intake Completion</span>
                    <span class="text-sm font-black text-indigo-600">&lt;90 Seconds Mobile</span>
                  </div>
                  <div class="p-3 bg-white rounded-xl border border-slate-200/80 flex items-center justify-between">
                    <span class="text-xs font-medium text-slate-600">Target Segment</span>
                    <span class="text-sm font-black text-slate-900">Tier 1 &amp; Tier 2 Indian OPDs</span>
                  </div>
                </div>
              </div>

              <!-- Recruiter Takeaway -->
              <div class="p-4 rounded-xl bg-blue-50/60 border border-blue-200/80 text-xs text-blue-900 space-y-1">
                <span class="font-bold flex items-center gap-1.5 text-blue-800">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                  Founder's Office &amp; PM Takeaway
                </span>
                <p>Proves full-cycle ownership: identifying unaddressed ground-truth user friction, coding the end-to-end platform, creating clinical trust mechanics, and running outbound GTM validation.</p>
              </div>

            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- 4. ANALYTICS & MACHINE LEARNING PROJECTS (STAR Structured) -->
    <section id="projects" class="py-16 sm:py-24 bg-slate-100/60 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="text-center max-w-3xl mx-auto space-y-3 mb-14">
          <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200">
            Analytics &amp; Data Science
          </span>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 font-heading">
            Statistical Modeling &amp; Quantitative Case Studies
          </h2>
          <p class="text-sm sm:text-base text-slate-600">
            Each project is backed by deep exploratory data analysis (EDA), rigorous statistical hypothesis testing, and business impact estimation.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <!-- Project 1: Healthcare Insurance Cost -->
          <div class="glass-card p-6 sm:p-8 flex flex-col justify-between project-card" data-project-id="healthcare-cost">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200">Regression &bull; R² = 0.88</span>
                <span class="text-xs font-bold text-slate-500">Python &bull; Scikit-Learn</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">
                Healthcare Insurance Treatment Cost Prediction Engine
              </h3>
              <p class="text-sm text-slate-600 leading-relaxed">
                Engineered an end-to-end regression pipeline modeling individual claim payouts. Discovered critical non-linear interaction between BMI and smoking status that reduced baseline Mean Absolute Error by 24%.
              </p>
              <div class="flex flex-wrap gap-2 pt-1">
                <span class="tech-badge">Python</span>
                <span class="tech-badge">Ridge / Lasso</span>
                <span class="tech-badge">Gradient Boosting</span>
                <span class="tech-badge">Feature Engineering</span>
                <span class="tech-badge">SHAP Explainability</span>
              </div>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-200/80 flex items-center justify-between">
              <button type="button" data-star-target="healthcare-cost" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5">
                <span>View STAR Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </button>
              <span class="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">MAE -24%</span>
            </div>
          </div>

          <!-- Project 2: IPL Match Outcome Predictor -->
          <div class="glass-card p-6 sm:p-8 flex flex-col justify-between project-card" data-project-id="ipl-outcome">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200">Classification &bull; 81.5% Acc</span>
                <span class="text-xs font-bold text-slate-500">Python &bull; XGBoost</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">
                IPL Match Winner &amp; Ball-by-Ball Probability Model
              </h3>
              <p class="text-sm text-slate-600 leading-relaxed">
                Synthesized 200,000+ historical ball-by-ball records across 15 IPL seasons into a dynamic in-game win probability model incorporating pitch fatigue, required run rates, and venue chase biases.
              </p>
              <div class="flex flex-wrap gap-2 pt-1">
                <span class="tech-badge">Python</span>
                <span class="tech-badge">XGBoost</span>
                <span class="tech-badge">Logistic Regression</span>
                <span class="tech-badge">Brier Score Calibration</span>
                <span class="tech-badge">EDA</span>
              </div>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-200/80 flex items-center justify-between">
              <button type="button" data-star-target="ipl-outcome" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5">
                <span>View STAR Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </button>
              <span class="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">200k+ Balls</span>
            </div>
          </div>

          <!-- Project 3: Indian Startup Funding Analytics -->
          <div class="glass-card p-6 sm:p-8 flex flex-col justify-between project-card" data-project-id="startup-funding">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">Macro Intelligence</span>
                <span class="text-xs font-bold text-slate-500">EDA &bull; Economics</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">
                Indian Startup Ecosystem Funding &amp; Valuation Trends
              </h3>
              <p class="text-sm text-slate-600 leading-relaxed">
                Analyzed 3,000+ venture funding transactions across 14 industry verticals from 2018&ndash;2024, evaluating the macroeconomic transition from hyper-growth subsidization to sustainable unit economics.
              </p>
              <div class="flex flex-wrap gap-2 pt-1">
                <span class="tech-badge">Economics</span>
                <span class="tech-badge">Unit Economics</span>
                <span class="tech-badge">Valuation Multiples</span>
                <span class="tech-badge">Cohort Analysis</span>
                <span class="tech-badge">Pandas / Seaborn</span>
              </div>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-200/80 flex items-center justify-between">
              <button type="button" data-star-target="startup-funding" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5">
                <span>View STAR Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </button>
              <span class="text-xs font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">3,000+ Deals</span>
            </div>
          </div>

          <!-- Project 4: Retail Churn Modeling -->
          <div class="glass-card p-6 sm:p-8 flex flex-col justify-between project-card" data-project-id="retail-churn">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Retention &bull; 84% ROC-AUC</span>
                <span class="text-xs font-bold text-slate-500">Python &bull; RFM Analysis</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">
                Customer Churn Analytics &amp; Proactive Retention Model
              </h3>
              <p class="text-sm text-slate-600 leading-relaxed">
                Constructed RFM segmentation matrices and behavioral decay indicators to identify customer churn risks 30 days ahead of contract lapses, forecasting an 18% recovery rate on at-risk ARR.
              </p>
              <div class="flex flex-wrap gap-2 pt-1">
                <span class="tech-badge">Random Forest</span>
                <span class="tech-badge">SMOTE</span>
                <span class="tech-badge">RFM Analysis</span>
                <span class="tech-badge">LTV Optimization</span>
                <span class="tech-badge">Product Operations</span>
              </div>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-200/80 flex items-center justify-between">
              <button type="button" data-star-target="retail-churn" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5">
                <span>View STAR Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </button>
              <span class="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">18% Recovery</span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- 5. CORE COMPETENCIES & TOOLKIT -->
    <section id="skills" class="py-16 sm:py-24 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="text-center max-w-3xl mx-auto space-y-3 mb-14">
          <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-cyan-50 text-cyan-700 border border-cyan-200">
            Skills &amp; Capabilities
          </span>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 font-heading">
            Core Toolkit &amp; Functional Competencies
          </h2>
          <p class="text-sm sm:text-base text-slate-600">
            A balanced synthesis of strategic economic reasoning, applied mathematics, client advisory empathy, and operational execution.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <!-- Category 1: Founder's Office & Strategy -->
          <div class="glass-card p-6 space-y-4">
            <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Founder's Office &amp; Strategy</h3>
            <ul class="space-y-2 text-xs text-slate-600">
              <li class="flex items-center gap-2">&bull; 0-to-1 Product Building</li>
              <li class="flex items-center gap-2">&bull; Unit Economics &amp; Pricing</li>
              <li class="flex items-center gap-2">&bull; Outbound GTM &amp; Cold Outreach</li>
              <li class="flex items-center gap-2">&bull; Market Research &amp; TAM Analysis</li>
              <li class="flex items-center gap-2">&bull; Cross-Functional Team Leadership</li>
            </ul>
          </div>

          <!-- Category 2: Business Analytics & Data Science -->
          <div class="glass-card p-6 space-y-4">
            <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Analytics &amp; Applied Math</h3>
            <ul class="space-y-2 text-xs text-slate-600">
              <li class="flex items-center gap-2">&bull; SQL (Aggregations, Joins, CTEs)</li>
              <li class="flex items-center gap-2">&bull; Python (Pandas, NumPy, Scikit)</li>
              <li class="flex items-center gap-2">&bull; Exploratory Data Analysis (EDA)</li>
              <li class="flex items-center gap-2">&bull; Predictive Regression &amp; XGBoost</li>
              <li class="flex items-center gap-2">&bull; Applied Math &amp; Quantitative Logic</li>
            </ul>
          </div>

          <!-- Category 3: Product Operations & Growth -->
          <div class="glass-card p-6 space-y-4">
            <div class="w-10 h-10 rounded-xl bg-cyan-100 text-cyan-700 flex items-center justify-center font-bold">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Product Operations &amp; APM</h3>
            <ul class="space-y-2 text-xs text-slate-600">
              <li class="flex items-center gap-2">&bull; User Journey &amp; Empathy Mapping</li>
              <li class="flex items-center gap-2">&bull; Workflow Bottleneck Triage</li>
              <li class="flex items-center gap-2">&bull; Advisory Funnel Optimization</li>
              <li class="flex items-center gap-2">&bull; SOP Documentation &amp; SLAs</li>
              <li class="flex items-center gap-2">&bull; WhatsApp API &amp; Webhook Integration</li>
            </ul>
          </div>

          <!-- Category 4: Tools & Frameworks -->
          <div class="glass-card p-6 space-y-4">
            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Tools &amp; Tech Stack</h3>
            <ul class="space-y-2 text-xs text-slate-600">
              <li class="flex items-center gap-2">&bull; Next.js &bull; TailwindCSS &bull; HTML/JS</li>
              <li class="flex items-center gap-2">&bull; FastAPI &bull; PostgreSQL</li>
              <li class="flex items-center gap-2">&bull; Tableau &bull; PowerBI &bull; Excel / Sheets</li>
              <li class="flex items-center gap-2">&bull; Git &bull; GitHub &bull; Vercel</li>
              <li class="flex items-center gap-2">&bull; Brevo API &bull; REST Endpoints</li>
            </ul>
          </div>

        </div>

      </div>
    </section>

    <!-- 6. EXPERIENCE & EDUCATION -->
    <section id="experience" class="py-16 sm:py-24 bg-white/70 border-t border-slate-200/80 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          <!-- Left Col: Experience -->
          <div class="lg:col-span-7 space-y-8">
            <div>
              <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-700 border border-blue-200">
                Work Experience &amp; Leadership
              </span>
              <h2 class="text-2xl sm:text-3xl font-black text-slate-900 font-heading mt-2">
                Professional Journey &amp; Impact
              </h2>
            </div>

            <!-- Timeline items -->
            <div class="space-y-8 border-l-2 border-blue-200 pl-6 ml-2">
              
              <!-- Role 1: SwasthAI -->
              <div class="relative group">
                <span class="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-blue-600 ring-4 ring-blue-100"></span>
                <div class="flex flex-wrap items-center justify-between gap-1 mb-1">
                  <span class="text-xs font-bold text-blue-600">Dec 2024 &mdash; Present</span>
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-700 border border-blue-200">Founder &bull; SaaS</span>
                </div>
                <h3 class="text-lg font-extrabold text-slate-900 font-heading">Founder &amp; Product Lead</h3>
                <h4 class="text-xs font-bold text-slate-500 mb-2">SwasthAI &bull; Healthcare SaaS (<a href="https://swasthai-three.vercel.app/" target="_blank" class="text-blue-600 underline">Live App</a>)</h4>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-2.5">
                  Conceived and engineered an intelligent OPD triage platform. Built 0-to-1 patient triage UX, doctor dashboard, automated WhatsApp alerts, and deployed clinical email campaigns to 496+ institutional clinics across India.
                </p>
                <ul class="space-y-1.5 text-xs text-slate-600">
                  <li class="flex items-start gap-2">
                    <span class="text-blue-600 font-bold mt-0.5">&bull;</span>
                    <span><strong>0-to-1 Product Architecture:</strong> Designed rapid &lt;90-second QR intake and multi-factor clinical urgency scoring algorithm (&lt;150ms latency).</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-blue-600 font-bold mt-0.5">&bull;</span>
                    <span><strong>Clinical GTM &amp; Outreach:</strong> Orchestrated targeted institutional outreach to 496+ hospital clinicians with 0 hard bounces.</span>
                  </li>
                </ul>
              </div>

              <!-- Role 2: Ditto Insurance -->
              <div class="relative group">
                <span class="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-indigo-600 ring-4 ring-indigo-100"></span>
                <div class="flex flex-wrap items-center justify-between gap-1 mb-1">
                  <span class="text-xs font-bold text-indigo-600">Aug 2026 &mdash; Present</span>
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">Insurtech &bull; Advisory</span>
                </div>
                <h3 class="text-lg font-extrabold text-slate-900 font-heading">Insurance Advisor</h3>
                <h4 class="text-xs font-bold text-slate-500 mb-2">Ditto Insurance (by Finshots) &bull; Remote</h4>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-2.5">
                  Conduct structured medical profiling and high-intent 1:1 advisory for consumers on health insurance policy structures, underwriting parameters, and coverage limits.
                </p>
                <ul class="space-y-1.5 text-xs text-slate-600">
                  <li class="flex items-start gap-2">
                    <span class="text-indigo-600 font-bold mt-0.5">&bull;</span>
                    <span><strong>Structured Medical Profiling:</strong> Accurately capture health history and pre-existing conditions to evaluate insurer underwriting decisions and loaded premiums.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-indigo-600 font-bold mt-0.5">&bull;</span>
                    <span><strong>Policy Interpretation &amp; Guidance:</strong> Demystify waiting periods, room-rent capping, co-pay clauses, and exclusion policies across top Indian insurers.</span>
                  </li>
                </ul>
              </div>

              <!-- Role 3: Discover India Program -->
              <div class="relative group">
                <span class="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-cyan-600 ring-4 ring-cyan-100"></span>
                <div class="flex flex-wrap items-center justify-between gap-1 mb-1">
                  <span class="text-xs font-bold text-cyan-700">Aug 2024 &mdash; May 2025</span>
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-cyan-50 text-cyan-700 border border-cyan-200">Leadership &bull; Field Research</span>
                </div>
                <h3 class="text-lg font-extrabold text-slate-900 font-heading">Group Representative &amp; Research Lead</h3>
                <h4 class="text-xs font-bold text-slate-500 mb-2">Discover India Program &bull; Aurangabad</h4>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                  Led a 14-member cross-functional team through a 10-month field research lifecycle. Coordinated logistics, synthesized large-scale qualitative and quantitative field data into an executive report, and presented final findings to senior academic leadership.
                </p>
              </div>

            </div>
          </div>

          <!-- Right Col: Education & Background -->
          <div class="lg:col-span-5 space-y-8">
            <div>
              <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200">
                Education &amp; Credentials
              </span>
              <h2 class="text-2xl sm:text-3xl font-black text-slate-900 font-heading mt-2">
                Academic Foundation
              </h2>
            </div>

            <!-- College Card -->
            <div class="glass-card p-6 space-y-4 border-2 border-emerald-500/20">
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="text-lg font-bold text-slate-900 font-heading">FLAME University</h3>
                  <p class="text-xs font-bold text-emerald-700">B.A. in Economics &bull; Minor in Applied Mathematics</p>
                  <p class="text-xs text-slate-500">Pune, Maharashtra &bull; 2023 &mdash; 2026</p>
                </div>
                <span class="px-2.5 py-1 rounded-lg text-xs font-black bg-emerald-100 text-emerald-800">B.A.</span>
              </div>
              <p class="text-xs text-slate-600 leading-relaxed">
                Core coursework in Applied Mathematics, Econometrics, Quantitative Statistical Methods, Microeconomics, Game Theory, and Behavioral Economics.
              </p>
              <div class="pt-2 border-t border-slate-200/80 flex flex-wrap gap-1.5">
                <span class="tech-badge">Applied Mathematics</span>
                <span class="tech-badge">Econometrics</span>
                <span class="tech-badge">Statistical Inference</span>
                <span class="tech-badge">Quantitative Modeling</span>
              </div>
            </div>

            <!-- Certifications Card -->
            <div class="glass-card p-5 space-y-3 border border-slate-200">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500">Verified Certifications</h4>
              <ul class="space-y-2 text-xs text-slate-700">
                <li class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                  <span><strong>Python (Basic) Certificate</strong> &mdash; HackerRank</span>
                </li>
                <li class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                  <span><strong>Data Analysis with Python</strong></span>
                </li>
                <li class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                  <span><strong>Google Digital Marketing Certificate</strong></span>
                </li>
              </ul>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- 7. QUANTITATIVE HONORS & AWARDS -->
    <section id="honors" class="py-16 bg-slate-100/70 border-t border-slate-200/80 relative">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="text-center max-w-3xl mx-auto space-y-3 mb-10">
          <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300">
            Distinctions &amp; Records
          </span>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 font-heading">
            Honors &amp; Quantitative Achievements
          </h2>
          <p class="text-sm sm:text-base text-slate-600">
            A track record of computational speed, analytical rigor, and communication excellence.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div class="glass-card p-6 border-2 border-amber-400/30 space-y-3">
            <span class="text-2xl">🏆</span>
            <h3 class="text-base font-extrabold text-slate-900 font-heading">India Book of Records Holder</h3>
            <p class="text-xs font-bold text-amber-800">Fastest Cube Root Calculation</p>
            <p class="text-xs text-slate-600 leading-relaxed">
              Recognized in the India Book of Records for extraordinary mental arithmetic and rapid computational problem-solving.
            </p>
          </div>

          <div class="glass-card p-6 border border-slate-200 space-y-3">
            <span class="text-2xl">🥉</span>
            <h3 class="text-base font-extrabold text-slate-900 font-heading">Bronze Medalist</h3>
            <p class="text-xs font-bold text-blue-700">The Royal Commonwealth Society Essay Competition</p>
            <p class="text-xs text-slate-600 leading-relaxed">
              Awarded Bronze Medal internationally for structured essay composition, global perspective, and articulate reasoning.
            </p>
          </div>

          <div class="glass-card p-6 border border-slate-200 space-y-3">
            <span class="text-2xl">🎯</span>
            <h3 class="text-base font-extrabold text-slate-900 font-heading">Top 10% Finalist</h3>
            <p class="text-xs font-bold text-indigo-700">State-Level Inter-School Mathematics Competition</p>
            <p class="text-xs text-slate-600 leading-relaxed">
              Achieved top decile rank in state-level competitive mathematics testing quantitative analysis, geometry, and algebra.
            </p>
          </div>

        </div>

      </div>
    </section>

    <!-- 8. CONTACT & RECRUITER CTA -->
    <section id="contact" class="py-16 sm:py-24 relative overflow-hidden bg-slate-900 text-white">
      <div class="max-w-5xl mx-auto px-5 sm:px-8 text-center space-y-8 relative z-10">
        
        <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-500/20 text-blue-300 border border-blue-400/30">
          Get In Touch &bull; Fast Response
        </span>

        <h2 class="text-3xl sm:text-5xl font-black font-heading tracking-tight max-w-2xl mx-auto leading-tight">
          Let's Build &amp; Scale Together.
        </h2>

        <p class="text-sm sm:text-base text-slate-300 max-w-xl mx-auto leading-relaxed">
          Open to full-time opportunities in <strong class="text-white">Founder's Office</strong>, <strong class="text-white">Business Analyst</strong>, and <strong class="text-white">Product Operations</strong> roles.
        </p>

        <!-- Action Cards Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto pt-4 text-left">
          
          <!-- Email Card -->
          <div class="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex flex-col justify-between group">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Direct Email</span>
              <span class="block text-sm font-bold text-white mt-1 break-all">mishrasankalp04@gmail.com</span>
            </div>
            <div class="pt-4 flex items-center gap-2">
              <a href="mailto:mishrasankalp04@gmail.com" class="text-xs font-bold text-blue-400 hover:text-blue-300">Send Email &rarr;</a>
              <button type="button" data-copy="mishrasankalp04@gmail.com" data-copy-label="Email" class="text-xs text-slate-400 hover:text-white ml-auto">Copy</button>
            </div>
          </div>

          <!-- Phone Card -->
          <div class="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex flex-col justify-between group">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Phone &amp; WhatsApp</span>
              <span class="block text-sm font-bold text-white mt-1">+91 9140721395</span>
            </div>
            <div class="pt-4 flex items-center gap-2">
              <a href="tel:+919140721395" class="text-xs font-bold text-emerald-400 hover:text-emerald-300">Call Directly &rarr;</a>
              <button type="button" data-copy="+919140721395" data-copy-label="Phone" class="text-xs text-slate-400 hover:text-white ml-auto">Copy</button>
            </div>
          </div>

          <!-- Location & Resume -->
          <div class="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex flex-col justify-between group">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Location &amp; Status</span>
              <span class="block text-sm font-bold text-white mt-1">Lucknow / Pune / Remote</span>
            </div>
            <div class="pt-4 flex items-center gap-2">
              <a href="Resume.pdf" target="_blank" class="text-xs font-bold text-cyan-400 hover:text-cyan-300">Resume PDF &rarr;</a>
            </div>
          </div>

        </div>

        <div class="pt-4 flex items-center justify-center gap-6 text-sm text-slate-400">
          <a href="https://www.linkedin.com/in/sankalp2329/" target="_blank" rel="noopener noreferrer" class="hover:text-white transition flex items-center gap-1.5">
            <span>LinkedIn</span>
          </a>
          <span>&bull;</span>
          <a href="https://github.com/Sankalp232004" target="_blank" rel="noopener noreferrer" class="hover:text-white transition flex items-center gap-1.5">
            <span>GitHub</span>
          </a>
          <span>&bull;</span>
          <a href="https://swasthai-three.vercel.app/" target="_blank" rel="noopener noreferrer" class="hover:text-blue-400 transition flex items-center gap-1.5">
            <span>SwasthAI</span>
          </a>
        </div>

      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-slate-500 text-xs py-8 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p>&copy; 2026 Sankalp Mishra. Built with Clean HTML, Vanilla CSS &amp; JavaScript.</p>
      <p>B.A. Economics, Minor in Applied Mathematics &bull; FLAME University &bull; Founder, SwasthAI</p>
    </div>
  </footer>

  <!-- DYNAMIC STAR CASE STUDY MODAL -->
  <div id="case-study-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modal-dynamic-title">
    <div class="modal-window relative">
      <button type="button" id="modal-close-btn" class="absolute top-4 right-4 p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 transition" aria-label="Close Case Study Modal">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
      <div id="modal-dynamic-content">
        <!-- Injected dynamically via script.js -->
      </div>
    </div>
  </div>

  <!-- 30-SECOND RECRUITER CHEAT SHEET MODAL -->
  <div id="cheat-sheet-modal" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-window relative max-w-2xl">
      <button type="button" id="cheat-sheet-close-btn" class="absolute top-4 right-4 p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 transition" aria-label="Close Cheat Sheet Modal">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>

      <div class="p-6 sm:p-8 space-y-6">
        <div class="border-b border-slate-200 pb-4">
          <span class="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900">30-Second Recruiter Summary</span>
          <h2 class="text-2xl font-black text-slate-900 font-heading mt-2">Sankalp Mishra &mdash; Fast Facts</h2>
          <p class="text-xs text-slate-500 mt-1">Everything you need to know in 30 seconds</p>
        </div>

        <div class="space-y-4 text-xs sm:text-sm text-slate-700">
          
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span class="font-bold text-slate-900 block mb-1">1. Who Am I?</span>
            <p>Economics graduate with a Minor in Applied Mathematics (FLAME University, 2026), Founder of SwasthAI, and Insurance Advisor at Ditto Insurance. India Book of Records Holder (Fastest Cube Root Calculation).</p>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span class="font-bold text-slate-900 block mb-1">2. Top 3 Demonstrated Strengths</span>
            <ul class="space-y-1 text-xs">
              <li>&bull; <strong class="text-slate-900">0-to-1 Product Speed:</strong> Conceived, coded, and deployed SwasthAI OPD triage SaaS with live clinic pilots.</li>
              <li>&bull; <strong class="text-slate-900">Quantitative &amp; Mathematical Rigor:</strong> India Book of Records holder; built regression ($R^2=0.88$) and classification ($81.5\%$) models in Python/SQL.</li>
              <li>&bull; <strong class="text-slate-900">Leadership &amp; Client Advisory:</strong> Advised consumers on health insurance at Ditto and led a 14-member field research team through a 10-month lifecycle.</li>
            </ul>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span class="font-bold text-slate-900 block mb-1">3. Ideal Roles &amp; Availability</span>
            <p>Targeting <strong class="text-blue-600">Founder's Office</strong>, <strong class="text-blue-600">Business Analyst</strong>, and <strong class="text-blue-600">Product Operations</strong>. Immediate availability, open to Lucknow, Pune, Gurgaon, Bangalore, or Remote.</p>
          </div>

        </div>

        <div class="flex items-center justify-between pt-4 border-t border-slate-200">
          <a href="Resume.pdf" target="_blank" class="px-4 py-2 rounded-lg bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 transition">
            Download Resume PDF
          </a>
          <button type="button" data-copy="mishrasankalp04@gmail.com" data-copy-label="Email" class="text-xs font-bold text-slate-600 hover:text-slate-900">
            Copy Email Address
          </button>
        </div>

      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toast-container"></div>

  <!-- JAVASCRIPT LOGIC -->
  <script src="script.js"></script>
</body>
</html>
"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("[OK] Generated upgraded index.html with LinkedIn Profile enhancements")
