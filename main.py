from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
import csv
import json


class FuntasticScraper:
    def __init__(self):
        self.base_url = "https://www.funtastic.sk"
        self.products_links = []
        self.driver = self.create_driver()
        self.data_to_save = []

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def get_all_categories(self):
        categories = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        menu_tag = soup.find('ul', {'class': 'menu-root'})
        category_tags = menu_tag.findAll('li', {'class': 'eshop-menu-item'})
        for category in category_tags:
            category_name = category.find("a").text.replace(
                    '\n', "").replace(
                    '(', "").replace(
                    ')', "").strip()
            categories.append(category_name)
        return categories

    def get_wanted_categories(self):
        with open("config.json", "r") as jsonfile:
            config_data = json.load(jsonfile)
        wanted_categories = config_data["wanted_categories"]
        if not wanted_categories:
            wanted_categories = self.get_all_categories()
        print(f"Wanted categories: {wanted_categories}")
        return wanted_categories

    def load_website(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        sleep(5)
        decline_cookies = self.driver.find_element(By.ID, "cookies-notify__disagree")
        if decline_cookies:
            decline_cookies.click()
        sleep(3.26)

    def get_products_links(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        products_list = soup.findAll('div', {'class': 'img_box'})
        for product in products_list:
            link = product.find("a")['href']
            self.products_links.append(self.base_url + link)

    def get_products(self):
        categories = self.get_wanted_categories()  # e.g. ["KNIHY", "KOMIKSY", "MANGA V ČEŠTINE"] or [] for all categories
        for category in categories:
            print(f"Current category: {category}")
            category_tag = self.driver.find_element(By.LINK_TEXT, category)
            category_tag.click()
            sleep(random.uniform(4, 5))

            pages_range_tag = self.driver.find_elements(By.CLASS_NAME, "number")
            try:
                page_range = max([int(page.text) for page in pages_range_tag])
            except ValueError:
                print("Category is empty")
            else:
                self.get_products_links()

                for i in range(1, page_range):
                    page_number = i + 1
                    next_page = self.driver.find_element(By.LINK_TEXT, f"{page_number}")
                    sleep(random.uniform(4, 5))
                    next_page.click()
                    sleep(random.uniform(2, 4))
                    self.get_products_links()

        self.driver.quit()

    def get_products_data(self):
        products_number = len(self.products_links)
        for i, product_link in enumerate(self.products_links):
            print(f"{i}/{products_number} - {product_link}")
            f = requests.get(product_link)
            soup = BeautifulSoup(f.content, 'html.parser')
            try:
                isbn = soup.find("td", {"class": "prices product-eancode-value"}).find("span",
                                                                                       {
                                                                                           "class": "fleft"}).text.replace(
                    '\n', "").strip()
            except AttributeError:
                isbn = None
            try:
                price_normal = float(
                    soup.find('span', {'class': 'price-normal'}).text.replace('\n', "").strip().strip('€').replace(',',
                                                                                                                   '.'))
            except AttributeError:
                price_normal = None
            description = soup.find("div", {"id": "wherei"}).findAll("a")
            category_level = []
            for _, des in enumerate(description):
                category_level.append({"category{}".format(_): "{}".format(des.text.replace('\n', "").strip())})
            category0 = None
            category1 = None
            category2 = None
            category3 = None
            category4 = None
            for cat in category_level:
                key, value = cat.popitem()
                if key == 'category0':
                    category0 = value
                if key == 'category1':
                    category1 = value
                if key == 'category2':
                    category2 = value
                if key == 'category3':
                    category3 = value
                if key == 'category4':
                    category4 = value
            self.data_to_save.append({
                "url": product_link,
                "title": soup.find("div", {"id": "wherei"}).find("span", {"class": "active"}).text.replace('\n',
                                                                                                           "").strip(),
                "isbn": isbn,
                "normal_price": price_normal,
                "price": float(
                    soup.find('span', {'class': 'price-value'}).text.replace('\n', "").strip().strip('€').replace(',',
                                                                                                                  '.')),
                "category0": category0,
                "category1": category1,
                "category2": category2,
                "category3": category3,
                "category4": category4
            })

        fieldnames = ["url", "title", "isbn", "normal_price", "price", "category0", "category1", "category2", "category3",
                      "category4"]

        with open('products.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data_to_save)


if __name__ == "__main__":
    funtastic_scraper = FuntasticScraper()
    funtastic_scraper.load_website()
    funtastic_scraper.get_products()
    funtastic_scraper.get_products_data()
