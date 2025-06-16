import csv
import re
from playwright.sync_api import sync_playwright

## Instruction to run it on mac
# install python3 
# brew install pipx  # (if not already installed)
# pipx install playwright
# playwright install
# caffeinate python your_script.py


def scrape_details(page, org_id):
    url = f"https://bharatfpofinder.nafpo.in/main/organisationDetails/{org_id}"
    print(f"Visiting {url}")
    page.goto(url)

    # Expand extra content if needed
    try:
        page.click("text=View More", timeout=3000)
        page.wait_for_timeout(1000)
    except:
        pass  # No View More button

    # Get visible text
    text = page.inner_text("body")

    # Extract emails (can adjust regex as needed)
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

    return emails

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with open("extracted_emails.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["org_id", "email"])

            # Example range
            for org_id in range(647, 69122):
                emails = scrape_details(page, org_id)
                for email in emails:
                    writer.writerow([org_id, email])

        browser.close()

if __name__ == "__main__":
    main()
