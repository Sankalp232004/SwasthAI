import json
import re
import time
from urllib.parse import urljoin

import requests

BASE = "http://127.0.0.1:5010"
TIME_LIMIT = 2.0

report = {
    "checks": [],
    "failures": [],
    "slow_items": [],
    "asset_failures": [],
    "button_missing": [],
}


def rec(name, ok, code=None, elapsed=None, detail=None):
    row = {"name": name, "ok": bool(ok)}
    if code is not None:
        row["status"] = code
    if elapsed is not None:
        row["elapsed_s"] = round(elapsed, 3)
        if elapsed > TIME_LIMIT:
            report["slow_items"].append({"name": name, "elapsed_s": round(elapsed, 3)})
    if detail:
        row["detail"] = detail
    report["checks"].append(row)
    if not ok:
        report["failures"].append(row)


def req(sess, method, path, **kwargs):
    t0 = time.perf_counter()
    r = sess.request(method, urljoin(BASE, path), allow_redirects=False, timeout=20, **kwargs)
    return r, time.perf_counter() - t0


def assets(html):
    links = re.findall(r"(?:src|href)=[\"'](/[^\"']+)[\"']", html)
    return sorted({x for x in links if x.startswith("/static/") or x.startswith("/assets/")})


def btn_check(page, html):
    onclick_funcs = set(re.findall(r"onclick=[\"']\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(", html))
    defined_funcs = set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", html))
    missing = sorted(onclick_funcs - defined_funcs)
    if missing:
        report["button_missing"].append({"page": page, "missing": missing})


def check_page_assets(sess, page, html):
    for a in assets(html):
        ar, ae = req(sess, "GET", a)
        if ar.status_code >= 400:
            report["asset_failures"].append(
                {
                    "page": page,
                    "asset": a,
                    "status": ar.status_code,
                    "elapsed_s": round(ae, 3),
                }
            )


