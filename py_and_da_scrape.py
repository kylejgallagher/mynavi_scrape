import pandas as pd
# ------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

job_listings_python = []
job_listings_da = []

def scrape_python():
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for page in range(1, 10):  # Scrape pages 1 and 2
        url = f'https://tenshoku.mynavi.jp/fw/kwpython/pg{page}'
        driver.get(url)
        time.sleep(3)  # Let the page load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_boxes = soup.find_all('div', class_='cassetteRecruit')

        for box in job_boxes:
            # Job title
            title_tag = box.find('p', class_='cassetteRecruit__copy boxAdjust')
            title = title_tag.get_text(strip=True) if title_tag else "No title found"


            salary = 'Not Listed'
            rows = box.select('table.tableCondition tr')
            for row in rows:
                head = row.find('th')
                body = row.find('td', class_='tableCondition__body')
                if head and body:
                    label = head.get_text(strip=True)
                    if "月給" in label or "年収" in label or "給与" in label:
                        salary = body.get_text(strip=True)
            job_listings_python.append({
                'title': title,
                'salary': salary
            })

    driver.quit()

    # Output the result
    # for job in job_listings:
    #     print(f"Title: {job['title']}\nSalary: {job['salary']}\n")

def scrape_da():
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for page in range(1, 14):
        url = f'https://tenshoku.mynavi.jp/fw/kw%E3%83%87%E3%83%BC%E3%82%BF%E5%88%86%E6%9E%90/{page}'
        driver.get(url)
        time.sleep(3)  # Let the page load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_boxes = soup.find_all('div', class_='cassetteRecruit')

        for box in job_boxes:
            # Job title
            title_tag = box.find('p', class_='cassetteRecruit__copy boxAdjust')
            title = title_tag.get_text(strip=True) if title_tag else "No title found"


            salary = 'Not Listed'
            rows = box.select('table.tableCondition tr')
            for row in rows:
                head = row.find('th')
                body = row.find('td', class_='tableCondition__body')
                if head and body:
                    label = head.get_text(strip=True)
                    if "月給" in label or "年収" in label or "給与" in label:
                        salary = body.get_text(strip=True)
            job_listings_da.append({
                'title': title,
                'salary': salary
            })

    driver.quit()

    # Output the result
    # for job in job_listings:
    #     print(f"Title: {job['title']}\nSalary: {job['salary']}\n")


scrape_python()
scrape_da()

df_py = pd.DataFrame(job_listings_python)
df_da = pd.DataFrame(job_listings_da)

with open('Mynavi Job Scrape.csv', 'w') as f:
    df_da.to_csv(f, index=False)
    f.write('\n')
    df_py.to_csv(f, index=False)
