import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


import uuid

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

def add_random_product():
    global wait
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "s")))
        search_box.clear()
        search_box.send_keys("KFD")
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)

        print("Wyszukiwanie zakończone.")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "products")))

        found_products = driver.find_elements(By.CSS_SELECTOR, ".product-miniature")
        time.sleep(2)
        if len(found_products) > 0:

            transition = False
            while (transition) == False:
                random_product = random.choice(found_products)

                print("Wylosowano: " + random_product.text)
                if "OBECNIE BRAK NA STANIE" not in random_product.text:
                    product_link = random_product.find_element(By.CSS_SELECTOR, ".product-title a")
                    time.sleep(1)
                    product_link.click()
                if "Dodaj do koszyka" in driver.page_source:
                    print("Przejście do strony produktu udane.")
                    transition = True
                else:
                    print("OBECNIE BRAK NA STANIE")
            add_to_cart2 = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
            add_to_cart2.click()
            time.sleep(3)
            print("Losowy produkt dodany do koszyka.")
            continue1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
            continue1_btn.click()

        else:
            print("Nie znaleziono żadnych produktów dla tej frazy.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
def delete_products():
    try:
        cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Koszyk')]")))
        cart_btn.click()
        time.sleep(4)
        product_id = 24
        xpath = f"//a[contains(@href, 'id_product={product_id}')]/ancestor::li//button[contains(@class, 'js-decrease-product-quantity')]"
        decrease_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        decrease_btn.click()
        decrease_btn.click()
        decrease_btn.click()
        time.sleep(3)
        print("Produkt został usunięty!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


def registration():
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

    wait.until(EC.presence_of_element_located((By.NAME, "firstname")))

    driver.find_element(By.NAME, "firstname").send_keys("Jan")
    driver.find_element(By.NAME, "lastname").send_keys("Kowalski")
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
    politic_checkbox = driver.find_element(By.NAME, "psgdpr")
    politic_checkbox.click()
    time.sleep(1)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit_btn.click()

    time.sleep(3)
    if "Wyloguj się" in driver.page_source or "Sign out" in driver.page_source or "Jan Kowalski" in driver.page_source:
        print("Zarejestrowano i zalogowano pomyślnie")
    else:
        print("Nie udało się zarejestrować")


try:


    driver.get("https://localhost:8443/")
    print("Strona otwarta.")

    print(f"Tytuł strony: {driver.title}")

    # ------- produkt z kategorii 1 dodajemy 4 sztuki
    category_btn = wait.until(EC.element_to_be_clickable((By.ID, "category-3")))
    hover = ActionChains(driver).move_to_element(category_btn) # Hover
    hover.perform()
    category_btn.click()
    time.sleep(1)
    category_heath_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Zdrowie i kondycja")))
    category_heath_btn.click()
    time.sleep(3)

    product1 = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Now Foods Omega 3 1000mg -...")))
    product1.click()
    print("Przejscie do strony produktu udane")
    time.sleep(3)
    count1 = wait.until(EC.presence_of_element_located((By.ID, "quantity_wanted")))
    count1.send_keys(Keys.CONTROL + "a")
    count1.send_keys(Keys.DELETE)
    count1.send_keys("4")
    add_to_cart = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
    add_to_cart.click()
    time.sleep(1)
    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
    continue_btn.click()
    time.sleep(3)

    # -------- produkt z kategorii 2 dodajemy 6 sztuk
    category1_btn = wait.until(EC.element_to_be_clickable((By.ID, "category-3")))
    category1_btn.click()
    time.sleep(1)
    category_clothes_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Akcesoria i ubrania")))
    category_clothes_btn.click()
    time.sleep(3)
    product2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='id_product=245']")))
    product2.click()
    print("Przejscie do strony produktu udane")
    time.sleep(3)
    count2 = wait.until(EC.presence_of_element_located((By.ID, "quantity_wanted")))
    count2.send_keys(Keys.CONTROL + "a")
    count2.send_keys(Keys.DELETE)
    count2.send_keys("6")
    add_to_cart2 = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
    add_to_cart2.click()
    time.sleep(1)
    continue1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
    continue1_btn.click()
    time.sleep(3)

    # ------- Wyszukanie produktu po nazwie i dodanie do koszyka losowego produktu spośród znalezionych
    add_random_product()

    # ------- przechodzimy do koszyka i usuwamy produkt
    delete_products()

    # ------- logowanie i rejestracja
    registration()

    # ------- realizacja zamówienia
    time.sleep(2)
    cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Koszyk')]")))
    cart_btn.click()
    time.sleep(1)
    order_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='controller=order']")))
    order_btn.click()
    print("Przechodzimy do realizacji zamówienia")
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.NAME, "firstname")))
    driver.find_element(By.NAME, "address1").send_keys("Gabriela Narutowicza 11/12")
    driver.find_element(By.NAME, "postcode").send_keys("80-233")
    driver.find_element(By.NAME, "city").send_keys("Gdańsk")
    confirm_addresses = driver.find_element(By.NAME, "confirm-addresses")
    time.sleep(2)
    confirm_addresses.click()
    print("adres jest wpisany")
    time.sleep(1)
    # Znajdź input, a potem wyjdź piętro wyżej (..)
    # To kliknie w całą otoczkę przycisku
    radio_wrapper = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='delivery_option_9']/..")))
    radio_wrapper.click()
    driver.find_element(By.NAME, "confirmDeliveryOption").click()
    time.sleep(3)
    cash_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='payment-option-2']/..")))
    cash_option.click()
    terms_input = wait.until(EC.presence_of_element_located((By.NAME, "conditions_to_approve[terms-and-conditions]")))
    driver.execute_script("arguments[0].click();", terms_input)
    time.sleep(4)
    # Szukamy buttona wewnątrz diva #payment-confirmation
    place_order_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#payment-confirmation button")))
    place_order_btn.click()
    time.sleep(5)
    print("udało się")



except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    driver.quit()
    pass
