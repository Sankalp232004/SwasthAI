import os
import re
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("SWASTHAI SYSTEM-WIDE ALIGNMENT & INTEGRITY AUDIT")
print("=" * 60)

errors = []
warnings = []

# 1. MDX Blog Files Audit
blog_dir = r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\content\blog"
print(f"\n[1] Auditing MDX Blog Posts in: {blog_dir}")
mdx_files = [f for f in os.listdir(blog_dir) if f.endswith(".mdx") or f.endswith(".md")]
print(f"    Found {len(mdx_files)} blog articles.")

for f in sorted(mdx_files):
    path = os.path.join(blog_dir, f)
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    
    # Frontmatter check
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not fm_match:
        errors.append(f"MDX: {f} has invalid frontmatter boundary.")
        continue
    
    fm_text = fm_match.group(1)
    body = fm_match.group(2)
    
    required_keys = ["title", "publishedAt", "author", "category", "excerpt"]
    for key in required_keys:
        if f"{key}:" not in fm_text:
            errors.append(f"MDX: {f} is missing required frontmatter key '{key}'.")
    
    # Check Callout tag balance
    open_callouts = len(re.findall(r"<Callout\b", body))
    close_callouts = len(re.findall(r"</Callout>", body))
    if open_callouts != close_callouts:
        errors.append(f"MDX: {f} has unmatched <Callout> tags ({open_callouts} open vs {close_callouts} close).")
    
    # Check for unclosed code fences
    fences = len(re.findall(r"^```", body, re.MULTILINE))
    if fences % 2 != 0:
        errors.append(f"MDX: {f} has unclosed code fence (found {fences} ``` markers).")

print(f"    MDX posts audit complete. Checked {len(mdx_files)} files.")

# 2. Sitemap Audit
sitemap_path = r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\public\sitemap.xml"
print(f"\n[2] Auditing Sitemap: {sitemap_path}")
with open(sitemap_path, "r", encoding="utf-8") as fp:
    sitemap_text = fp.read()

for f in mdx_files:
    slug = f.replace(".mdx", "").replace(".md", "")
    expected_url = f"https://swasthai-three.vercel.app/blog/{slug}"
    if expected_url not in sitemap_text:
        warnings.append(f"Sitemap: Post '{slug}' is missing from public/sitemap.xml")

print("    Sitemap audit complete.")

# 3. TSX JSX Integrity Audit
tsx_files = [
    r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\src\app\blog\[slug]\page.tsx",
    r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\src\components\blog\BlogCard.tsx",
    r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\src\components\blog\Callout.tsx",
    r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\src\lib\config.ts"
]

print(f"\n[3] Auditing Core Website TSX/TS Files")
for tf in tsx_files:
    if not os.path.exists(tf):
        errors.append(f"TSX: File not found: {tf}")
        continue
    with open(tf, "r", encoding="utf-8") as fp:
        code = fp.read()
    
    # Basic brace balance check
    open_curlies = code.count("{")
    close_curlies = code.count("}")
    if open_curlies != close_curlies:
        errors.append(f"TSX: {os.path.basename(tf)} has unmatched curly braces ({open_curlies} vs {close_curlies}).")
    else:
        print(f"    [OK] {os.path.basename(tf)} syntax & brace structure verified.")

# 4. Flask Templates Audit
templates_dir = r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\templates"
print(f"\n[4] Auditing Flask Templates in: {templates_dir}")
for root, _, files in os.walk(templates_dir):
    for f in files:
        if f.endswith(".html"):
            t_path = os.path.join(root, f)
            with open(t_path, "r", encoding="utf-8", errors="ignore") as fp:
                t_content = fp.read()
            
            # Check Jinja tag balance
            open_blocks = len(re.findall(r"{%\s*block\b", t_content))
            close_blocks = len(re.findall(r"{%\s*endblock\b", t_content))
            if open_blocks != close_blocks:
                errors.append(f"Template: {f} has unmatched block tags ({open_blocks} vs {close_blocks}).")
            
            open_ifs = len(re.findall(r"{%\s*if\b", t_content))
            close_ifs = len(re.findall(r"{%\s*endif\b", t_content))
            if open_ifs != close_ifs:
                errors.append(f"Template: {f} has unmatched if tags ({open_ifs} vs {close_ifs}).")

print(f"    Flask templates audit complete.")

# 5. Live Website Connectivity & Route Check
print(f"\n[5] Checking Live Production URLs")
test_urls = [
    "https://swasthai-three.vercel.app/",
    "https://swasthai-three.vercel.app/blog",
    "https://swasthai-three.vercel.app/features",
    "https://swasthai-three.vercel.app/demo",
    "https://swasthai-three.vercel.app/about",
    "https://swasthai-three.vercel.app/sitemap.xml",
    "https://swasthai-three.vercel.app/rss.xml",
    "https://swasthai-three.vercel.app/blog/receptionist-triage-decisions-indian-clinics",
    "https://swasthai-three.vercel.app/blog/india-filed-65000-medical-negligence-cases-2025"
]

req_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
for url in test_urls:
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            print(f"    [HTTP {status}] {url}")
    except urllib.error.HTTPError as e:
        warnings.append(f"Live URL: {url} returned HTTP {e.code}")
        print(f"    [HTTP {e.code}] {url}")
    except Exception as e:
        warnings.append(f"Live URL: {url} connection check failed ({str(e)})")
        print(f"    [ERR] {url} -> {e}")

# Summary Report
print("\n" + "=" * 60)
print("AUDIT SUMMARY RESULTS")
print("=" * 60)
if not errors and not warnings:
    print(">>> 100% PERFECT ALIGNMENT. Zero errors, Zero warnings.")
else:
    if errors:
        print(f"\n[CRITICAL ERRORS: {len(errors)}]")
        for err in errors:
            print(f"  - {err}")
    if warnings:
        print(f"\n[WARNINGS / NOTICES: {len(warnings)}]")
        for w in warnings:
            print(f"  - {w}")

print("=" * 60)
