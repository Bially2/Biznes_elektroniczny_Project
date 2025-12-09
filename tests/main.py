import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("testy_run.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
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
        search_box.send_keys("Creatine")
        time.sleep(2)
        search_box.submit()
        time.sleep(2)

        logging.info("Wyszukiwanie zakończone.")
        wait.until(EC.presence_of_element_located((By.ID, "products")))

        found_products = driver.find_elements(By.CSS_SELECTOR, ".product-miniature")
        time.sleep(2)
        if len(found_products) > 0:

            transition = False
            while (transition) == False:
                random_product = random.choice(found_products)

                logging.info("Wylosowano: " + random_product.text)
                if "OBECNIE BRAK NA STANIE" not in random_product.text:
                    product_link = random_product.find_element(By.CSS_SELECTOR, ".product-title a")
                    time.sleep(1)
                    product_link.click()
                if "Dodaj do koszyka" in driver.page_source:
                    logging.info("Przejście do strony produktu udane.")
                    transition = True
                else:
                    logging.info("OBECNIE BRAK NA STANIE")
            time.sleep(1)
            add_to_cart2 = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
            time.sleep(1)
            add_to_cart2.click()
            time.sleep(2)
            logging.info("Losowy produkt dodany do koszyka.")
            continue1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
            time.sleep(1)
            continue1_btn.click()

        else:
            logging.warning("Nie znaleziono żadnych produktów dla tej frazy.")
    except Exception as e:
        logging.error(f"Wystąpił błąd: {e}")


def delete_products():
    try:
        cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Koszyk')]")))
        cart_btn.click()
        time.sleep(2)

        product_id = 33
        xpath = f"//a[contains(@href, 'id_product={product_id}')]/ancestor::li//button[contains(@class, 'js-decrease-product-quantity')]"
        for i in range(3):
            decrease_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            decrease_btn.click()
            logging.info(f"Usunięecie produktu {i + 1}")
            wait.until(EC.staleness_of(decrease_btn))
        time.sleep(2)
        logging.info("Produkt został usunięty!")
    except Exception as e:
        logging.error(f"Wystąpił błąd: {e}")


def registration():
    login_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Zaloguj się do swojego konta klienta']")))
    login_btn.click()
    time.sleep(1)
    logging.info("Przejście do strony logowania.")

    reg_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".no-account a")))
    time.sleep(1)
    reg_btn.click()
    logging.info("Przejście do strony rejestracji.")
    time.sleep(1)

    wait.until(EC.presence_of_element_located((By.NAME, "firstname")))
    firstname = "Jan"
    lastname = "Kowalski"
    driver.find_element(By.NAME, "firstname").send_keys(firstname)
    time.sleep(1)
    driver.find_element(By.NAME, "lastname").send_keys(lastname)
    time.sleep(1)

    random_string = str(uuid.uuid4())[:8]
    email = f"jan.{random_string}@test.pl"
    driver.find_element(By.NAME, "email").send_keys(email)
    logging.info(f"Użyty email: {email}")
    time.sleep(1)
    driver.find_element(By.NAME, "password").send_keys("biznes-super:)")
    time.sleep(1)

    #cust_checkbox = driver.find_element(By.NAME, "customer_privacy")
    #cust_checkbox.click()
    #time.sleep(1)
    politic_checkbox = driver.find_element(By.NAME, "psgdpr")
    politic_checkbox.click()
    time.sleep(1)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit_btn.click()

    time.sleep(3)
    if "Wyloguj się" in driver.page_source or "Sign out" in driver.page_source or "Jan Kowalski" in driver.page_source:
        logging.info("Zarejestrowano i zalogowano pomyślnie")
    else:
        logging.warning("Nie udało się zarejestrować")
    return firstname, lastname

def category1():
    category_btn = wait.until(EC.element_to_be_clickable((By.ID, "category-533")))
    hover = ActionChains(driver).move_to_element(category_btn)  # Hover
    hover.perform()
    #category_btn.click()
    time.sleep(1)
    category_heath_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(normalize-space(), 'Zdrowie i kondycja')]")))
    category_heath_btn.click()
    time.sleep(2)

    product_id = "2"
    selector = f"article[data-id-product='{product_id}'] a.product-thumbnail"
    product_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    product_link.click()

    logging.info("Przejscie do strony produktu udane")
    time.sleep(2)
    count1 = wait.until(EC.presence_of_element_located((By.ID, "quantity_wanted")))
    count1.send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    count1.send_keys(Keys.DELETE)
    count1.send_keys("4")
    time.sleep(2)
    add_to_cart = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
    time.sleep(1)
    add_to_cart.click()
    logging.info("Produkty zostały dodane do koszyka")
    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
    time.sleep(1)
    continue_btn.click()
    time.sleep(3)

