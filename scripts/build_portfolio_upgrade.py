"""
Generate complete index.html for Sankalp Mishra's portfolio
"""
import os

PORTFOLIO_DIR = r"C:\Users\home\OneDrive\Desktop\Job\Portfolio"
INDEX_PATH = os.path.join(PORTFOLIO_DIR, "index.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Primary SEO Meta Tags -->
  <title>Sankalp Mishra — Business Analyst & Strategy | Founder's Office & Product Operations</title>
  <meta name="title" content="Sankalp Mishra — Business Analyst & Strategy | Founder's Office & Product Operations" />
  <meta name="description" content="Economics graduate from FLAME University and Founder of SwasthAI. Specializing in Founder's Office, Business Analysis, Product Operations, and Data-Driven Strategy." />
  <meta name="keywords" content="Business Analyst, Strategy, Product Operations, Founder's Office, Business Analytics, Economics, Product Management, Sankalp Mishra, SwasthAI" />
  <meta name="author" content="Sankalp Mishra" />

  <!-- Open Graph / LinkedIn / Facebook -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://sankalp232004.github.io/Portfolio/" />
  <meta property="og:title" content="Sankalp Mishra — Business Analyst & Strategy Portfolio" />
  <meta property="og:description" content="Economics graduate from FLAME University & Founder of SwasthAI. Solving complex operational bottlenecks through analytics, product thinking, and 0-to-1 execution." />
  <meta property="og:image" content="Photo.jpeg" />

  <!-- Twitter Card -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://sankalp232004.github.io/Portfolio/" />
  <meta property="twitter:title" content="Sankalp Mishra — Business Analyst & Strategy Portfolio" />
  <meta property="twitter:description" content="Economics graduate from FLAME University & Founder of SwasthAI. Solving complex operational bottlenecks through analytics, product thinking, and 0-to-1 execution." />
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
    "alumniOf": {
      "@type": "EducationalOrganization",
      "name": "FLAME University"
    },
    "knowsAbout": [
      "Business Analysis",
      "Product Strategy",
      "Product Operations",
      "Founder's Office",
      "Business Analytics",
      "Economics",
      "SQL",
      "Python",
      "GTM Strategy"
    ],
    "sameAs": [
      "https://www.linkedin.com/in/sankalp2329/",
      "https://github.com/Sankalp232004"
    ]
  }
  </script>

  <!-- TailwindCSS & Custom Design System -->
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
  <div class="mesh-glow mesh-glow-cyan w-[500px] h-[500px] top-[400px] right-[-150px]"></div>
  <div class="mesh-glow mesh-glow-purple w-[650px] h-[650px] top-[1800px] left-[-200px]"></div>

  <!-- STICKY GLASS NAVIGATION BAR -->
  <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-200/80 transition-all duration-300">
    <nav class="max-w-7xl mx-auto px-5 sm:px-8 py-3.5 flex items-center justify-between">
      <a href="#hero" class="text-lg font-extrabold text-slate-900 tracking-tight hover:text-blue-600 transition-colors flex items-center gap-2.5 group">
        <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 text-white flex items-center justify-center text-xs font-black shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">SM</span>
        <span class="font-heading font-bold text-slate-900 group-hover:text-blue-600 transition-colors">Sankalp Mishra</span>
      </a>

      <!-- Desktop Nav Links -->
      <div class="hidden lg:flex items-center gap-6 text-sm font-medium text-slate-600">
        <a href="#about" class="hover:text-blue-600 transition-colors">About</a>
        <a href="#featured-swasth" class="hover:text-blue-600 transition-colors font-semibold text-blue-600 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
          SwasthAI
        </a>
        <a href="#projects" class="hover:text-blue-600 transition-colors">Projects</a>
        <a href="#skills" class="hover:text-blue-600 transition-colors">Skills</a>
        <a href="#experience" class="hover:text-blue-600 transition-colors">Experience</a>
        <a href="#whyme" class="hover:text-blue-600 transition-colors">Why Me</a>
        <a href="#education" class="hover:text-blue-600 transition-colors">Education</a>
      </div>

      <!-- Quick Action Buttons -->
      <div class="hidden sm:flex items-center gap-2.5">
        <button data-modal-target="recruiter-cheat-modal" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 transition-all flex items-center gap-1.5 shadow-sm">
          <span>⚡</span>
          <span>Recruiter 30s Cheat-sheet</span>
        </button>
        <button data-modal-target="resume-modal" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-all flex items-center gap-1.5 shadow-sm shadow-blue-500/25">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          <span>Resume</span>
        </button>
      </div>

      <!-- Mobile Menu Button -->
      <button id="mobile-menu-toggle" class="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors" aria-label="Toggle navigation">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
      </button>
    </nav>

    <!-- Mobile Dropdown -->
    <div id="mobile-menu" class="hidden lg:hidden bg-white/95 backdrop-blur-xl border-b border-slate-200 px-6 py-4 space-y-3">
      <a href="#about" class="block text-slate-700 font-medium hover:text-blue-600">About</a>
      <a href="#featured-swasth" class="block text-blue-600 font-bold">SwasthAI (Featured Showcase)</a>
      <a href="#projects" class="block text-slate-700 font-medium hover:text-blue-600">Projects</a>
      <a href="#skills" class="block text-slate-700 font-medium hover:text-blue-600">Skills</a>
      <a href="#experience" class="block text-slate-700 font-medium hover:text-blue-600">Experience</a>
      <a href="#whyme" class="block text-slate-700 font-medium hover:text-blue-600">Why Me</a>
      <a href="#education" class="block text-slate-700 font-medium hover:text-blue-600">Education</a>
      <div class="pt-3 border-t border-slate-100 flex flex-col gap-2">
        <button data-modal-target="recruiter-cheat-modal" class="w-full text-center py-2 text-xs font-semibold rounded-lg bg-amber-50 text-amber-800 border border-amber-200">⚡ Recruiter 30s Cheat-sheet</button>
        <button data-modal-target="resume-modal" class="w-full text-center py-2 text-xs font-semibold rounded-lg bg-blue-600 text-white">📄 View Resume</button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="flex-grow">

    <!-- HERO SECTION -->
    <section id="hero" class="relative pt-12 pb-16 md:pt-20 md:pb-24 overflow-hidden">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 relative z-10">
        
        <!-- Live Status Pill -->
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-semibold mb-6 shadow-xs">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>Open to Full-Time Roles &bull; Founder's Office &bull; Business Analyst &bull; Product Operations</span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <!-- Left Column: Copy & CTAs -->
          <div class="lg:col-span-7 space-y-6">
            <div class="space-y-2">
              <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-slate-950 font-heading tracking-tight leading-[1.1]">
                Hi, I'm <span class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 bg-clip-text text-transparent">Sankalp Mishra</span>
              </h1>
              <div class="text-xl sm:text-2xl font-bold text-slate-700 flex items-center gap-2 h-9">
                <span class="text-slate-500 font-normal">Focused on:</span>
                <span id="typing-role" class="text-blue-600 font-heading typing-cursor"></span>
              </div>
            </div>

            <p class="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl">
              Economics graduate from <strong class="text-slate-800 font-semibold">FLAME University</strong> and Founder of <strong class="text-blue-600 font-semibold">SwasthAI</strong>. I bridge quantitative data analytics, business intuition, and 0-to-1 operational execution to turn ambiguous problems into streamlined, high-growth systems.
            </p>

            <!-- Quick Impact Metric Strip -->
            <div id="impact-metrics" class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
              <div class="stat-metric-card">
                <div class="text-2xl sm:text-3xl font-black text-blue-600 font-heading counter-val" data-target="450" data-suffix="+">450+</div>
                <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Clinics Reached</div>
              </div>
              <div class="stat-metric-card">
                <div class="text-2xl sm:text-3xl font-black text-indigo-600 font-heading counter-val" data-target="98.2" data-suffix="%" data-decimals="1">98.2%</div>
                <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Model Accuracy</div>
              </div>
              <div class="stat-metric-card">
                <div class="text-2xl sm:text-3xl font-black text-emerald-600 font-heading counter-val" data-target="0" data-prefix="" data-suffix=" Bounces">0</div>
                <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Hard Bounces</div>
              </div>
              <div class="stat-metric-card">
                <div class="text-2xl sm:text-3xl font-black text-cyan-600 font-heading counter-val" data-target="5" data-suffix="+">5+</div>
                <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Core Projects</div>
              </div>
            </div>

            <!-- Primary CTAs -->
            <div class="flex flex-wrap items-center gap-3.5 pt-3">
              <a href="#featured-swasth" class="btn-primary px-6 py-3 rounded-xl text-sm font-semibold flex items-center gap-2">
                <span>Explore SwasthAI Case Study</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </a>
              <button data-modal-target="resume-modal" class="btn-secondary px-5 py-3 rounded-xl text-sm font-semibold flex items-center gap-2">
                <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <span>View Resume</span>
              </button>
              <button class="copy-email-btn px-4 py-3 rounded-xl text-sm font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors flex items-center gap-2 border border-slate-200">
                <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                <span>Copy Email</span>
              </button>
            </div>
          </div>

          <!-- Right Column: Profile Card & Quick Info -->
          <div class="lg:col-span-5 flex justify-center">
            <div class="relative w-full max-w-md">
              <div class="glass-panel p-6 sm:p-7 rounded-3xl relative z-10 border border-slate-200/90 shadow-xl">
                <div class="flex items-center gap-5 mb-5">
                  <img src="Photo.jpeg" alt="Sankalp Mishra" class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-cover border-2 border-white shadow-md ring-4 ring-blue-50" />
                  <div>
                    <h3 class="text-xl font-bold text-slate-900 font-heading">Sankalp Mishra</h3>
                    <p class="text-sm font-medium text-blue-600">Founder &bull; Business Analyst</p>
                    <p class="text-xs text-slate-500 mt-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      India (Available for Relocation)
                    </p>
                    <div class="flex items-center gap-2 mt-2.5">
                      <a href="https://www.linkedin.com/in/sankalp2329/" target="_blank" rel="noopener noreferrer" class="p-1.5 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white transition-all shadow-xs" title="LinkedIn Profile">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                      </a>
                      <a href="https://github.com/Sankalp232004" target="_blank" rel="noopener noreferrer" class="p-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-900 hover:text-white transition-all shadow-xs" title="GitHub Profile">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                      </a>
                      <a href="mailto:mishrasankalp04@gmail.com" class="p-1.5 rounded-lg bg-emerald-50 text-emerald-700 hover:bg-emerald-600 hover:text-white transition-all shadow-xs" title="Send Email">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                      </a>
                    </div>
                  </div>
                </div>

                <div class="space-y-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
                  <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-500 uppercase">Education</span>
                    <span class="font-bold text-slate-800">B.A. Economics, FLAME University</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-500 uppercase">Core Stack</span>
                    <span class="font-bold text-slate-800">SQL &bull; Python &bull; Analytics &bull; GTM</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-500 uppercase">Current Venture</span>
                    <span class="font-bold text-blue-600">Founder, SwasthAI</span>
                  </div>
                </div>

                <div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span class="text-xs font-semibold text-slate-500">Contact:</span>
                  <span class="font-mono text-xs font-semibold text-slate-800">mishrasankalp04@gmail.com</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- RECRUITER ROLE LENS / ROLE MATCHER (HIGH-IMPACT HIRING FEATURE) -->
    <section id="recruiter-lens" class="py-8 bg-white border-y border-slate-200/80 sticky top-[61px] z-40 shadow-xs">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Interactive Recruiter Lens:</span>
            <h2 class="text-base font-bold text-slate-900 font-heading">Filter Profile for Your Target Role:</h2>
          </div>

          <!-- Role Selector Buttons -->
          <div class="flex flex-wrap items-center gap-2">
            <button data-role="all" class="role-tab-btn active px-3.5 py-1.5 rounded-lg text-xs font-bold border border-slate-200">
              🚀 All-Rounder
            </button>
            <button data-role="founders_office" class="role-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-bold border border-slate-200 bg-white text-slate-700 hover:border-blue-400">
              🎯 Founder's Office
            </button>
            <button data-role="business_analyst" class="role-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-bold border border-slate-200 bg-white text-slate-700 hover:border-blue-400">
              📊 Business Analyst
            </button>
            <button data-role="product_ops" class="role-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-bold border border-slate-200 bg-white text-slate-700 hover:border-blue-400">
              ⚙️ Product Operations
            </button>
          </div>
        </div>

        <!-- Dynamic Role Summary Banner -->
        <div id="role-summary-box" class="mt-4 p-4 rounded-xl bg-gradient-to-r from-blue-50/80 via-indigo-50/50 to-slate-50 border border-blue-100 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div class="space-y-0.5">
            <span id="role-summary-title" class="text-sm font-bold text-blue-900 font-heading">Full Cross-Functional Profile</span>
            <p id="role-summary-desc" class="text-xs text-slate-600 leading-relaxed">Combines 0-to-1 founder ownership, rigorous economics & data modeling, and hands-on B2B operations.</p>
          </div>
          <div class="shrink-0 flex items-center gap-2">
            <span class="text-xs font-semibold text-slate-500">Alignment:</span>
            <span id="role-match-score" class="px-2.5 py-1 rounded-md bg-blue-600 text-white font-mono text-xs font-bold shadow-xs">100% Fit</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ABOUT SECTION -->
    <section id="about" class="py-16 md:py-24">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        <div class="max-w-3xl mb-12">
          <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Background & Philosophy</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">About Me</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="glass-panel p-7 rounded-2xl space-y-3 role-spotlight" data-roles="founders_office product_ops all">
            <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-lg">🎯</div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">0-to-1 Founder Mindset</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              As Founder of SwasthAI, I didn't wait for a manual. I led clinician user discovery, designed clinical triage algorithms, mapped OPD clinic bottlenecks, and engineered automated B2B outreach infrastructure reaching 450+ healthcare facilities.
            </p>
          </div>

          <div class="glass-panel p-7 rounded-2xl space-y-3 role-spotlight" data-roles="business_analyst analytics all">
            <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-lg">📊</div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Quantitative & Economic Rigor</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Trained in Economics at FLAME University with heavy coursework in Econometrics, Statistics, and Data Science. Skilled in translating messy raw numbers into clear cohort retentions, unit economics, and data-backed executive recommendations.
            </p>
          </div>

          <div class="glass-panel p-7 rounded-2xl space-y-3 role-spotlight" data-roles="product_ops strategy all">
            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-lg">⚙️</div>
            <h3 class="text-lg font-bold text-slate-900 font-heading">Product Operations & Execution</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Experienced in structuring end-to-end customer advisory funnels (Ditto by Finshots), designing API integrations, writing clear PRDs, and ensuring zero-friction cross-functional execution between tech, ops, and business stakeholders.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURED SHOWCASE: SWASTHAI (0-TO-1 VENTURE DEEP DIVE) -->
    <section id="featured-swasth" class="py-16 md:py-24 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900 text-white relative overflow-hidden">
      <div class="mesh-glow mesh-glow-blue w-[700px] h-[700px] top-[-100px] right-[-200px] opacity-20"></div>
      
      <div class="max-w-7xl mx-auto px-5 sm:px-8 relative z-10">
        
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-bold uppercase tracking-wider mb-3">
              <span>🌟 Primary Founder Case Study</span>
            </div>
            <h2 class="text-3xl sm:text-5xl font-black font-heading text-white tracking-tight">SwasthAI — Clinic Operations Platform</h2>
          </div>
          <a href="https://swasthai-three.vercel.app/" target="_blank" rel="noopener noreferrer" class="btn-primary px-5 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-2 shrink-0">
            <span>Visit Live Platform</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          </a>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          <!-- Narrative & Architecture -->
          <div class="lg:col-span-7 bg-slate-800/80 backdrop-blur-xl border border-slate-700/80 p-7 sm:p-9 rounded-3xl space-y-6">
            <div>
              <h3 class="text-xl font-bold text-white font-heading">The Operational Problem</h3>
              <p class="text-slate-300 text-sm leading-relaxed mt-2">
                In Indian outpatient clinics (OPD), counter registration is digitized via ABDM QR codes (4 minutes), but patients still wait <strong class="text-white">50 to 180 minutes</strong> to see the doctor for a 2-4 minute consultation. When acute walk-ins arrive amidst scheduled appointments, non-clinical receptionists make stressful informal guesses on who goes first.
              </p>
            </div>

            <div>
              <h3 class="text-xl font-bold text-white font-heading">The SwasthAI Solution</h3>
              <p class="text-slate-300 text-sm leading-relaxed mt-2">
                Patients scan a waiting-room QR code and answer structured triage questions on their smartphone. SwasthAI's rule engine generates a recommended clinical priority order on the doctor's screen, while leaving the physician in 100% control with one-click override.
              </p>
            </div>

            <div>
              <h3 class="text-xl font-bold text-white font-heading">GTM & Outbound Automation Engine</h3>
              <p class="text-slate-300 text-sm leading-relaxed mt-2">
                Engineered an automated research-driven B2B cold outreach engine via Brevo Transactional API across 5 distinct campaign angles. Validated DNS MX records live on all recipient domains to achieve <strong class="text-emerald-400">0 hard bounces across 450+ verified institutional clinic targets</strong>.
              </p>
            </div>

            <div class="pt-2 flex flex-wrap gap-2">
              <span class="px-3 py-1 rounded-md bg-slate-700/60 border border-slate-600 text-slate-300 text-xs font-mono">Next.js</span>
              <span class="px-3 py-1 rounded-md bg-slate-700/60 border border-slate-600 text-slate-300 text-xs font-mono">TypeScript</span>
              <span class="px-3 py-1 rounded-md bg-slate-700/60 border border-slate-600 text-slate-300 text-xs font-mono">Python (FastAPI)</span>
              <span class="px-3 py-1 rounded-md bg-slate-700/60 border border-slate-600 text-slate-300 text-xs font-mono">Brevo Transactional API</span>
              <span class="px-3 py-1 rounded-md bg-slate-700/60 border border-slate-600 text-slate-300 text-xs font-mono">Supabase SQL</span>
            </div>
          </div>

          <!-- Key Metrics & Breakdown -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-4">
            <div class="bg-gradient-to-br from-blue-900/40 to-indigo-900/40 border border-blue-500/30 p-6 rounded-3xl space-y-4">
              <h4 class="text-base font-bold text-white font-heading flex items-center gap-2">
                <span>📈</span>
                <span>Verified Impact Metrics</span>
              </h4>
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50">
                  <div class="text-2xl font-black text-blue-400 font-heading">450+</div>
                  <div class="text-xs text-slate-400 mt-0.5">Verified Clinics Reached</div>
                </div>
                <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50">
                  <div class="text-2xl font-black text-emerald-400 font-heading">0%</div>
                  <div class="text-xs text-slate-400 mt-0.5">Hard Bounce Rate</div>
                </div>
                <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50">
                  <div class="text-2xl font-black text-cyan-400 font-heading">10</div>
                  <div class="text-xs text-slate-400 mt-0.5">Indian Metro Hubs</div>
                </div>
                <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50">
                  <div class="text-2xl font-black text-purple-400 font-heading">5</div>
                  <div class="text-xs text-slate-400 mt-0.5">Tested Campaign Angles</div>
                </div>
              </div>
            </div>

            <div class="bg-slate-800/80 border border-slate-700/80 p-6 rounded-3xl space-y-3">
              <h4 class="text-base font-bold text-white font-heading">What this proves to a hirer:</h4>
              <ul class="text-xs text-slate-300 space-y-2">
                <li class="flex items-start gap-2">
                  <span class="text-emerald-400 font-bold">&check;</span>
                  <span><strong>Product Thinking:</strong> Identified a structural healthcare bottleneck beyond simple surface problems.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-400 font-bold">&check;</span>
                  <span><strong>Technical & Data Execution:</strong> Built rule algorithms, API pipelines, and transactional delivery infrastructure.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-400 font-bold">&check;</span>
                  <span><strong>GTM Ownership:</strong> Executed systematic outreach without relying on generic sales tactics.</span>
                </li>
              </ul>
              <button data-modal-target="swasth-modal" class="w-full mt-2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition-colors text-center">
                View Full STAR Case Study Breakdown &rarr;
              </button>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- PROJECTS & CASE STUDIES SECTION -->
    <section id="projects" class="py-16 md:py-24">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Case Studies & Technical Projects</span>
            <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">Featured Projects</h2>
          </div>

          <!-- Project Filter Pills -->
          <div class="flex flex-wrap items-center gap-2">
            <button data-filter="all" class="project-filter-btn px-3.5 py-1.5 rounded-lg text-xs font-bold bg-blue-600 text-white">All</button>
            <button data-filter="strategy" class="project-filter-btn px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:border-blue-400">Business & Strategy</button>
            <button data-filter="analytics" class="project-filter-btn px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:border-blue-400">Analytics & ML</button>
            <button data-filter="operations" class="project-filter-btn px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:border-blue-400">Operations</button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">

          <!-- PROJECT 1: SWASTHAI RISK ANALYZER -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="strategy" data-roles="founders_office strategy all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-blue">Healthcare &bull; Product Strategy</span>
                <span class="font-mono text-xs text-slate-400">2026</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">SwasthAI — Triage Risk Analysis</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Risk-based clinical triage model assessing emergency severity, patient vital stability, and queue sequencing rules with 98.2% discrimination score.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Python</span>
                <span class="badge-pill badge-slate text-[10px]">Rule Engine</span>
                <span class="badge-pill badge-slate text-[10px]">Clinical Triage</span>
                <span class="badge-pill badge-slate text-[10px]">Next.js</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button data-modal-target="modal-swasth-risk" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <a href="https://github.com/Sankalp232004/SwasthAI-Triage-Analyzer" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-slate-700 transition-colors" title="GitHub Repository">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
            </div>
          </div>

          <!-- PROJECT 2: HEALTHCARE COST PREDICTOR -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="analytics" data-roles="business_analyst analytics all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-emerald">Predictive ML &bull; Econometrics</span>
                <span class="font-mono text-xs text-slate-400">2026</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Healthcare Cost Predictor</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Regression-based cost estimation model identifying premium cost drivers, demographic risks, and smoker multipliers with 0.88 R² predictive accuracy.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Python</span>
                <span class="badge-pill badge-slate text-[10px]">Scikit-Learn</span>
                <span class="badge-pill badge-slate text-[10px]">Linear Regression</span>
                <span class="badge-pill badge-slate text-[10px]">Pandas</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button data-modal-target="modal-health-cost" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <a href="https://github.com/Sankalp232004/Healthcare_Cost_Predictor" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-slate-700 transition-colors" title="GitHub Repository">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
            </div>
          </div>

          <!-- PROJECT 3: IPL MATCH OUTCOME -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="analytics" data-roles="business_analyst analytics all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-purple">Sports Analytics &bull; EDA</span>
                <span class="font-mono text-xs text-slate-400">2026</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">IPL Match Outcome Analysis</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Comprehensive exploratory data analysis analyzing toss impact, venue advantages, and win probability matrices across 1000+ historical IPL encounters.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Python</span>
                <span class="badge-pill badge-slate text-[10px]">EDA</span>
                <span class="badge-pill badge-slate text-[10px]">Matplotlib</span>
                <span class="badge-pill badge-slate text-[10px]">Seaborn</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button data-modal-target="modal-ipl" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <a href="https://github.com/Sankalp232004/IPLanalysis" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-slate-700 transition-colors" title="GitHub Repository">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
            </div>
          </div>

          <!-- PROJECT 4: STARTUP FUNDING ANALYSIS -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="strategy" data-roles="founders_office strategy all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-blue">Venture Capital &bull; Market Research</span>
                <span class="font-mono text-xs text-slate-400">2026</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Startup Funding Ecosystem</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Quantitative breakdown of Indian startup deal volume, stage-wise ticket sizes, sector momentum (Fintech/Healthtech), and investor syndicates.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Python</span>
                <span class="badge-pill badge-slate text-[10px]">Market Sizing</span>
                <span class="badge-pill badge-slate text-[10px]">Data Visualization</span>
                <span class="badge-pill badge-slate text-[10px]">VC Trends</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button data-modal-target="modal-startup-funding" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <a href="https://github.com/Sankalp232004/data-science-learning-log" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-slate-700 transition-colors" title="GitHub Repository">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
            </div>
          </div>

          <!-- PROJECT 5: RETAIL CUSTOMER CHURN -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="operations" data-roles="business_analyst product_ops all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-emerald">Cohort Retention &bull; Ops</span>
                <span class="font-mono text-xs text-slate-400">2026</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Retail Customer Churn Analysis</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Classification model uncovering primary triggers for customer attrition, RFM segmentation, and retention intervention strategies.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Python</span>
                <span class="badge-pill badge-slate text-[10px]">RFM Segmentation</span>
                <span class="badge-pill badge-slate text-[10px]">Churn Modeling</span>
                <span class="badge-pill badge-slate text-[10px]">SQL</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button data-modal-target="modal-retail-churn" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View Case Study</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <a href="https://github.com/Sankalp232004/retail-customer-churn" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-slate-700 transition-colors" title="GitHub Repository">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
            </div>
          </div>

          <!-- PROJECT 6: LEARNING & CODE BASE -->
          <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between project-item role-spotlight" data-category="analytics" data-roles="business_analyst analytics all">
            <div class="p-6 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-pill badge-purple">Data Science &bull; Codebase</span>
                <span class="font-mono text-xs text-slate-400">Ongoing</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Data Science & SQL Learning Log</h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Repository of advanced SQL queries, econometric scripts, data pipelines, statistical hypothesis tests, and data cleaning routines.
              </p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span class="badge-pill badge-slate text-[10px]">Advanced SQL</span>
                <span class="badge-pill badge-slate text-[10px]">Pandas</span>
                <span class="badge-pill badge-slate text-[10px]">Statistical Testing</span>
              </div>
            </div>
            <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <a href="https://github.com/Sankalp232004/data-science-learning-log" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1">
                <span>View GitHub Repository</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </a>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- SKILLS MATRIX WITH REAL-WORLD PROOF POINTS -->
    <section id="skills" class="py-16 md:py-24 bg-slate-100/60 border-y border-slate-200/80">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="max-w-3xl mb-12">
          <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Core Competencies</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">Skills & Tooling Matrix</h2>
          <p class="text-slate-600 text-sm mt-2">Grouped by business application with concrete real-world implementation proof points.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <!-- Skill Card 1: Business & Strategy -->
          <div class="glass-panel p-6 rounded-2xl space-y-4 role-spotlight" data-roles="founders_office strategy all">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">🎯</div>
              <h3 class="font-bold text-slate-900 font-heading">Business & Strategy</h3>
            </div>
            <ul class="space-y-2.5 text-xs text-slate-700">
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">GTM Strategy & Outbound</strong>
                <span class="text-slate-500">Applied in SwasthAI 450+ clinic campaign</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Market Sizing (TAM/SAM/SOM)</strong>
                <span class="text-slate-500">Applied in Healthcare clinic research</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Competitor Benchmarking</strong>
                <span class="text-slate-500">Analyzed EMR & triage solutions in India</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Founder's Office Operations</strong>
                <span class="text-slate-500">Cross-functional execution & prioritization</span>
              </li>
            </ul>
          </div>

          <!-- Skill Card 2: Analytics & Data -->
          <div class="glass-panel p-6 rounded-2xl space-y-4 role-spotlight" data-roles="business_analyst analytics all">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold">📊</div>
              <h3 class="font-bold text-slate-900 font-heading">Analytics & Data</h3>
            </div>
            <ul class="space-y-2.5 text-xs text-slate-700">
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Advanced SQL & Aggregations</strong>
                <span class="text-slate-500">Window functions, CTEs, complex joins</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Python (Pandas, NumPy, Scikit)</strong>
                <span class="text-slate-500">Applied in Healthcare & Churn modeling</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Cohort & Retention Analysis</strong>
                <span class="text-slate-500">RFM segmentation, churn propensity</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Data Storytelling & KPIs</strong>
                <span class="text-slate-500">Translating raw data into executive insights</span>
              </li>
            </ul>
          </div>

          <!-- Skill Card 3: Product & Operations -->
          <div class="glass-panel p-6 rounded-2xl space-y-4 role-spotlight" data-roles="product_ops operations all">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">⚙️</div>
              <h3 class="font-bold text-slate-900 font-heading">Product & Operations</h3>
            </div>
            <ul class="space-y-2.5 text-xs text-slate-700">
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Workflow Mapping & SOPs</strong>
                <span class="text-slate-500">OPD intake & clinic queue optimization</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">PRD & User Story Writing</strong>
                <span class="text-slate-500">Doctor-in-the-loop prioritization rules</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">API & Email Infrastructure</strong>
                <span class="text-slate-500">Brevo REST API, DNS MX validation gates</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Customer Advisory Operations</strong>
                <span class="text-slate-500">Trained advisor at Ditto by Finshots</span>
              </li>
            </ul>
          </div>

          <!-- Skill Card 4: Quantitative Economics -->
          <div class="glass-panel p-6 rounded-2xl space-y-4 role-spotlight" data-roles="business_analyst economics all">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center font-bold">📈</div>
              <h3 class="font-bold text-slate-900 font-heading">Quantitative Economics</h3>
            </div>
            <ul class="space-y-2.5 text-xs text-slate-700">
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Econometric Modeling</strong>
                <span class="text-slate-500">Linear/logistic regression & causation</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Statistical Hypothesis Testing</strong>
                <span class="text-slate-500">p-values, confidence intervals, A/B testing</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Pricing Elasticity & Cost Modeling</strong>
                <span class="text-slate-500">Health insurance & SaaS pricing curves</span>
              </li>
              <li class="p-2 rounded-lg bg-slate-50 border border-slate-100">
                <strong class="block text-slate-900">Labor Market Research</strong>
                <span class="text-slate-500">Primary research with WageIndicator</span>
              </li>
            </ul>
          </div>

        </div>

      </div>
    </section>

    <!-- EXPERIENCE & LEADERSHIP TIMELINE -->
    <section id="experience" class="py-16 md:py-24">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="max-w-3xl mb-14">
          <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Track Record</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">Professional Experience</h2>
        </div>

        <div class="relative pl-6 md:pl-0 space-y-8">
          
          <!-- STEM LINE -->
          <div class="timeline-stem"></div>

          <!-- EXP 1: SWASTHAI -->
          <div class="relative timeline-item md:grid md:grid-cols-2 md:gap-12 items-center role-spotlight" data-roles="founders_office strategy product_ops all">
            <div class="md:text-right space-y-1">
              <span class="badge-pill badge-blue">Jan 2026 — Present</span>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Founder &amp; Product Lead</h3>
              <p class="text-sm font-semibold text-blue-600">SwasthAI &bull; Healthcare Operations</p>
            </div>
            <div class="timeline-bullet absolute -left-[31px] md:left-1/2 md:-translate-x-1/2 top-4 md:top-auto"></div>
            <div class="mt-4 md:mt-0 glass-panel p-6 rounded-2xl space-y-2.5">
              <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed">
                <li>Conducted customer discovery with 40+ clinicians to identify the critical post-registration waiting room bottleneck.</li>
                <li>Designed and built a rule-assisted clinical intake prioritization engine in Next.js, Python, and Supabase SQL.</li>
                <li>Engineered an automated B2B outbound campaign delivering 450+ verified clinic emails across 10 metro cities with 0 hard bounces and 100% DNS MX verification.</li>
              </ul>
            </div>
          </div>

          <!-- EXP 2: DITTO BY FINSHOTS -->
          <div class="relative timeline-item md:grid md:grid-cols-2 md:gap-12 items-center role-spotlight" data-roles="product_ops business_analyst all">
            <div class="md:order-2 space-y-1">
              <span class="badge-pill badge-emerald">Oct 2025 — Dec 2025</span>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Insurance Advisor</h3>
              <p class="text-sm font-semibold text-emerald-700">Ditto by Finshots &bull; Financial Advisory</p>
            </div>
            <div class="timeline-bullet absolute -left-[31px] md:left-1/2 md:-translate-x-1/2 top-4 md:top-auto"></div>
            <div class="md:order-1 mt-4 md:mt-0 glass-panel p-6 rounded-2xl space-y-2.5 md:text-right">
              <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed md:list-none">
                <li>Analyzed complex health and life insurance policies to provide transparent, spam-free financial guidance to 200+ clients.</li>
                <li>Translated complex policy wordings, exclusions, and claim settlement ratios into actionable customer comparisons.</li>
                <li>Consistently maintained a 95%+ client satisfaction score through objective, consultative communication.</li>
              </ul>
            </div>
          </div>

          <!-- EXP 3: RESOLUTE AI -->
          <div class="relative timeline-item md:grid md:grid-cols-2 md:gap-12 items-center role-spotlight" data-roles="business_analyst strategy all">
            <div class="md:text-right space-y-1">
              <span class="badge-pill badge-purple">Apr 2024 — Jun 2024</span>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Business Development Associate</h3>
              <p class="text-sm font-semibold text-purple-700">ResoluteAI &bull; Enterprise AI Solutions</p>
            </div>
            <div class="timeline-bullet absolute -left-[31px] md:left-1/2 md:-translate-x-1/2 top-4 md:top-auto"></div>
            <div class="mt-4 md:mt-0 glass-panel p-6 rounded-2xl space-y-2.5">
              <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed">
                <li>Conducted market research across enterprise AI applications and computer vision deployment in industrial settings.</li>
                <li>Built structured prospect lists, qualified inbound leads, and mapped B2B sales funnels for deep-tech offerings.</li>
              </ul>
            </div>
          </div>

          <!-- EXP 4: DISCOVER INDIA -->
          <div class="relative timeline-item md:grid md:grid-cols-2 md:gap-12 items-center role-spotlight" data-roles="strategy all">
            <div class="md:order-2 space-y-1">
              <span class="badge-pill badge-slate">2023 — 2024</span>
              <h3 class="text-xl font-bold text-slate-900 font-heading">News Analyst &amp; Correspondent</h3>
              <p class="text-sm font-semibold text-slate-700">Discover India &bull; Media &amp; Policy</p>
            </div>
            <div class="timeline-bullet absolute -left-[31px] md:left-1/2 md:-translate-x-1/2 top-4 md:top-auto"></div>
            <div class="md:order-1 mt-4 md:mt-0 glass-panel p-6 rounded-2xl space-y-2.5 md:text-right">
              <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed md:list-none">
                <li>Researched economic policy, market trends, and socio-economic developments in Indian states.</li>
                <li>Authored in-depth analytical pieces breaking down complex macroeconomic data into accessible reports.</li>
              </ul>
            </div>
          </div>

          <!-- EXP 5: WAGEINDICATOR -->
          <div class="relative timeline-item md:grid md:grid-cols-2 md:gap-12 items-center role-spotlight" data-roles="business_analyst economics all">
            <div class="md:text-right space-y-1">
              <span class="badge-pill badge-blue">2023</span>
              <h3 class="text-xl font-bold text-slate-900 font-heading">Research Intern</h3>
              <p class="text-sm font-semibold text-blue-600">WageIndicator Foundation &bull; Labor Economics</p>
            </div>
            <div class="timeline-bullet absolute -left-[31px] md:left-1/2 md:-translate-x-1/2 top-4 md:top-auto"></div>
            <div class="mt-4 md:mt-0 glass-panel p-6 rounded-2xl space-y-2.5">
              <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed">
                <li>Collected and analyzed primary data on living wages, labor laws, and minimum wage compliance across India.</li>
                <li>Cleaned and standardized multi-region survey datasets for international economic benchmarking.</li>
              </ul>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- WHY HIRE ME SECTION -->
    <section id="whyme" class="py-16 md:py-24 bg-gradient-to-b from-blue-50/70 via-slate-50 to-blue-50/70 border-t border-slate-200/80">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Hiring Manager Value Proposition</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">Why Hire Sankalp?</h2>
          <p class="text-slate-600 text-sm mt-2">What I uniquely bring to a high-growth Founder's Office, Business Analytics, or Product Operations team.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-7">
          
          <div class="glass-panel p-8 rounded-3xl space-y-4 border border-blue-100 shadow-md">
            <div class="w-12 h-12 rounded-2xl bg-blue-600 text-white flex items-center justify-center text-xl font-bold shadow-md shadow-blue-500/20">01</div>
            <h3 class="text-xl font-bold text-slate-900 font-heading">High Velocity &amp; Ownership</h3>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
              I don't wait for structured SOPs to exist. When building SwasthAI, I handled user research, rule modeling, frontend implementation, and B2B transactional delivery end-to-end. I thrive in 0-to-1 ambiguity.
            </p>
          </div>

          <div class="glass-panel p-8 rounded-3xl space-y-4 border border-indigo-100 shadow-md">
            <div class="w-12 h-12 rounded-2xl bg-indigo-600 text-white flex items-center justify-center text-xl font-bold shadow-md shadow-indigo-500/20">02</div>
            <h3 class="text-xl font-bold text-slate-900 font-heading">Analytical Rigor &amp; Business Sense</h3>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
              My Economics background means I understand causal relationships, incentives, unit economics, and data modeling. I don't just run SQL queries; I translate metrics into strategic commercial moves.
            </p>
          </div>

          <div class="glass-panel p-8 rounded-3xl space-y-4 border border-emerald-100 shadow-md">
            <div class="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center text-xl font-bold shadow-md shadow-emerald-500/20">03</div>
            <h3 class="text-xl font-bold text-slate-900 font-heading">Clear Communication</h3>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Whether explaining health policy exclusions to retail clients at Ditto, presenting pitch decks to clinicians, or drafting technical PRDs, I communicate complex ideas simply, calmly, and persuasively.
            </p>
          </div>

        </div>

      </div>
    </section>

    <!-- EDUCATION SECTION -->
    <section id="education" class="py-16 md:py-20">
      <div class="max-w-7xl mx-auto px-5 sm:px-8">
        
        <div class="max-w-3xl mb-10">
          <span class="text-xs font-bold tracking-wider text-blue-600 uppercase">Academic Background</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-950 font-heading mt-1">Education</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="glass-panel p-7 rounded-2xl space-y-3">
            <div class="flex items-center justify-between">
              <span class="badge-pill badge-blue">2021 — 2024</span>
              <span class="text-xs font-semibold text-slate-500">Pune, India</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 font-heading">FLAME University</h3>
            <p class="text-sm font-semibold text-blue-600">Bachelor of Arts (B.A.) in Economics</p>
            <p class="text-xs text-slate-600 leading-relaxed">
              Coursework in Econometrics, Quantitative Methods, Micro/Macroeconomics, Statistics, and Data Analysis. Active Member of the Placement Committee and Social Media PR Head.
            </p>
          </div>

          <div class="glass-panel p-7 rounded-2xl space-y-3">
            <div class="flex items-center justify-between">
              <span class="badge-pill badge-slate">High School</span>
              <span class="text-xs font-semibold text-slate-500">Lucknow, India</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 font-heading">City Montessori School (CMS)</h3>
            <p class="text-sm font-semibold text-slate-700">ISC Board &bull; Commerce with Mathematics</p>
            <p class="text-xs text-slate-600 leading-relaxed">
              Strong quantitative foundation in Mathematics, Economics, and Accountancy.
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- CTA & CONTACT SECTION -->
    <section id="contact" class="py-16 md:py-24 bg-gradient-to-b from-slate-900 to-slate-950 text-white relative">
      <div class="max-w-4xl mx-auto px-5 sm:px-8 text-center space-y-8 relative z-10">
        
        <div class="space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold border border-blue-500/30">
            <span>🤝 Let's Connect</span>
          </div>
          <h2 class="text-3xl sm:text-5xl font-extrabold font-heading text-white">Ready to drive measurable impact.</h2>
          <p class="text-slate-300 text-sm sm:text-base max-w-xl mx-auto leading-relaxed">
            I am available for immediate full-time opportunities in <strong class="text-white font-semibold">Founder's Office, Business Analysis, Product Operations, and Strategy</strong>.
          </p>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-4 pt-2">
          <a href="mailto:mishrasankalp04@gmail.com" class="btn-primary px-7 py-3.5 rounded-xl text-sm font-semibold flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            <span>Email Sankalp</span>
          </a>
          <button class="copy-email-btn px-6 py-3.5 rounded-xl text-sm font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
            <span>mishrasankalp04@gmail.com</span>
          </button>
          <a href="https://www.linkedin.com/in/sankalp2329/" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-xl text-sm font-semibold bg-[#0077b5] hover:bg-[#006097] text-white transition-colors flex items-center gap-2">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            <span>LinkedIn</span>
          </a>
        </div>

      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-slate-500 text-xs py-8 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>&copy; 2026 Sankalp Mishra. Built for impact &amp; analytical excellence.</div>
      <div class="flex items-center gap-4">
        <a href="#hero" class="hover:text-slate-300 transition-colors">Back to Top &uarr;</a>
      </div>
    </div>
  </footer>

  <!-- ======================================================================
       INTERACTIVE MODALS (STAR CASE STUDIES & RECRUITER TOOLS)
       ====================================================================== -->

  <!-- MODAL 1: RECRUITER 30-SECOND CHEAT SHEET -->
  <div id="recruiter-cheat-modal" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-6 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-4 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-amber-700 uppercase">⚡ 30-Second Candidate Summary</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">Recruiter Executive Brief</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 text-xl font-bold">&times;</button>
      </div>

      <div class="space-y-4 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <div class="p-3.5 rounded-xl bg-blue-50/80 border border-blue-100 space-y-1">
          <strong class="text-blue-900 font-heading font-bold">1. Who is Sankalp?</strong>
          <p class="text-slate-600">Economics graduate from FLAME University and Founder of SwasthAI. Combines quantitative modeling (SQL/Python/Econometrics) with hands-on 0-to-1 operational execution.</p>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
          <strong class="text-slate-900 font-heading font-bold">2. Best Suited Roles:</strong>
          <p class="text-slate-600">&bull; <strong>Founder's Office:</strong> High velocity, handles cross-functional ambiguity, translates strategy into ops.<br>&bull; <strong>Business Analyst:</strong> Advanced SQL, cohort retentions, unit economics, data storytelling.<br>&bull; <strong>Product Operations:</strong> API workflows, clinical rule systems, user funnel optimization.</p>
        </div>

        <div class="p-3.5 rounded-xl bg-emerald-50/80 border border-emerald-100 space-y-1">
          <strong class="text-emerald-900 font-heading font-bold">3. Top Verifiable Achievements:</strong>
          <p class="text-slate-600">&bull; <strong>SwasthAI:</strong> Engineered automated B2B pipeline reaching 450+ verified clinic accounts across India with 0 hard bounces.<br>&bull; <strong>Ditto by Finshots:</strong> Advised 200+ clients maintaining a 95%+ CSAT rating.<br>&bull; <strong>Analytics Projects:</strong> Built predictive models with up to 98.2% accuracy in clinical triage &amp; cost estimation.</p>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
        <button class="copy-email-btn px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700">Copy Email Address</button>
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 2: RESUME PREVIEW MODAL -->
  <div id="resume-modal" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-4xl w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-5 max-h-[92vh] flex flex-col">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-blue-600 uppercase">Official CV</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">Sankalp Mishra — Resume</h3>
        </div>
        <div class="flex items-center gap-2">
          <a href="Resume.pdf" download class="btn-primary px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
            <span>Download PDF</span>
          </a>
          <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 text-xl font-bold">&times;</button>
        </div>
      </div>

      <!-- Embedded PDF / Responsive Container -->
      <div class="flex-grow bg-slate-100 rounded-2xl overflow-hidden border border-slate-200 min-h-[450px]">
        <iframe src="Resume.pdf" class="w-full h-full min-h-[450px]" title="Resume Preview"></iframe>
      </div>
    </div>
  </div>

  <!-- MODAL 3: SWASTHAI STAR CASE STUDY -->
  <div id="swasth-modal" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-3xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-6 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-4 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-blue-600 uppercase">STAR Methodology Case Study</span>
          <h3 class="text-xl sm:text-2xl font-bold text-slate-900 font-heading">SwasthAI — Clinic Triage &amp; Operations</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 text-xl font-bold">&times;</button>
      </div>

      <div class="space-y-4 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <div class="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
          <strong class="text-blue-900 font-heading font-bold">Situation:</strong>
          <p class="text-slate-600">Indian OPDs have fast digital counter registration through ABDM Scan &amp; Register, but the physical waiting queue outside doctor consultation rooms remains unorganized. Patients wait 50-180 minutes for a 3-minute doctor visit.</p>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
          <strong class="text-blue-900 font-heading font-bold">Task:</strong>
          <p class="text-slate-600">Design a lightweight patient intake mechanism that captures clinical acuity prior to consultation without adding administrative burden to front-desk staff or doctors.</p>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
          <strong class="text-blue-900 font-heading font-bold">Action Taken:</strong>
          <p class="text-slate-600">&bull; Developed QR-based symptom questionnaire on patient mobile browsers.<br>&bull; Engineered rule-assisted urgency prioritization on the doctor dashboard with 100% manual override capability.<br>&bull; Built Brevo Transactional outbound engine with concurrent DNS MX checks to validate 450+ clinic leads with 0 bounces.</p>
        </div>

        <div class="p-4 rounded-xl bg-emerald-50/80 border border-emerald-100 space-y-1">
          <strong class="text-emerald-900 font-heading font-bold">Result &amp; Business Impact:</strong>
          <p class="text-slate-600">&bull; Reached 450+ verified clinics across 10 Indian metros.<br>&bull; Achieved 0% hard bounce rate.<br>&bull; Reduced pre-consultation history taking overhead by ~40%.</p>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
        <a href="https://swasthai-three.vercel.app/" target="_blank" rel="noopener noreferrer" class="btn-primary px-4 py-2 rounded-xl text-xs font-semibold">Visit Platform</a>
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 4: HEALTHCARE COST PREDICTOR STAR -->
  <div id="modal-health-cost" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-emerald-700 uppercase">STAR Case Study</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">Healthcare Cost Predictor</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <p><strong>Situation:</strong> Healthcare insurers and patients face unpredictable out-of-pocket expenses due to non-linear cost multipliers.</p>
        <p><strong>Task:</strong> Build a predictive regression model in Python to identify cost drivers and forecast individual medical expenses.</p>
        <p><strong>Action:</strong> Implemented Exploratory Data Analysis, one-hot encoding, and multiple regression models in Scikit-Learn evaluating R² and RMSE metrics.</p>
        <p class="p-3 bg-emerald-50 rounded-xl text-emerald-900 font-medium"><strong>Result:</strong> Achieved 0.88 R² accuracy, pinpointing smoking status and age as the dominant non-linear risk drivers.</p>
      </div>
      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 5: IPL ANALYSIS STAR -->
  <div id="modal-ipl" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-purple-700 uppercase">STAR Case Study</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">IPL Match Outcome Analysis</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <p><strong>Situation:</strong> Complex multivariate sports data contains hidden venue and match dynamics that dictate win probabilities.</p>
        <p><strong>Task:</strong> Perform exploratory data analysis and statistical modeling across 1000+ matches to identify decisive factors.</p>
        <p><strong>Action:</strong> Used Pandas, NumPy, Seaborn, and Matplotlib to analyze toss correlation, pitch wear, and chasing vs defending success rates.</p>
        <p class="p-3 bg-purple-50 rounded-xl text-purple-900 font-medium"><strong>Result:</strong> Identified that venue dew factor and second-innings chasing created a statistically significant 54.3% win advantage.</p>
      </div>
      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 6: STARTUP FUNDING STAR -->
  <div id="modal-startup-funding" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-blue-700 uppercase">STAR Case Study</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">Startup Funding Ecosystem</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <p><strong>Situation:</strong> Venture capital investment trends in India underwent massive sector shifts between 2021 and 2025.</p>
        <p><strong>Task:</strong> Aggregate and analyze deal-level data to map sector momentum, valuations, and check size trends.</p>
        <p><strong>Action:</strong> Built data cleaning and aggregation pipelines in Python, generating market sizing models and investor syndicate maps.</p>
        <p class="p-3 bg-blue-50 rounded-xl text-blue-900 font-medium"><strong>Result:</strong> Delivered a clear visual report showing Seed-to-Series A conversion drop-offs and the rise of HealthTech/DeepTech funding.</p>
      </div>
      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 7: RETAIL CUSTOMER CHURN STAR -->
  <div id="modal-retail-churn" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-emerald-700 uppercase">STAR Case Study</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">Retail Customer Churn Analysis</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <p><strong>Situation:</strong> High customer acquisition costs make churn prevention a critical revenue driver for retail operations.</p>
        <p><strong>Task:</strong> Segment customers and build a predictive churn model to enable proactive retention outreach.</p>
        <p><strong>Action:</strong> Conducted RFM (Recency, Frequency, Monetary) segmentation and trained classification models in Python/Scikit-Learn.</p>
        <p class="p-3 bg-emerald-50 rounded-xl text-emerald-900 font-medium"><strong>Result:</strong> Identified that customers with a 45+ day inactivity threshold had an 82% churn probability, enabling targeted win-back campaigns.</p>
      </div>
      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL 8: SWASTH RISK ANALYZER STAR -->
  <div id="modal-swasth-risk" class="modal-container hidden fixed inset-0 z-50 modal-overlay items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-blue-700 uppercase">STAR Case Study</span>
          <h3 class="text-xl font-bold text-slate-900 font-heading">SwasthAI — Triage Risk Engine</h3>
        </div>
        <button data-modal-close class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <p><strong>Situation:</strong> First-come-first-served token systems treat high-risk acute cases and routine checkups equally.</p>
        <p><strong>Task:</strong> Create an objective clinical scoring algorithm that recommends priority queueing while ensuring zero medical malpractice risk.</p>
        <p><strong>Action:</strong> Developed structured screening questions covering duration, severity, red-flag symptoms, and pediatric fever thresholds.</p>
        <p class="p-3 bg-blue-50 rounded-xl text-blue-900 font-medium"><strong>Result:</strong> Built a 98.2% discrimination score model with full physician override control.</p>
      </div>
      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button data-modal-close class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700">Close</button>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION FOR COPY EMAIL -->
  <div id="toast-notification" class="glass-panel p-4 rounded-2xl shadow-xl flex items-center gap-3 border border-emerald-200 bg-white">
    <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-sm">&check;</div>
    <div>
      <h4 class="text-xs font-bold text-slate-900 font-heading">Email Copied to Clipboard!</h4>
      <p class="text-[11px] text-slate-500 font-mono">mishrasankalp04@gmail.com</p>
    </div>
  </div>

  <!-- SCRIPT INCLUSION -->
  <script src="script.js"></script>
</body>
</html>
"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)
print("[OK] Generated index.html")
