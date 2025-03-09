from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_e4b9049b-zone-ai_scraper:ou38u0ceibcc'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


def scrape_website(website):
    print("Launching Chrome Browser")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifoulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
