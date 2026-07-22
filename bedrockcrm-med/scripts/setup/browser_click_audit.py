import json
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5010"
MAX_SEC = 2.0
OUT = Path("data/browser_click_report.json")


def now_ts() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def add_defect(defects, area, title, steps, expected, actual, severity="medium"):
    defects.append(
        {
            "timestamp": now_ts(),
            "severity": severity,
            "area": area,
            "title": title,
            "repro_steps": steps,
            "expected": expected,
            "actual": actual,
        }
    )


def timed_action(timings, name, fn):
    t0 = time.perf_counter()
    result = fn()
    dt = time.perf_counter() - t0
    timings.append({"name": name, "seconds": round(dt, 3)})
    return result, dt


def check_timing(defects, area, action, seconds):
    if seconds > MAX_SEC:
        add_defect(
            defects,
            area,
            f"Action slower than {MAX_SEC}s",
            [f"Run action: {action}"],
            f"Action completes within {MAX_SEC}s",
            f"Took {seconds:.3f}s",
            severity="medium",
        )


def install_page_monitors(page, defects, area_label):
    def on_console(msg):
        if msg.type == "error":
            if "Failed to load resource" in msg.text:
                return
            add_defect(
                defects,
                area_label,
                "Console error",
                [f"Open page in area: {area_label}"],
                "No console errors",
                msg.text,
                severity="low",
            )

    def on_request_failed(req):
        failure = (req.failure or "")
        # Ignore expected aborts caused by quick page transitions or stream shutdown.
        if "ERR_ABORTED" in failure:
            return
        # Ignore optional external providers that may fail in headless/offline environments.
        if any(host in req.url for host in ["openstreetmap.org", "cdn.jsdelivr.net"]):
            return
        if "/sse/queue" in req.url:
            return
        add_defect(
            defects,
            area_label,
            "Network request failed",
            [f"Open page in area: {area_label}", f"Trigger request to {req.url}"],
            "Requests should not fail",
            f"Request failed: {failure}",
            severity="medium",
        )

    def on_response(resp):
        status = resp.status
        if any(host in resp.url for host in ["openstreetmap.org", "cdn.jsdelivr.net"]):
            return
        if status >= 400 and resp.request.resource_type in {"document", "script", "stylesheet", "xhr", "fetch", "image"}:
            add_defect(
                defects,
                area_label,
                "HTTP error response",
                [f"Open page in area: {area_label}", f"Trigger URL {resp.url}"],
                "No 4xx/5xx responses for core assets/actions",
                f"HTTP {status} from {resp.url}",
                severity="medium",
            )

    page.on("console", on_console)
    page.on("requestfailed", on_request_failed)
    page.on("response", on_response)
    page.on("dialog", lambda d: d.accept())


def dismiss_blocking_modals(page):
    # Credentials modal can remain open after clinic creation and block pointer events.
    if page.locator("#credentialsModal.show").count() > 0:
        close_btn = page.locator("#credentialsModal .btn-close")
        if close_btn.count() > 0:
            close_btn.first.click()
        else:
            page.keyboard.press("Escape")

    # Fallback: close any visible bootstrap modal with a close icon.
    for modal in page.locator(".modal.show").all():
        btn = modal.locator(".btn-close")
        if btn.count() > 0:
            btn.first.click()

        # Force-clear any lingering bootstrap backdrops and modal state.
        page.evaluate(
                """
                () => {
                    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('padding-right');
                    document.querySelectorAll('.modal').forEach(m => {
                        m.classList.remove('show');
                        m.style.display = 'none';
                        m.removeAttribute('aria-modal');
                    });
                }
                """
        )


