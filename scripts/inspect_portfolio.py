"""
Deep inspection of Portfolio HTML, CSS, and JS
"""
import os
import re

PORTFOLIO_DIR = r"C:\Users\home\OneDrive\Desktop\Job\Portfolio"

with open(os.path.join(PORTFOLIO_DIR, "index.html"), encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("=== Modals ===")
for m in re.findall(r'<div[^>]*id=["\']([^"\']*modal[^"\']*)["\'][^>]*>', html, re.I):
    print(" - Modal ID:", m)

print("\n=== Project Titles ===")
for p in re.findall(r'<h3[^>]*class=["\'][^"\']*font-bold[^"\']*["\'][^>]*>(.*?)</h3>', html):
    print(" - Project/Card:", re.sub(r'<[^>]+>', '', p).strip())

print("\n=== Contact Links ===")
for mail in set(re.findall(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)):
    print(" - Email:", mail)

for link in set(re.findall(r'href=["\'](https?://[^"\']+)["\']', html)):
    print(" - Link:", link)