def run():
    s = requests.Session()
    r, e = req(s, "GET", "/health")
    rec("health", r.status_code == 200, r.status_code, e)

    sa = requests.Session()
    r, e = req(sa, "GET", "/superadmin/login")
    rec("superadmin login page", r.status_code == 200, r.status_code, e)
    if r.status_code == 200:
        btn_check("/superadmin/login", r.text)
        check_page_assets(sa, "/superadmin/login", r.text)

    r, e = req(sa, "POST", "/superadmin/login", json={"email": "swasthai.admin@system.com", "password": "Sw@sth1#2026"})
    ok = r.status_code == 200 and r.json().get("success") is True
    rec("superadmin login api", ok, r.status_code, e)

    super_pages = [
        "/superadmin/dashboard",
        "/superadmin/clinics",
        "/superadmin/patients",
        "/superadmin/analytics",
        "/superadmin/admins",
    ]
    for p in super_pages:
        r, e = req(sa, "GET", p)
        rec(f"superadmin page {p}", r.status_code == 200, r.status_code, e)
        if r.status_code == 200:
            btn_check(p, r.text)
            check_page_assets(sa, p, r.text)

    uniq = str(int(time.time()))
    r, e = req(
        sa,
        "POST",
        "/superadmin/api/clinics",
        json={"name": f"MVP Link {uniq}", "email": f"mvp{uniq}@mail.com", "phone": "+919999999999", "address": "Mumbai"},
    )
    created = r.status_code == 201
    data = r.json() if "application/json" in r.headers.get("content-type", "") else {}
    slug = data.get("slug")
    cid = data.get("id")
    rec("create clinic", created, r.status_code, e, detail=f"slug={slug}")

    pt = requests.Session()
    r, e = req(pt, "GET", "/")
    rec("patient home", r.status_code == 200, r.status_code, e)
    if r.status_code == 200:
        btn_check("/", r.text)
        check_page_assets(pt, "/", r.text)

    r, e = req(pt, "GET", "/c/sample-clinic")
    rec("sample clinic landing", r.status_code == 200, r.status_code, e)
    if r.status_code == 200:
        btn_check("/c/sample-clinic", r.text)
        check_page_assets(pt, "/c/sample-clinic", r.text)

    if slug:
        r, e = req(pt, "GET", f"/c/{slug}")
        rec("new clinic landing visible", r.status_code == 200, r.status_code, e)

    req(pt, "GET", "/c/sample-clinic/register")
    payload = {
        "name": "Smoke Patient",
        "age": 31,
        "gender": "Male",
        "phone": "9000012345",
        "complaint": "fever",
        "heart_rate": 88,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "respiratory_rate": 18,
        "temperature": 37.3,
        "consciousness_level": "ALERT",
        "pain_level": 2,
        "pain_location": "head",
        "chest_pain": False,
        "difficulty_breathing": False,
        "bleeding_severity": "NONE",
        "symptom_duration_hours": 24,
        "is_pregnant": False,
        "has_diabetes": False,
        "has_heart_condition": False,
    }
    r, e = req(pt, "POST", "/api/patient/submit", json=payload)
    pid = r.json().get("patient_id") if r.status_code == 201 else None
    rec("patient submit", r.status_code == 201 and bool(pid), r.status_code, e, detail=f"patient_id={pid}")

    if pid:
        r, e = req(pt, "GET", f"/c/sample-clinic/waiting/{pid}")
        rec("patient waiting page", r.status_code == 200, r.status_code, e)
        r, e = req(pt, "GET", f"/c/sample-clinic/result/{pid}")
        rec("patient result page", r.status_code == 200, r.status_code, e)

    doc_email = f"doc{uniq}@mvp.test"
    r, e = req(
        sa,
        "POST",
        f"/superadmin/api/clinics/{cid}/doctors",
        json={"name": "Dr Link", "email": doc_email, "password": "test1234", "specialization": "General Medicine"},
    )
    rec("create doctor in new clinic", r.status_code == 201, r.status_code, e)

    pt2 = requests.Session()
    req(pt2, "GET", f"/c/{slug}")
    r, e = req(pt2, "GET", "/api/doctor/list")
    reflected = False
    if r.status_code == 200:
        reflected = any(d.get("email") == doc_email for d in r.json().get("doctors", []))
    rec("patient doctor list reflects superadmin add", reflected, r.status_code, e)

    dr = requests.Session()
    r, e = req(dr, "GET", "/doctor/login")
    rec("doctor login page", r.status_code == 200, r.status_code, e)

    r, e = req(dr, "POST", "/api/doctor/login", json={"email": "admin@clinic.com", "password": "admin123"})
    rec("doctor login api", r.status_code == 200 and r.json().get("success") is True, r.status_code, e)

    doctor_pages = ["/doctor/dashboard", "/doctor/appointments", "/doctor/clinic-hours", "/doctor/slot-settings"]
    for p in doctor_pages:
        r, e = req(dr, "GET", p)
        rec(f"doctor page {p}", r.status_code == 200, r.status_code, e)
        if r.status_code == 200:
            btn_check(p, r.text)
            check_page_assets(dr, p, r.text)

    r, e = req(dr, "GET", "/api/doctor/queue")
    queue_ok = r.status_code == 200
    queue_data = r.json() if r.status_code == 200 and "application/json" in r.headers.get("content-type", "") else {}
    qsize = len(queue_data.get("patients", [])) if isinstance(queue_data.get("patients", []), list) else -1
    rec("doctor queue api", queue_ok, r.status_code, e, detail=f"size={qsize}")

    report["summary"] = {
        "total_checks": len(report["checks"]),
        "check_failures": len(report["failures"]),
        "asset_failures": len(report["asset_failures"]),
        "button_missing_pages": len(report["button_missing"]),
        "slow_over_2s": len(report["slow_items"]),
    }

    out_file = "data/mvp_smoke_report.json"
    with open(out_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"REPORT_FILE {out_file}")
    print("SUMMARY " + json.dumps(report["summary"]))


if __name__ == "__main__":
    run()
