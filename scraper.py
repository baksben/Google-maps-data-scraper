import csv
import time
import random
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import os
from utils import create_dataframe, export_data  # Import the functions from utils

class Scraper:
    def __init__(self, chrome_path):
        self.chrome_path = chrome_path

    def start_browser(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-search-engine-choice-screen")
        self.driver = webdriver.Chrome(service=Service(self.chrome_path), options=options)
        self.names = []
        self.categories = []
        self.addresses = []
        self.numbers = []
        self.emails = []
        self.websites = []
        self.ratings = []
        self.reviews = []
        self.geocoders = []
        self.screenshot_paths = []
        self.cities = []

    def close_browser(self):
        self.driver.quit()

    def click_on_cookie(self):
        try:
            driver = self.driver
            # Wait for and click the cookie consent button
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button//span[contains(text(), 'Accept all') or contains(text(), 'Aceptar todo') or contains(text(), 'Accept')]")
                )
            )
            cookie_button.click()
            print("Clicked the cookie button successfully")
        except TimeoutException:
            print("Cookie button not found within the given time.")
        except NoSuchElementException:
            print("Cookie button not found on the page.")
        except Exception as e:
            print(f"An error occurred while clicking the cookie button: {e}")

    def get_name(self):
        try:
            return self.driver.find_element(by=By.XPATH, value = "//h1[@class='DUwDvf lfPIob']").text
        except Exception as e:
            print(f"Error getting name: {e}")
            return None

    def get_address(self):
        try:
            return self.driver.find_element(By.XPATH, "//button[@data-tooltip='Copiar la dirección']//div[contains(@class, 'fontBodyMedium')]").text
        except Exception as e:
            print(e)
            return None

    def get_number(self):
        try:
            return self.driver.find_element(By.XPATH, "//button[@data-tooltip='Copiar el número de teléfono']//div[contains(@class, 'fontBodyMedium')]").text
        except Exception as e:
            print(e)
            return None

    def get_website(self):
        try:
            return self.driver.find_element(By.XPATH, "//a[@data-tooltip='Abrir el sitio web']").get_attribute("href")
        except Exception as e:
            print(e)
            return None

    def get_rating(self):
        try:
            return self.driver.find_element(By.XPATH, "//div[@class='fontDisplayLarge']").text
        except Exception as e:
            print(e)
            return None
        

    def get_review_number(self):
        try:
            review_text = self.driver.find_element(By.XPATH, '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]').text
            review_number = re.findall(r'\d+', review_text)[0]
            return review_number
        except Exception as e:
            print(e)
            return None
        
        
    def get_category(self):
        try:
            return self.driver.find_element(by = By.CSS_SELECTOR, value = "button[jsaction*='.category']").text
        except Exception as e:
            print(e)
            return None


    def get_geocoder(self, url_location):
        try:
            coords = re.search(r"!3d-?\d\d?\.\d{4,8}!4d-?\d\d?\.\d{4,8}", url_location).group()
            coord = coords.split('!3d')[1]
            return tuple(coord.split('!4d'))
        except Exception as e:
            print(f"Error getting geocoder: {e}")
            return None

    def take_screenshot(self, name, city):
        try:
            # Clean the business name to create a valid filename
            valid_name = re.sub(r'[\\/*?:"<>|]', "", name)
            city_folder = os.path.join("screenshots", city)
            if not os.path.exists(city_folder):
                os.makedirs(city_folder)
            screenshot_path = os.path.join(city_folder, f"{valid_name}.png")
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None

    def input_search_query(self, query):
        try:
            search_box = self.driver.find_element(By.ID, "searchboxinput")
            search_box.clear()
            search_box.send_keys(query)
            search_button = self.driver.find_element(By.ID, "searchbox-searchbutton")
            search_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
            )
        except Exception as e:
            print(f"Error inputting search query: {e}")

    def scrap_city(self, city):
        search_query = f"Notaries in {city}"
        self.input_search_query(search_query)
        self.driver.implicitly_wait(random.randint(1, 2))

        # Scroll to load more results
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Find all result elements
        elements = self.driver.find_elements(by = By.CLASS_NAME, value = "hfpxzc")
        total_elements = len(elements)
        processed_elements = 0

        while processed_elements < total_elements:
            # Re-find elements to avoid stale element references
            elements = self.driver.find_elements(by = By.CLASS_NAME, value = "hfpxzc")
            for element in elements[processed_elements:]:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    element.click()
                    time.sleep(random.randint(1, 3))

                    name = self.get_name()
                    self.names.append(name)
                    self.cities.append(city)

                    category = self.get_category()
                    self.categories.append(category)

                    address = self.get_address()
                    self.addresses.append(address)

                    number = self.get_number()
                    self.numbers.append(number)

                    website = self.get_website()
                    self.websites.append(website)

                    rating = self.get_rating()
                    self.ratings.append(rating)

                    review = self.get_review_number()
                    self.reviews.append(review)

                    geocoder = self.get_geocoder(self.driver.current_url)
                    self.geocoders.append(geocoder)

                    screenshot_path = self.take_screenshot(name, city)
                    self.screenshot_paths.append(screenshot_path)

                    processed_elements += 1
                    print(f"Processed {processed_elements} out of {total_elements} elements")
                except Exception as e:
                    print(f"An error occurred while scraping an element: {e}")
                    processed_elements += 1

            # Scroll down to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Check if new elements have been loaded
            new_total_elements = len(self.driver.find_elements(by =By.CLASS_NAME, value = "hfpxzc"))
            if new_total_elements > total_elements:
                total_elements = new_total_elements
            else:
                # If no new elements are loaded, break the loop
                break

        data_df = create_dataframe(
            names=self.names,
            categories=self.categories,
            addresses=self.addresses,
            numbers=self.numbers,
            websites=self.websites,
            ratings=self.ratings,
            reviews=self.reviews,
            geocoders=self.geocoders,
            screenshot_paths=self.screenshot_paths,
            cities=self.cities
        )

        export_data(dataframe=data_df, city=city)

    def scrap(self, url, cities):
        print(f"🚀 Starting scrape for cities: {cities}")
        for city in cities:
            print(f"🌍 Starting browser for {city}")
            self.start_browser()
            print("✅ Browser started successfully")
            try:
                self.driver.maximize_window()
                print("🔗 Going to:", url)
                self.driver.get(url=url)
                self.driver.implicitly_wait(random.randint(1, 2))
                print("🧠 Waiting before clicking cookie")
                self.click_on_cookie()
                self.driver.implicitly_wait(random.randint(1, 2))

                self.scrap_city(city)
                print(f"Completed scraping for {city}")
            except Exception as e:
                print(f"An error occurred during scraping for {city}: {e}")
            finally:
                self.close_browser()

            # Sleep for a random interval between 15 to 60 seconds before the next city
            # sleep_time = random.randint(15, 60)
            # print(f"Sleeping for {sleep_time} seconds before starting the next city...")
            # time.sleep(sleep_time)


if __name__ == "__main__":
    print("Testing running")
    url_test = "https://www.google.com/maps"
    cities = ["Blanes", "Alicante", "Girona"]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_path = os.path.join(base_dir, "chromedriver-win64", "chromedriver.exe")
    scraper_test = Scraper(chrome_path=chrome_path)
    scraper_test.scrap(url=url_test, cities=cities)
