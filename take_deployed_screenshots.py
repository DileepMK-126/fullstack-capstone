from playwright.sync_api import sync_playwright
import time

SAVE_DIR = r"C:\Users\DILEEP M K\.gemini\antigravity-ide\scratch\ibm-fullstack-capstone"
BASE = "http://127.0.0.1:8000"

def ss(page, name):
    path = SAVE_DIR + "\\" + name
    page.screenshot(path=path, full_page=False)
    print(f"Saved: {name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # ── deployed_landingpage: Home page (not logged in) ──────────────────────
    page.goto(f"{BASE}/")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    ss(page, "deployed_landingpage.png")

    # ── Login ─────────────────────────────────────────────────────────────────
    page.goto(f"{BASE}/login")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    try:
        page.fill("input[name='username'], input[placeholder*='Username'], input[placeholder*='username']", "admin")
        page.fill("input[type='password']", "adminpassword")
        page.click("input[type='submit'], button[type='submit']")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    except Exception as e:
        print(f"Login error: {e}")

    # ── deployed_loggedin: Home page after login (showing username) ───────────
    page.goto(f"{BASE}/")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    ss(page, "deployed_loggedin.png")

    # ── deployed_dealer_detail: Dealer page with reviews ─────────────────────
    page.goto(f"{BASE}/dealer/1")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page, "deployed_dealer_detail.png")

    # ── Submit a review then capture ──────────────────────────────────────────
    page.goto(f"{BASE}/postreview/1")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    try:
        page.fill("textarea", "Absolutely fantastic dealership! Highly recommend to everyone.")
    except:
        pass
    try:
        cb = page.locator("input[type='checkbox']").first
        if not cb.is_checked():
            cb.check()
    except:
        pass
    try:
        selects = page.locator("select").all()
        for sel in selects:
            sel.select_option(index=1)
    except:
        pass
    try:
        page.fill("input[type='date']", "2024-01-15")
    except:
        pass
    try:
        page.locator("input[type='submit']").click(timeout=5000)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
    except Exception as e:
        print(f"Submit error: {e}")

    # ── deployed_add_review: Dealer page now with the new review shown ────────
    page.goto(f"{BASE}/dealer/1")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page, "deployed_add_review.png")

    browser.close()
    print("\nAll deployed screenshots saved!")
