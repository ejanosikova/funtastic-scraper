from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
import csv

base_url = "https://www.funtastic.sk"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(base_url)
driver.maximize_window()
sleep(5)

decline_cookies = driver.find_element(By.ID, "cookies-notify__disagree")
if decline_cookies:
    decline_cookies.click()
sleep(3.26)

# categories = ["KNIHY", "KOMIKSY", "MANGA V ČEŠTINE"]
categories = ["MANGA V ČEŠTINE"]

products_links = []

for category in categories:

    category_tag = driver.find_element(By.LINK_TEXT, category)
    category_tag.click()
    sleep(random.uniform(4, 5))

    pages_range_tag = driver.find_elements(By.CLASS_NAME, "number")
    page_range = max([int(page.text) for page in pages_range_tag])

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    products_list = soup.findAll('div', {'class': 'img_box'})
    for product in products_list:
        link = product.find("a")['href']
        products_links.append(base_url + link)

    for i in range(1, page_range):
        page_number = i + 1
        next_page = driver.find_element(By.LINK_TEXT, f"{page_number}")
        sleep(random.uniform(4, 5))
        next_page.click()
        sleep(random.uniform(2, 4))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        products_list = soup.findAll('div', {'class': 'img_box'})
        for product in products_list:
            link = product.find("a")['href']
            products_links.append(base_url + link)

driver.quit()

data_to_save = []
print(len(products_links))
for product_link in products_links:
    print(product_link)
    f = requests.get(product_link)
    hun = BeautifulSoup(f.content, 'html.parser')
    try:
        MOC = float(
            hun.find('span', {'class': 'price-normal'}).text.replace('\n', "").strip().strip('€').replace(',', '.'))
    except:
        MOC = None
    describ = hun.find("div", {"id": "wherei"}).findAll("a")
    category_level = []
    for i, des in enumerate(describ):
        category_level.append({"Category{}".format(i): "{}".format(des.text.replace('\n', "").strip())})
    Category0 = None
    Category1 = None
    Category2 = None
    Category3 = None
    Category4 = None
    for cat in category_level:
        key, value = cat.popitem()
        if key == 'Category0':
            Category0 = value
        if key == 'Category1':
            Category1 = value
        if key == 'Category2':
            Category2 = value
        if key == 'Category3':
            Category3 = value
        if key == 'Category4':
            Category4 = value
    data_to_save.append({
        "URL": product_link,
        "Title": hun.find("div", {"id": "wherei"}).find("span", {"class": "active"}).text.replace('\n',
                                                                                                  "").strip(),
        "ISBN": hun.find("td", {"class": "prices product-eancode-value"}).find("span",
                                                                               {"class": "fleft"}).text.replace(
            '\n', "").strip(),
        "MOC": MOC,
        "Price": float(
            hun.find('span', {'class': 'price-value'}).text.replace('\n', "").strip().strip('€').replace(',',
                                                                                                         '.')),
        "Category0": Category0,
        "Category1": Category1,
        "Category2": Category2,
        "Category3": Category3,
        "Category4": Category4
    })

    fieldnames = ["URL", "Title", "ISBN", "MOC", "Price", "Category0", "Category1", "Category2", "Category3",
                  "Category4"]

    with open('books.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_save)
