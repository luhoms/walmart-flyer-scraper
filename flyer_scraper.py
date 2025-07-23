import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Walmart URL and Selenium path
walmart_url = ("https://flipp.com/en-ca/stores/walmart")

# Headless mode
options = Options()
options.add_argument("--headless=new")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(walmart_url)

# Try and find this weeks flyer
try:
    flyer_elem = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="currentFlyers"]/div[2]/*[1]'))
    )
    publication_id = flyer_elem.get_attribute('flyer-id')
    print("Flyer ID found: ", publication_id)
except Exception as e:
    print("Could not find flyer ID", e)
    driver.quit()
    exit()

# Create link to API data
api_url = f"https://dam.flippenterprise.net/flyerkit/publication/{publication_id}/products?display_type=all&locale=en&access_token=92bcff5f7d07c3aaa4b33e2c048d7728"

if api_url:
    print("URL Found: ", api_url)

# Get JSON data from api_url
response = requests.get(api_url)
response.raise_for_status()
data = response.json()

items = []
prices = []
links = []

# Retrieve data
for i in range(len(data)):
    item = data[i].get("name")
    price = data[i].get("price_text")
    link = data[i].get("item_web_url")        

    items.append(item)
    prices.append(price)
    links.append(link)

# 3 columns for item, price of item, and link to item
dict = {"item" : items, "price" : prices, "link" : links}

df = pd.DataFrame(dict)

# Output as CSV
df.to_csv(f"walmart_flyer.csv", index=False)
    
driver.quit()

