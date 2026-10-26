import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=[
        "--window-position=0,0", "--window-size=1440,900", "--no-first-run"])
    pg = b.new_context(no_viewport=True).new_page()
    pg.goto(url)
    pg.wait_for_load_state("networkidle")
    time.sleep(5)
    subprocess.run(["import", "-window", "root", out], check=True)
    b.close()