def run():
    defects = []
    timings = []
    created_clinic_slug = None
    created_clinic_id = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ---------------- Super-admin flow ----------------
        context_sa = browser.new_context()
        page_sa = context_sa.new_page()
        install_page_monitors(page_sa, defects, "superadmin")

        # Warm first hit to avoid cold-start noise in timing checks.
        page_sa.goto(f"{BASE}/superadmin/login", wait_until="domcontentloaded")
        _, dt = timed_action(timings, "goto superadmin login", lambda: page_sa.goto(f"{BASE}/superadmin/login", wait_until="domcontentloaded"))
        check_timing(defects, "superadmin", "goto /superadmin/login", dt)

        page_sa.fill("#emailInput", "swasthai.admin@system.com")
        page_sa.fill("#passwordInput", "Sw@sth1#2026")

        _, dt = timed_action(
            timings,
            "superadmin sign in",
            lambda: (
                page_sa.click("button[type='submit']"),
                page_sa.wait_for_url("**/superadmin/dashboard", timeout=10000),
            ),
        )
        check_timing(defects, "superadmin", "login and redirect", dt)

        # Navigate core pages by click
        for name, selector, expected_url in [
            ("clinics", "a[href='/superadmin/clinics']", "**/superadmin/clinics"),
            ("patients", "a[href='/superadmin/patients']", "**/superadmin/patients"),
            ("analytics", "a[href='/superadmin/analytics']", "**/superadmin/analytics"),
            ("admins", "a[href='/superadmin/admins']", "**/superadmin/admins"),
        ]:
            try:
                _, dt = timed_action(
                    timings,
                    f"superadmin nav {name}",
                    lambda: (page_sa.click(selector), page_sa.wait_for_url(expected_url, timeout=10000)),
                )
                check_timing(defects, "superadmin", f"navigate to {name}", dt)
            except PlaywrightTimeoutError:
                add_defect(
                    defects,
                    "superadmin",
                    f"Cannot navigate to {name}",
                    [
                        "Login as superadmin",
                        f"Click nav link {selector}",
                    ],
                    f"Should open {expected_url}",
                    "Navigation timed out",
                    severity="high",
                )

        # Return clinics, create a clinic via UI modal
        page_sa.goto(f"{BASE}/superadmin/clinics", wait_until="domcontentloaded")
        page_sa.click("button:has-text('Add New Clinic')")
        page_sa.fill("#clinicName", f"UI Audit Clinic {int(time.time())}")
        page_sa.fill("#clinicEmail", f"uiaudit{int(time.time())}@clinic.test")
        page_sa.fill("#clinicPhone", "+919988776655")
        page_sa.fill("#clinicAddress", "Audit Address Mumbai")

        try:
            with page_sa.expect_response(lambda r: "/superadmin/api/clinics" in r.url and r.request.method == "POST", timeout=15000) as resp_info:
                _, dt = timed_action(timings, "superadmin create clinic click", lambda: page_sa.click("#clinicModal .btn.btn-primary:has-text('Save Clinic')"))
                check_timing(defects, "superadmin", "click save clinic", dt)
            resp = resp_info.value
            if resp.status != 201:
                add_defect(
                    defects,
                    "superadmin",
                    "Create clinic failed",
                    [
                        "Login as superadmin",
                        "Go to Clinics",
                        "Click Add New Clinic",
                        "Fill required fields and click Save Clinic",
                    ],
                    "Clinic should be created (201)",
                    f"Received HTTP {resp.status}",
                    severity="high",
                )
            else:
                payload = resp.json()
                created_clinic_slug = payload.get("slug")
                created_clinic_id = payload.get("id")
        except PlaywrightTimeoutError:
            add_defect(
                defects,
                "superadmin",
                "Create clinic request timeout",
                [
                    "Login as superadmin",
                    "Go to Clinics",
                    "Create clinic and click Save",
                ],
                "POST /superadmin/api/clinics should return quickly",
                "No response within timeout",
                severity="high",
            )

        # Create doctor from manage doctors modal to validate cross-linking
        if created_clinic_id:
            dismiss_blocking_modals(page_sa)
            if page_sa.locator("#credentialsModal.show").count() > 0:
                page_sa.click("#credentialsModal .btn-close")
                page_sa.wait_for_selector("#credentialsModal.show", state="hidden", timeout=5000)
            page_sa.wait_for_selector("#clinicModal.show", state="hidden", timeout=5000)
            row = page_sa.locator("#clinicsTableBody tr", has_text=str(created_clinic_slug))
            if row.count() == 0:
                add_defect(
                    defects,
                    "superadmin",
                    "New clinic not visible in clinics table",
                    [
                        "Create clinic from Clinics page",
                        "Look for clinic row by slug",
                    ],
                    "New clinic row should render in table",
                    f"No row found for slug {created_clinic_slug}",
                    severity="high",
                )
            else:
                try:
                    dismiss_blocking_modals(page_sa)
                    row.first.locator("button[title='Manage Doctors']").click()
                    page_sa.fill("#doctorName", "Dr UI Audit")
                    doctor_email = f"dr.ui.audit.{int(time.time())}@clinic.test"
                    page_sa.fill("#doctorEmail", doctor_email)
                    page_sa.fill("#doctorPassword", "test1234")
                    page_sa.fill("#doctorSpecialization", "General Medicine")
                    with page_sa.expect_response(lambda r: f"/superadmin/api/clinics/{created_clinic_id}/doctors" in r.url and r.request.method == "POST", timeout=15000) as dresp_info:
                        _, dt = timed_action(timings, "superadmin create doctor click", lambda: page_sa.click("#addDoctorForm button[type='submit']"))
                        check_timing(defects, "superadmin", "create doctor", dt)
                    dresp = dresp_info.value
                except PlaywrightTimeoutError:
                    add_defect(
                        defects,
                        "superadmin",
                        "Manage doctor modal interaction failed",
                        [
                            "Open Manage Doctors for a clinic",
                            "Click Manage Doctors button",
                        ],
                        "Doctor modal should open and allow create action",
                        "Interaction timed out (likely modal overlay issue)",
                        severity="high",
                    )
                else:
                    if dresp.status != 201:
                        add_defect(
                            defects,
                            "superadmin",
                            "Create doctor failed",
                            [
                                "Open Manage Doctors for a clinic",
                                "Fill doctor form and submit",
                            ],
                            "Doctor should be created (201)",
                            f"Received HTTP {dresp.status}",
                            severity="high",
                        )

        context_sa.close()

        # ---------------- Doctor flow ----------------
        context_dr = browser.new_context()
        page_dr = context_dr.new_page()
        install_page_monitors(page_dr, defects, "doctor")

        _, dt = timed_action(timings, "goto doctor login", lambda: page_dr.goto(f"{BASE}/doctor/login", wait_until="domcontentloaded"))
        check_timing(defects, "doctor", "goto /doctor/login", dt)

        page_dr.fill("#emailInput", "admin@clinic.com")
        page_dr.fill("#passwordInput", "admin123")
        _, dt = timed_action(
            timings,
            "doctor sign in",
            lambda: (page_dr.click("button[type='submit']"), page_dr.wait_for_url("**/doctor/dashboard", timeout=10000)),
        )
        check_timing(defects, "doctor", "login and redirect", dt)

        # Click core dashboard controls
        for selector, label in [
            ("#walkins-tab", "walkins tab"),
            ("#appointments-tab", "appointments tab"),
            ("#unified-tab", "unified tab"),
            ("button:has-text('Refresh All')", "refresh all"),
        ]:
            try:
                _, dt = timed_action(timings, f"doctor click {label}", lambda s=selector: page_dr.click(s))
                check_timing(defects, "doctor", f"click {label}", dt)
            except PlaywrightTimeoutError:
                add_defect(
                    defects,
                    "doctor",
                    f"Failed to click {label}",
                    ["Login as doctor", f"Click element {selector}"],
                    "Element should be clickable",
                    "Click timed out",
                    severity="medium",
                )

        # Navigate linked pages by clicking header links
        for href in ["/doctor/appointments", "/doctor/clinic-hours", "/doctor/slot-settings", "/doctor/change-password"]:
            try:
                _, dt = timed_action(
                    timings,
                    f"doctor nav {href}",
                    lambda h=href: (page_dr.click(f"a[href='{h}']"), page_dr.wait_for_url(f"**{h}", timeout=10000)),
                )
                check_timing(defects, "doctor", f"navigate {href}", dt)
            except PlaywrightTimeoutError:
                add_defect(
                    defects,
                    "doctor",
                    f"Navigation failed {href}",
                    ["Login as doctor", f"Click link a[href='{href}']"],
                    f"Should open {href}",
                    "Navigation timed out",
                    severity="medium",
                )

        context_dr.close()

        # ---------------- Patient flow ----------------
        context_pt = browser.new_context()
        page_pt = context_pt.new_page()
        install_page_monitors(page_pt, defects, "patient")

        slug = created_clinic_slug or "sample-clinic"
        # Warm first hit for clinic landing before measuring.
        page_pt.goto(f"{BASE}/c/{slug}", wait_until="domcontentloaded")
        _, dt = timed_action(timings, "goto clinic landing", lambda: page_pt.goto(f"{BASE}/c/{slug}", wait_until="domcontentloaded"))
        check_timing(defects, "patient", f"goto /c/{slug}", dt)

        # Track-status button flow (phone may not exist; still verifies click/action path)
        if page_pt.locator("#trackPhone").count() > 0:
            page_pt.fill("#trackPhone", "9000012345")
            _, dt = timed_action(timings, "patient click Find My Status", lambda: page_pt.click("button:has-text('Find My Status')"))
            check_timing(defects, "patient", "click Find My Status", dt)

        # Register now click and page transitions
        _, dt = timed_action(
            timings,
            "patient click Register Now",
            lambda: (page_pt.click("a:has-text('Register Now')"), page_pt.wait_for_url(f"**/c/{slug}/register", timeout=10000)),
        )
        check_timing(defects, "patient", "open register page", dt)

        # Fill registration and submit
        unique_phone = f"9{int(time.time()) % 1000000000:09d}"
        page_pt.fill("input[name='name']", "Browser Audit Patient")
        page_pt.fill("input[name='age']", "29")
        page_pt.select_option("select[name='gender']", "Male")
        page_pt.fill("#phoneInput", unique_phone)

        # If doctor selector is visible, choose first doctor
        if page_pt.locator("#doctorSelectSection").is_visible():
            opts = page_pt.locator("#doctorSelectInput option")
            if opts.count() > 1:
                page_pt.select_option("#doctorSelectInput", index=1)

        page_pt.click("#step1 button:has-text('Next')")
        page_pt.click("#step2 button:has-text('Next')")

        # Submit and wait for patient submit response
        try:
            with page_pt.expect_response(lambda r: "/api/patient/submit" in r.url and r.request.method == "POST", timeout=20000) as presp_info:
                _, dt = timed_action(timings, "patient submit registration", lambda: page_pt.click("#submitBtn"))
                check_timing(defects, "patient", "submit registration", dt)
            presp = presp_info.value
            if presp.status != 201:
                add_defect(
                    defects,
                    "patient",
                    "Patient registration submit failed",
                    [
                        f"Open {BASE}/c/{slug}/register",
                        "Fill required fields",
                        "Click Complete Registration",
                    ],
                    "Submit should return 201",
                    f"HTTP {presp.status} from /api/patient/submit",
                    severity="high",
                )
        except PlaywrightTimeoutError:
            add_defect(
                defects,
                "patient",
                "Patient submit timed out",
                [
                    f"Open {BASE}/c/{slug}/register",
                    "Fill required fields",
                    "Click Complete Registration",
                ],
                "Submit should complete quickly",
                "No /api/patient/submit response within timeout",
                severity="high",
            )

        context_pt.close()
        browser.close()

    # Deduplicate noisy repeated defects (same area/title/actual)
    unique = []
    seen = set()
    for d in defects:
        key = (d["area"], d["title"], d["actual"])
        if key not in seen:
            unique.append(d)
            seen.add(key)

    summary = {
        "generated_at": now_ts(),
        "base_url": BASE,
        "max_allowed_seconds": MAX_SEC,
        "timings": timings,
        "timing_violations": [t for t in timings if t["seconds"] > MAX_SEC],
        "defect_count": len(unique),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump({"summary": summary, "defects": unique}, f, indent=2)

    print(json.dumps({"report": str(OUT), "defect_count": len(unique), "timing_violations": len(summary['timing_violations'])}, indent=2))


if __name__ == "__main__":
    run()
