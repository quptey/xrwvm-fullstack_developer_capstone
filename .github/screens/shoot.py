"""Drive the running app in a real (headful) Chromium on Xvfb and capture
the whole X screen, so the browser address bar is visible in every shot."""
import os
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

OUT = sys.argv[1]
DJ = "http://localhost:8000"
EX = "http://localhost:3030"
SA = "http://localhost:5050"
USER, PWD = "quptey", "Capstone#2026"
os.makedirs(OUT, exist_ok=True)


def grab(name, wait=1.5):
    time.sleep(wait)
    subprocess.run(["import", "-window", "root", os.path.join(OUT, name)],
                   check=True)
    print("captured", name, flush=True)


def go(page, url, name=None, wait=2.0):
    page.goto(url)
    page.wait_for_load_state("networkidle")
    if name:
        grab(name, wait)


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--window-position=0,0", "--window-size=1440,900",
              "--no-first-run", "--disable-infobars"])
    ctx = browser.new_context(no_viewport=True)
    page = ctx.new_page()

    # Static pages
    go(page, DJ + "/about/", "about_us.png")
    go(page, DJ + "/contact/", "contact_us.png")

    # Dynamic pages before login
    go(page, DJ + "/dealers/", "get_dealers.png", 3)

    # Sign-up with 5 fields (filled, then submitted -> user is logged in)
    go(page, DJ + "/register/")
    page.fill("#username", USER)
    page.fill("#first_name", "Alibek")
    page.fill("#last_name", "Turarbek")
    page.fill("#email", "alibek@example.com")
    page.fill("#psw", PWD)
    grab("sign-up.png")
    page.click("input.submit")
    page.wait_for_url(DJ + "/")
    page.wait_for_load_state("networkidle")

    # Logout notification (native alert left open for the screenshot)
    with page.expect_event("dialog") as dlg:
        page.click("text=Logout", no_wait_after=True)
    grab("logout.png", 1.5)
    dlg.value.accept()
    page.wait_for_load_state("networkidle")

    # Login -> home page shows the username
    go(page, DJ + "/login/")
    page.fill("input[name=username]", USER)
    page.fill("input[name=psw]", PWD)
    page.click("input[value=Login]")
    page.wait_for_url(DJ + "/")
    page.wait_for_load_state("networkidle")
    grab("login.png")

    # Dynamic pages after login
    go(page, DJ + "/dealers/", "get_dealers_loggedin.png", 3)
    page.select_option("#state", "Kansas")
    page.wait_for_load_state("networkidle")
    grab("dealersbystate.png", 2.5)

    go(page, DJ + "/dealer/15", "dealer_id_reviews.png", 4)

    page.click("a[href$='postreview/15']")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    page.fill("#review", "Fantastic services! The team was friendly, "
                         "honest and helped me pick the right car.")
    page.fill("input[type=date]", "2026-10-20")
    opts = page.eval_on_selector_all(
        "#cars option", "els => els.map(e => e.value)")
    pick = next(v for v in opts if v.startswith("Toyota Camry")) \
        if any(v.startswith("Toyota Camry") for v in opts) else opts[1]
    page.select_option("#cars", pick)
    page.fill("input[type=int]", "2023")
    grab("dealership_review_submission.png")
    page.click("button.postreview")
    page.wait_for_url(DJ + "/dealer/15")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.mouse.wheel(0, 5000)
    grab("added_review.png", 2)

    # Express / Mongo endpoints
    go(page, EX + "/fetchReviews/dealer/15", "dealer_review.png")
    go(page, EX + "/fetchDealers", "dealerships.png")
    go(page, EX + "/fetchDealer/15", "dealer_details.png")
    go(page, EX + "/fetchDealers/Kansas", "kansasDealers.png")

    # Django proxy endpoints / sentiment analyzer
    go(page, DJ + "/djangoapp/get_cars", "cars.png")
    go(page, SA + "/analyze/Fantastic%20services", "sentiment_analyzer.png")

    # Django admin as root
    admin = ctx.new_page()
    page.close()
    go(admin, DJ + "/admin/")
    admin.fill("#id_username", "root")
    admin.fill("#id_password", PWD)
    admin.click("input[type=submit]")
    admin.wait_for_load_state("networkidle")
    grab("admin_login.png")
    go(admin, DJ + "/admin/djangoapp/carmodel/", "car_models.png")
    go(admin, DJ + "/admin/")
    admin.click("#logout-form button, a[href$='logout/']")
    admin.wait_for_load_state("networkidle")
    grab("admin_logout.png")

    browser.close()