def category2():
    category2_btn = wait.until(EC.element_to_be_clickable((By.ID, "category-533")))
    hover = ActionChains(driver).move_to_element(category2_btn)  # Hover
    hover.perform()
    #category2_btn.click()
    time.sleep(1)
    time.sleep(1)

    category_clothes_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#category-626 > a")))
    category_clothes_btn.click()
    time.sleep(2)

    product_id = "33"
    selector = f"article[data-id-product='{product_id}'] a.product-thumbnail"
    product_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    product_link.click()

    logging.info("Przejscie do strony produktu udane")
    time.sleep(2)
    count2 = wait.until(EC.presence_of_element_located((By.ID, "quantity_wanted")))
    count2.send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    count2.send_keys(Keys.DELETE)
    count2.send_keys("6")
    time.sleep(2)
    add_to_cart2 = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
    time.sleep(1)
    add_to_cart2.click()
    logging.info("Produkty zostały dodane do koszyka")
    time.sleep(1)
    continue1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")))
    time.sleep(1)
    continue1_btn.click()
    time.sleep(3)

def order():
    time.sleep(1)
    cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Koszyk')]")))
    time.sleep(1)
    cart_btn.click()
    time.sleep(1)
    order_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='controller=order']")))
    order_btn.click()
    logging.info("Przechodzimy do realizacji zamówienia")
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.NAME, "firstname")))
    driver.find_element(By.NAME, "address1").send_keys("Gabriela Narutowicza 11/12")
    time.sleep(1)
    driver.find_element(By.NAME, "postcode").send_keys("80-233")
    time.sleep(1)
    driver.find_element(By.NAME, "city").send_keys("Gdańsk")
    confirm_addresses = driver.find_element(By.NAME, "confirm-addresses")
    time.sleep(2)
    confirm_addresses.click()
    logging.info("adres jest wpisany")
    time.sleep(1)
    radio_wrapper = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='delivery_option_10']/..")))
    time.sleep(1)
    radio_wrapper.click()
    time.sleep(0.5)
    driver.find_element(By.NAME, "confirmDeliveryOption").click()
    time.sleep(1)
    cash_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='payment-option-2']/..")))
    cash_option.click()
    terms_input = wait.until(EC.presence_of_element_located((By.NAME, "conditions_to_approve[terms-and-conditions]")))
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", terms_input)
    time.sleep(3)
    place_order_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#payment-confirmation button")))
    time.sleep(0.5)
    place_order_btn.click()
    time.sleep(3)
    logging.info("Zamówienie zostalo zatwierdzone")

def order_status(firstname, lastname):
    my_account = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{firstname} {lastname}')]")))
    time.sleep(1)
    my_account.click()
    logging.info("Przejscie do mojego konta")
    time.sleep(1)
    history_btn = wait.until(EC.element_to_be_clickable((By.ID, "history-link")))
    time.sleep(1)
    history_btn.click()
    time.sleep(2)



try:


    driver.get("https://localhost:8443/")
    logging.info("Strona otwarta.")

    logging.info(f"Tytuł strony: {driver.title}")

    # ------- produkt z kategorii 1 dodajemy 4 sztuki
    category1()

    # -------- produkt z kategorii 2 dodajemy 6 sztuk
    category2()

    # ------- Wyszukanie produktu po nazwie i dodanie do koszyka losowego produktu spośród znalezionych
    add_random_product()
    

    # ------- przechodzimy do koszyka i usuwamy produkt
    delete_products()

    # ------- logowanie i rejestracja
    firstname, lastname = registration()

    # ------- realizacja zamówienia
    order()

    # ------- sprawdzenie statusu zamówienia
    order_status(firstname, lastname)

    order_ref_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:first-child th")))
    order_reference = order_ref_element.text
    logging.info(f"Twój numer zamówienia to: {order_reference}")

    # ------ pobieranie faktury VAT
    frontend_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get("https://localhost:8443/admin-dev")

    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys("demo@prestashop.com")
    time.sleep(1)
    driver.find_element(By.NAME, "passwd").send_keys("prestashop_demo")
    time.sleep(1)
    driver.find_element(By.ID, "submit_login").click()
    time.sleep(3)
    logging.info("Udane logowanie na stronę admina")

    wait.until(EC.element_to_be_clickable((By.ID, "subtab-AdminParentOrders"))).click()
    time.sleep(0.5)
    wait.until(EC.element_to_be_clickable((By.ID, "subtab-AdminOrders"))).click()
    time.sleep(3)
    xpath_dropdown = f"//*[contains(text(), '{order_reference}')]/ancestor::tr//button[contains(@class, 'dropdown-toggle')]"
    dropdown_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dropdown)))
    dropdown_btn.click()
    xpath_status = "//button[contains(text(), 'Zamówienie oczekujące (opłacone)')]"
    time.sleep(1)
    status_option = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_status)))
    status_option.click()

    logging.info("Status zmieniony")
    time.sleep(5)
    driver.close()
    driver.switch_to.window(frontend_window)
    driver.refresh()

    invoice_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='controller=pdf-invoice']")))
    time.sleep(2)
    invoice_btn.click()
    logging.info("Faktura została pobrana")
    time.sleep(5)


except Exception as e:
    logging.error(f"Wystąpił błąd: {e}")

finally:
    driver.quit()
    pass