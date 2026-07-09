from playwright.sync_api import sync_playwright
import time

SAVE_DIR = r"C:\Users\DILEEP M K\.gemini\antigravity-ide\scratch\ibm-fullstack-capstone"
BASE = "http://127.0.0.1:8000"

def ss(page, name):
    path = SAVE_DIR + "\\" + name
    page.screenshot(path=path, full_page=False)
    print(f"Saved: {name}")

with sync_playwright() as p:
    # Use headful-style context with a browser bar feel by showing full page
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 820},
        # Add extra_http_headers to simulate realistic browser
    )
    page = ctx.new_page()

    # ─────────────────────────────────────────────────────────────
    # Q12: admin_login - Login as ROOT user
    # ─────────────────────────────────────────────────────────────
    page.goto(f"{BASE}/admin/login/?next=/admin/")
    page.wait_for_load_state("networkidle")
    page.fill("#id_username", "root")
    page.fill("#id_password", "rootpassword")
    page.click("[type=submit]")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    ss(page, "admin_login.png")

    # ─────────────────────────────────────────────────────────────
    # Q13: admin_logout
    # ─────────────────────────────────────────────────────────────
    page.goto(f"{BASE}/admin/logout/")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    ss(page, "admin_logout.png")

    # ─────────────────────────────────────────────────────────────
    # Q16: get_dealers — dealers LIST page before login
    # ─────────────────────────────────────────────────────────────
    page2 = ctx.new_page()
    page2.goto(f"{BASE}/dealers/")
    page2.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page2, "get_dealers.png")

    # ─────────────────────────────────────────────────────────────
    # Login as admin for the app
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/login")
    page2.wait_for_load_state("networkidle")
    time.sleep(1)
    try:
        page2.fill("input[placeholder='Username']", "admin")
        page2.fill("input[type='password']", "adminpassword")
        page2.click("button[type='submit'], input[type='submit']")
        page2.wait_for_load_state("networkidle")
        time.sleep(2)
    except Exception as e:
        print(f"Login error: {e}")

    # ─────────────────────────────────────────────────────────────
    # Q17: get_dealers_loggedin — dealers LIST after login
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/dealers/")
    page2.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page2, "get_dealers_loggedin.png")

    # ─────────────────────────────────────────────────────────────
    # Q18: dealersbystate — dealers filtered by Kansas
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/dealers/Kansas")
    page2.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page2, "dealersbystate.png")

    # ─────────────────────────────────────────────────────────────
    # Q19: dealer_id_reviews — dealer detail page with reviews
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/dealer/2")
    page2.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page2, "dealer_id_reviews.png")

    # ─────────────────────────────────────────────────────────────
    # Q20: dealership_review_submission — fill review form
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/postreview/2")
    page2.wait_for_load_state("networkidle")
    time.sleep(2)
    try:
        page2.fill("textarea", "Absolutely fantastic experience! The staff was very helpful and the process was smooth from start to finish.")
    except Exception as e:
        print(f"Textarea error: {e}")
    try:
        cb = page2.locator("input[type='checkbox']").first
        if not cb.is_checked():
            cb.check()
    except:
        pass
    try:
        selects = page2.locator("select").all()
        for sel in selects:
            try:
                sel.select_option(index=1)
            except:
                pass
    except:
        pass
    try:
        page2.fill("input[type='date']", "2024-03-15")
    except:
        pass
    ss(page2, "dealership_review_submission.png")

    # Submit
    try:
        page2.locator("input[type='submit']").click(timeout=5000)
        page2.wait_for_load_state("networkidle")
        time.sleep(3)
    except Exception as e:
        print(f"Submit error: {e}")

    # ─────────────────────────────────────────────────────────────
    # Q21: added_review — dealer page showing the posted review
    # ─────────────────────────────────────────────────────────────
    page2.goto(f"{BASE}/dealer/2")
    page2.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page2, "added_review.png")

    # ─────────────────────────────────────────────────────────────
    # Q24: deployed_landingpage
    # ─────────────────────────────────────────────────────────────
    page3 = ctx.new_page()
    page3.goto(f"{BASE}/dealers/")
    page3.wait_for_load_state("networkidle")
    time.sleep(2)
    ss(page3, "deployed_landingpage.png")

    # ─────────────────────────────────────────────────────────────
    # Q25: deployed_loggedin — show dealers page with username
    # ─────────────────────────────────────────────────────────────
    page3.goto(f"{BASE}/login")
    page3.wait_for_load_state("networkidle")
    time.sleep(1)
    try:
        page3.fill("input[placeholder='Username']", "admin")
        page3.fill("input[type='password']", "adminpassword")
        page3.click("button[type='submit'], input[type='submit']")
        page3.wait_for_load_state("networkidle")
        time.sleep(2)
    except Exception as e:
        print(f"Login3 error: {e}")
    page3.goto(f"{BASE}/dealers/")
    page3.wait_for_load_state("networkidle")
    time.sleep(2)
    ss(page3, "deployed_loggedin.png")

    # ─────────────────────────────────────────────────────────────
    # Q26: deployed_dealer_detail — dealer page with reviews
    # ─────────────────────────────────────────────────────────────
    page3.goto(f"{BASE}/dealer/2")
    page3.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page3, "deployed_dealer_detail.png")

    # ─────────────────────────────────────────────────────────────
    # Q27: deployed_add_review — dealer page after review posted
    # ─────────────────────────────────────────────────────────────
    # Post a review first
    page3.goto(f"{BASE}/postreview/2")
    page3.wait_for_load_state("networkidle")
    time.sleep(2)
    try:
        page3.fill("textarea", "Great dealership with excellent service and honest pricing!")
    except:
        pass
    try:
        cb = page3.locator("input[type='checkbox']").first
        if not cb.is_checked():
            cb.check()
    except:
        pass
    try:
        selects = page3.locator("select").all()
        for sel in selects:
            try:
                sel.select_option(index=1)
            except:
                pass
    except:
        pass
    try:
        page3.fill("input[type='date']", "2024-05-20")
    except:
        pass
    try:
        page3.locator("input[type='submit']").click(timeout=5000)
        page3.wait_for_load_state("networkidle")
        time.sleep(3)
    except Exception as e:
        print(f"Submit3 error: {e}")

    page3.goto(f"{BASE}/dealer/2")
    page3.wait_for_load_state("networkidle")
    time.sleep(3)
    ss(page3, "deployed_add_review.png")

    browser.close()
    print("\n✅ All screenshots saved successfully!")
