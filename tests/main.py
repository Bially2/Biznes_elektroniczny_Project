import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import uuid

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:

    driver.get("https://localhost:8443/")
    print("Strona otwarta.")

    print(f"Tytuł strony: {driver.title}")

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "s")))
    search_box.clear()
    search_box.send_keys("KFD")
    #search_box.send_keys(Keys.RETURN)

    print("Wyszukiwanie zakończone.")
    #found_products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item")))

    # logowanie i rejestracja
    login_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Zaloguj się do swojego konta klienta']")))
    login_btn.click()
    time.sleep(1)
    print("Przejście do strony logowania.")

    reg_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".no-account a")))
    reg_btn.click()
    print("Przejście do strony rejestracji.")
    time.sleep(1)

    gender_mr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='field-id_gender-1']")))
    gender_mr.click()
    time.sleep(1)

    firstname = driver.find_element(By.NAME, "firstname").send_keys("Jan")
    lastname = driver.find_element(By.NAME, "lastname").send_keys("Kowalski")
    time.sleep(1)

    random_string = str(uuid.uuid4())[:8]
    email = f"jan.{random_string}@test.pl"
    driver.find_element(By.NAME, "email").send_keys(email)
    print(f"Użyty email: {email}")
    time.sleep(1)
    driver.find_element(By.NAME, "password").send_keys("biznes-super:)")
    time.sleep(1)

    cust_checkbox = driver.find_element(By.NAME, "customer_privacy")
    cust_checkbox.click()
    time.sleep(1)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit_btn.click()

    time.sleep(3)
    if "Wyloguj się" in driver.page_source or "Sign out" in driver.page_source or "Jan Kowalski" in driver.page_source:
        print("Zarejestrowano i zalogowano pomyślnie")
    else:
        print("Nie udało się zarejestrować")

    #if found_products:
    #    random_product = random.choice(found_products)
     #   add_button = random_product.find_element(By.CLASS_NAME, "add-to-cart-btn")
      #  add_button.click()
       # print("Losowy produkt dodany do koszyka.")
    #else:
     #   print("Nie znaleziono produktów.")



except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    driver.quit()
    pass
