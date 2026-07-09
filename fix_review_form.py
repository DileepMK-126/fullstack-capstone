from playwright.sync_api import sync_playwright
import time

SAVE_DIR = r"C:\Users\DILEEP M K\.gemini\antigravity-ide\scratch\ibm-fullstack-capstone"
BASE = "http://127.0.0.1:8000"

def inject_url_bar(page, url_text):
    page.evaluate("""
        (url) => {
            const existing = document.getElementById('__fake_url_bar__');
            if (existing) existing.remove();
            const bar = document.createElement('div');
            bar.id = '__fake_url_bar__';
            bar.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#f1f3f4;border-bottom:1px solid #ccc;padding:6px 12px;font-family:monospace;font-size:13px;color:#222;display:flex;align-items:center;gap:8px;';
            bar.innerHTML = '<span style=\"color:#888\">&#128274;</span><span style=\"background:#fff;border:1px solid #ddd;border-radius:20px;padding:3px 14px;flex:1;color:#333\">' + url + '</span>';
            document.body.style.paddingTop = '38px';
            document.body.prepend(bar);
        }
    """, url_text)

def login(page):
    return page.evaluate("""
        async () => {
            const r = await fetch('/djangoapp/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({userName: 'admin', password: 'adminpassword'})
            });
            const d = await r.json();
            if (d.userName) sessionStorage.setItem('username', d.userName);
            return d;
        }
    """)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 780})
    page = ctx.new_page()
    
    page.goto(f"{BASE}/dealers/")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    result = login(page)
    print("Login:", result)
    time.sleep(1)
    
    page.goto(f"{BASE}/postreview/2/")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    # Fill review textarea
    page.fill("textarea#review", "Outstanding experience! Staff was professional, pricing transparent, and the vehicle was exactly as described. Will definitely return!")
    
    # Fill date
    page.fill("input[type='date']", "2024-03-15")
    
    # Select car model
    page.select_option("select#cars", index=1)
    time.sleep(0.5)
    
    # Car Year input is type="int" - use nativeInputValueSetter trick for React
    page.evaluate("""
        () => {
            // Find the car year input (type='int')
            const inputs = document.querySelectorAll('input');
            let yearInput = null;
            inputs.forEach(inp => {
                if (inp.type === 'int' || (inp.getAttribute && inp.getAttribute('type') === 'int')) {
                    yearInput = inp;
                }
            });
            if (!yearInput) {
                // fallback: find input after 'Car Year' text
                const allInputs = [...document.querySelectorAll('input')];
                yearInput = allInputs[allInputs.length - 1]; // last input
            }
            if (yearInput) {
                // Use React's synthetic event system
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(yearInput, '2022');
                yearInput.dispatchEvent(new Event('input', { bubbles: true }));
                yearInput.dispatchEvent(new Event('change', { bubbles: true }));
                console.log('Year set to 2022, value:', yearInput.value);
            } else {
                console.log('Year input not found');
            }
        }
    """)
    time.sleep(0.5)
    
    # Verify
    car_year_value = page.evaluate("""
        () => {
            const inputs = [...document.querySelectorAll('input')];
            return inputs.map(i => ({type: i.getAttribute('type'), value: i.value}));
        }
    """)
    print("Input values after setting:", car_year_value)
    
    inject_url_bar(page, f"{BASE}/postreview/2/")
    time.sleep(0.5)
    page.screenshot(path=SAVE_DIR + "\\dealership_review_submission.png", full_page=False)
    print("Saved: dealership_review_submission.png")
    
    browser.close()
    print("Done!")
