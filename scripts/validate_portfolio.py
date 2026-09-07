"""
Validation script for Portfolio HTML, CSS, and JS integration
"""
import os
import re

PORTFOLIO_DIR = r"C:\Users\home\OneDrive\Desktop\Job\Portfolio"
INDEX_PATH = os.path.join(PORTFOLIO_DIR, "index.html")
CSS_PATH = os.path.join(PORTFOLIO_DIR, "styles.css")
JS_PATH = os.path.join(PORTFOLIO_DIR, "script.js")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css_content = f.read()

with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

print(f"HTML size: {len(html_content)} bytes")
print(f"CSS size: {len(css_content)} bytes")
print(f"JS size: {len(js_content)} bytes")

# 1. Check required IDs in HTML
required_ids = [
    "scroll-progress", "cursor-glow", "lens-title", "lens-score", 
    "lens-score-bar", "lens-tagline", "lens-summary", "lens-skills",
    "case-study-modal", "modal-dynamic-content", "modal-close-btn",
    "cheat-sheet-modal", "btn-cheat-sheet", "cheat-sheet-close-btn",
    "mobile-menu-btn", "mobile-nav"
]

missing_ids = []
for req_id in required_ids:
    if f'id="{req_id}"' not in html_content:
        missing_ids.append(req_id)

if missing_ids:
    print(f"[FAIL] Missing IDs in HTML: {missing_ids}")
else:
    print("[PASS] All required JavaScript IDs are present in HTML")

# 2. Check project cards
projects = ['swasth-ai', 'healthcare-cost', 'ipl-outcome', 'startup-funding', 'retail-churn']
missing_projects = []
for p in projects:
    if f'data-project-id="{p}"' not in html_content:
        missing_projects.append(p)
    if f'data-star-target="{p}"' not in html_content:
        missing_projects.append(f"{p} (star target)")

if missing_projects:
    print(f"[FAIL] Missing Project targets: {missing_projects}")
else:
    print("[PASS] All 5 project cards and STAR modal triggers are present")

# 3. Check role lens chips
roles = ['all', 'founders-office', 'business-analyst', 'product-ops']
missing_roles = []
for r in roles:
    if f'data-role="{r}"' not in html_content:
        missing_roles.append(r)

if missing_roles:
    print(f"[FAIL] Missing Role chips: {missing_roles}")
else:
    print("[PASS] All role filter chips are present")

# 4. Check for broken unicode characters
if "" in html_content or "" in css_content or "" in js_content:
    print("[FAIL] Detected replacement characters () in files!")
else:
    print("[PASS] Clean UTF-8 encoding across HTML, CSS, and JS")

# 5. Check cursor: none bug
if "cursor: none" in css_content:
    print("[FAIL] 'cursor: none' found in CSS!")
else:
    print("[PASS] No intrusive 'cursor: none' in CSS")
