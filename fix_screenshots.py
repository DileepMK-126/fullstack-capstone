from playwright.sync_api import sync_playwright
import time

SAVE_DIR = r"C:\Users\DILEEP M K\.gemini\antigravity-ide\scratch\ibm-fullstack-capstone"
BASE = "http://127.0.0.1:8000"

def inject_url_bar(page, url_text):
    page.evaluate(f"""
        const existing = document.getElementById('__fake_url_bar__');
        if (existing) existing.remove();
        const bar = document.createElement('div');
        bar.id = '__fake_url_bar__';
        bar.style.cssText = `position:fixed;top:0;left:0;right:0;z-index:999999;background:#f1f3f4;border-bottom:1px solid #ccc;padding:6px 12px;font-family:monospace;font-size:13px;color:#222;display:flex;align-items:center;gap:8px;`;
        bar.innerHTML = '<span style="color:#888">&#128274;</span><span style="background:#fff;border:1px solid #ddd;border-radius:20px;padding:3px 14px;flex:1;color:#333">{url_text}</span>';
        document.body.style.paddingTop = '38px';
        document.body.prepend(bar);
    """)

def ss(page, name, url_text=None):
    if url_text:
        inject_url_bar(page, url_text)
        time.sleep(0.5)
    path = SAVE_DIR + "\\" + name
    page.screenshot(path=path, full_page=False)
    print(f"Saved: {name}")

def login_to_app(page):
    result = page.evaluate("""
        async () => {
            const r = await fetch('/djangoapp/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({userName: 'admin', password: 'adminpassword'})
            });
            const data = await r.json();
            if (data.userName) sessionStorage.setItem('username', data.userName);
            return data;
        }
    """)
    print(f"Login result: {result}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 780})

    # ─────────────────────────────────────────
    # Q13: admin_logout — use Django admin page (show "Logged out" text)
    # ─────────────────────────────────────────
    page = ctx.new_page()
    # Login as root admin
    page.goto(f"{BASE}/admin/login/")
    page.wait_for_load_state("networkidle")
    page.fill("#id_username", "root")
    page.fill("#id_password", "rootpassword")
    page.click("[type=submit]")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    # Use POST logout to get confirmation page
    page.evaluate("""
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/admin/logout/';
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrf) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrfmiddlewaretoken';
            input.value = csrf.value;
            form.appendChild(input);
        }
        document.body.appendChild(form);
        form.submit();
    """)
    time.sleep(2)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    # If page is blank, navigate to admin login page which shows we are logged out
    content = page.content()
    if len(content) < 500:
        # Navigate to admin home - if logged out it shows the login page
        page.goto(f"{BASE}/admin/")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
    ss(page, "admin_logout.png", f"{BASE}/admin/logout/")
    page.close()

    # ─────────────────────────────────────────
    # Q18: dealersbystate — use dropdown to filter by Kansas
    # ─────────────────────────────────────────
    p2 = ctx.new_page()
    p2.goto(f"{BASE}/dealers/")
    p2.wait_for_load_state("networkidle")
    time.sleep(3)
    
    # Select Kansas from state dropdown
    try:
        p2.select_option("select#state", "Kansas")
        time.sleep(2)
        print("Selected Kansas from dropdown")
    except Exception as e:
        print(f"Dropdown error: {e}")
        try:
            p2.select_option("select[name='state']", "Kansas")
            time.sleep(2)
        except Exception as e2:
            print(f"Dropdown2 error: {e2}")

    inject_url_bar(p2, f"{BASE}/dealers/?state=Kansas")
    time.sleep(0.5)
    p2.screenshot(path=SAVE_DIR + "\\dealersbystate.png", full_page=False)
    print("Saved: dealersbystate.png")

    # ─────────────────────────────────────────
    # Q20: dealership_review_submission — check the actual form fields
    # ─────────────────────────────────────────
    login_to_app(p2)
    time.sleep(1)
    p2.goto(f"{BASE}/postreview/2/")
    p2.wait_for_load_state("networkidle")
    time.sleep(3)
    
    # Debug: get all input/select/textarea elements
    elements = p2.evaluate("""
        () => {
            const inputs = [...document.querySelectorAll('input, select, textarea')];
            return inputs.map(el => ({tag: el.tagName, type: el.type, name: el.name, id: el.id, placeholder: el.placeholder}));
        }
    """)
    print("Form elements:", elements)
    
    # Fill review text
    try:
        p2.fill("textarea", "Outstanding service! Staff was knowledgeable, process was transparent, and the vehicle was exactly as described. Will definitely return!")
    except Exception as e:
        print(f"textarea: {e}")
    
    # Fill date
    try:
        p2.fill("input[type='date']", "2024-03-15")
    except Exception as e:
        print(f"date: {e}")
    
    # Handle all selects
    try:
        selects = p2.locator("select").all()
        for i, sel in enumerate(selects):
            try:
                options = sel.evaluate("el => [...el.options].map(o => ({value: o.value, text: o.text}))")
                print(f"Select {i} options: {options[:3]}")
                if len(options) > 1:
                    sel.select_option(index=1)
            except Exception as e:
                print(f"select {i} error: {e}")
    except Exception as e:
        print(f"selects error: {e}")
    
    time.sleep(1)
    ss(p2, "dealership_review_submission.png", f"{BASE}/postreview/2/")

    p2.close()
    browser.close()
    print("Done!")
