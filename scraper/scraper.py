#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs
from PIL import Image
from io import BytesIO
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import logging
import re
import sys

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_kfd.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================================
# KONFIGURACJA ŚCIEŻEK
# ========================================
CHROMEDRIVER_PATH = None  # Ustaw ścieżkę do ChromeDriver, jeśli nie jest w PATH


class KFDScraper:
    def __init__(self, base_url="https://sklep.kfd.pl/", output_dir="data_kfd", max_workers=3):
        self.base_url = base_url
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.max_workers = max_workers
        self.create_directories()

        self.categories = []
        self.products = []
        self.lock = Lock()
        self.seen_products = set()

        logger.info(f"Inicjalizacja scrapera KFD (workers: {max_workers})")

    def create_directories(self):
        """Tworzy strukturę katalogów"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    def create_driver(self):
        """Tworzy nową instancję driver'a"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        if CHROMEDRIVER_PATH:
            service = Service(CHROMEDRIVER_PATH)
        else:
            service = Service()

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            logger.error(f"Nie można uruchomić Chrome. Sprawdź Chromedriver w PATH/ścieżce: {e}")
            raise

    def wait_for_page_load(self, driver, timeout=30):
        """Czeka na załadowanie strony"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(1)
        except TimeoutException:
            logger.warning("Timeout - kontynuuję mimo to")

    def clean_url(self, url):
        """Usuwa z linku zabronione parametry zgodnie z robots.txt KFD."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Parametry do usunięcia zgodnie z robots.txt KFD
        safe_params = {
            key: value
            for key, value in query_params.items()
            if key not in ['order', 'tag', 'id_currency', 'search_query', 'back', 'n', 'p']
        }

        # Rekonstrukcja URL bez zabronionych parametrów
        cleaned_url = urlunparse(parsed_url._replace(query=requests.compat.urlencode(safe_params, doseq=True)))

        # Filtrujemy ścieżki zabronione
        forbidden_paths = ['/controller=addresses', '/controller=cart', '/controller=search', '/login', '/my-account',
                           '/order']
        for path in forbidden_paths:
            if path in cleaned_url:
                return None

        return cleaned_url

    def extract_categories_from_jsonld(self, driver):
        """Pobiera hierarchię kategorii z danych JSON-LD, wymuszając pobranie zawartości tagu script."""

        # Używamy JavaScriptu do znalezienia i pobrania wszystkich tagów script typu application/ld+json
        js_script = """
        const scripts = document.querySelectorAll('script[type="application/ld+json"]');
        if (scripts.length === 0) return null;

        // Przechodzimy przez wszystkie skrypty i szukamy BreadcrumbList
        for (let i = 0; i < scripts.length; i++) {
            try {
                const content = JSON.parse(scripts[i].textContent);
                if (content['@type'] === 'BreadcrumbList') {
                    return JSON.stringify(content.itemListElement);
                }
            } catch (e) {
                // Ignore parsing errors
            }
        }
        return null;
        """

        try:
            json_array_str = driver.execute_script(js_script)

            if json_array_str:
                data = json.loads(json_array_str)
                logger.info("Dane JSON-LD (Breadcrumbs) pobrane pomyślnie przez JS.")
                return data

        except Exception as e:
            logger.error(f"  Błąd wykonania skryptu JS do pobrania JSON-LD: {e}")

        logger.warning("Brak JSON-LD BreadcrumbList na stronie produktu.")
        return None

    def get_product_urls_from_category(self, category_url, category_name, limit=None):
        """Pobiera listę URL produktów z kategorii KFD, obsługując paginację i filtrowanie."""
        logger.info(f"Skanowanie: {category_name} ({category_url})")
        driver = self.create_driver()
        product_urls = []
        page_url = category_url
        page_count = 1

        try:
            while page_url:
                if limit and len(product_urls) >= limit:
                    logger.info(f"Osiągnięto limit {limit} produktów. Przerywanie skanowania linków.")
                    break

                logger.info(f"Ładowanie strony {page_count}: {page_url}")
                driver.get(page_url)
                self.wait_for_page_load(driver)

                driver.implicitly_wait(0)  # Wyłączamy implicit wait dla szybszej analizy kart

                # Używamy scrollowania, aby aktywować ewentualny lazy loading
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)

                # --- ZBIERANIE PRODUKTÓW Z BIEŻĄCEJ STRONY ---

                product_card_selectors = ["article.product-miniature", "div.product"]
                product_cards = []
                for selector in product_card_selectors:
                    try:
                        product_cards.extend(driver.find_elements(By.CSS_SELECTOR, selector))
                        if product_cards: break
                    except NoSuchElementException:
                        continue

                if not product_cards:
                    logger.warning(f"Brak produktów na stronie {page_count}.")

                    break  # W przypadku braku produktów na pierwszej stronie

                current_page_products = []
                for card in product_cards:
                    try:
                        # Link produktu na KFD to zwykle a.thumbnail (zgodnie ze zrzutami)
                        link = card.find_element(By.CSS_SELECTOR, "a.thumbnail")
                        url = self.clean_url(link.get_attribute("href"))

                        if url and url not in self.seen_products:
                            self.seen_products.add(url)
                            product_urls.append((url, category_name))
                            current_page_products.append(url)  # Zbieramy linki TYLKO z tej strony

                            if limit and len(product_urls) >= limit:
                                page_url = None  # Przerwij paginację
                                break

                    except NoSuchElementException:
                        continue
                    except Exception as e:
                        logger.warning(f"Błąd przetwarzania karty: {e}")
                        continue

                if not page_url: break  # Limit osiągnięty

                # --- PORÓWNANIE PRZECIWKO NIESKOŃCZONEJ PĘTLI ---

                # --- OBSŁUGA PAGINACJI ---
                next_page_link = None

                try:
                    # KROK 3: Szukamy linku z atrybutem rel='next' (STANDARD SEO DLA NASTĘPNEJ STRONY)
                    next_page_link = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")

                    next_url = next_page_link.get_attribute("href")
                    cleaned_next_url = self.clean_url(next_url)  # Czyścimy URL

                    if cleaned_next_url and cleaned_next_url != page_url:
                        page_url = cleaned_next_url
                        page_count += 1
                        logger.info(f"Przechodzę do strony {page_count}.")
                    else:
                        page_url = None  # Koniec paginacji (lub błąd czyszczenia URL)

                except NoSuchElementException:
                    page_url = None  # Koniec paginacji (nie ma linku rel='next')
                except Exception as e:
                    logger.warning(f"Błąd paginacji: {e}")
                    page_url = None  # Zakończ w przypadku nieznanego błędu

        except Exception as e:
            logger.error(f"Błąd podczas skanowania kategorii: {e}")
        finally:
            driver.implicitly_wait(10)
            driver.quit()

        logger.info(f"Znaleziono {len(product_urls)} unikalnych URL produktów.")
        return product_urls

    def extract_full_jsonld(self, driver):
        """Pobiera wszystkie dane z JSON-LD, szukając głównego bloku Product."""
        js_script = """
        const scripts = document.querySelectorAll('script[type="application/ld+json"]');
        if (scripts.length === 0) return null;

        for (let i = 0; i < scripts.length; i++) {
            try {
                const content = JSON.parse(scripts[i].textContent);
                // Szukamy głównego bloku typu Product
                if (content['@type'] === 'Product') {
                    return JSON.stringify(content);
                }
            } catch (e) {
                // Ignore parsing errors
            }
        }
        return null;
        """
        try:
            json_str = driver.execute_script(js_script)
            if json_str:
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Błąd wykonania skryptu JS do pobrania pełnego JSON-LD: {e}")
        return None

    def scrape_product_details(self, product_url, category_name):
        """Pobiera szczegóły produktu, używając JSON-LD jako backup dla wagi/marki."""
        driver = self.create_driver()

        try:
            driver.get(product_url)
            self.wait_for_page_load(driver)

            product_data = {
                "url": product_url,
                "category": category_name,
                "name": "",
                "description": "",
                "price": "",
                "reference": f"KFD_{hashlib.sha256(product_url.encode()).hexdigest()[:8]}",
                "attributes": {},
                "images": [],
                "usage": "",
                "weight": "",  # Inicjalizacja: Waga
                "brand": ""  # Inicjalizacja: Marka
            }

            # --- KROK 0a: POBIERANIE WAGI I MARKI Z PEŁNEGO JSON-LD (Jako priorytetowe źródło) ---
            jsonld_data = self.extract_full_jsonld(driver)

            if jsonld_data:
                # Waga z JSON-LD
                weight_data = jsonld_data.get("weight", {})
                if weight_data and weight_data.get('value'):
                    # Zachowaj tylko wartość liczbową wagi
                    product_data["weight"] = re.sub(r'[^\d.]', '', str(weight_data['value']))
                    logger.info(f"Waga produktu: {product_data['weight']} (bez jednostek)")

                # Producent z JSON-LD
                brand_data = jsonld_data.get("brand", {})
                if brand_data and brand_data.get('name'):
                    product_data["brand"] = brand_data["name"].strip()
                    logger.info("Producent produktu pobrany z JSON-LD.")

            # --- KROK 0b: POBIERANIE HIERARCHII Z BREADCRUMBÓW ---
            breadcrumb_elements = self.extract_categories_from_jsonld(driver)

            if breadcrumb_elements:
                self.lock.acquire()
                try:
                    self.update_categories_from_breadcrumbs(breadcrumb_elements)
                finally:
                    self.lock.release()

                category_path_names = []
                for element in breadcrumb_elements:
                    # Pomijamy 'Strona główna' i sam produkt (zawsze ostatni element)
                    name = element.get('name', '').strip()
                    if name and name.lower() != 'strona główna' and element.get('position', 0) < len(
                            breadcrumb_elements):
                        category_path_names.append(name)

                # Tworzymy ścieżkę w formacie wymaganym przez Prestashop (np. Kategoria A > Kategoria B)
                # Użyjemy separatora, który jest bezpieczny (np. > lub |)
                product_data['category'] = ",".join(category_path_names)

                if not product_data['category']:
                    # Używamy pierwotnej kategorii, jeśli Breadcrumb nie zadziałał
                    product_data['category'] = category_name

            # --- KLUCZOWY KROK 1: POBIERANIE DANYCH Z JSON (data-product) ---
            try:
                data_element = driver.find_element(By.CSS_SELECTOR, "div.js-product-details")
                json_data_str = data_element.get_attribute('data-product')
                product_json = json.loads(json_data_str)
                logger.info("Dane JSON produktu pobrane pomyślnie z data-product.")
            except Exception as e:
                logger.error(f"Błąd krytyczny: Nie można pobrać/sparsować JSON (data-product): {e}")
                return None

            # --- KROK 2: EKSTRAKCJA DANYCH Z JSON (data-product) ---

            # 1. NAZWA, CENA, REFERENCJA
            product_data["name"] = product_json.get("name", "").strip()
            price_text = product_json.get("price", "0.00").replace(u'\xa0zł', '').replace(',', '.')
            product_data["price"] = re.sub(r'[^\d.]', '', price_text)
            product_data["reference"] = product_json.get("reference", product_data["reference"]).strip()

            # 2. OPIS
            raw_description = product_json.get("description", "")
            product_data["description"] = BeautifulSoup(raw_description, 'html.parser').get_text(separator=' ',
                                                                                                 strip=True)[:2000]

            # 3. SPOSÓB UŻYCIA (EXTRA CONTENT)
            extra_content = product_json.get("extraContent", [])
            for item in extra_content:
                if item.get("title", "").lower() == "sposób użycia":
                    usage_html = item.get("content", "")
                    product_data["usage"] = BeautifulSoup(usage_html, 'html.parser').get_text(separator=' ',
                                                                                              strip=True)[:1000]
                    logger.info("Sposób użycia pobrany z data-product.")
                    break

            # 4. WAGA (Nadpisanie tylko jeśli data-product ma kompletną wagę)
            weight_data_product = product_json.get("weight", {})
            if weight_data_product and weight_data_product.get('value') and weight_data_product.get('unitCode'):
                product_data["weight"] = weight_data['value']
                logger.info(f"Waga produktu: {product_data['weight']} (z data-product, nadpisano)")
            # ELSE: Zostawiamy wartość z JSON-LD

            # 5. PRODUCENT (Nadpisanie tylko jeśli data-product ma kompletną markę)
            brand_data_product = product_json.get("brand", {})
            if brand_data_product and brand_data_product.get("name"):
                product_data["brand"] = brand_data_product["name"].strip()
                logger.info(f"Producent produktu: {product_data['brand']} (z data-product, nadpisano)")
            # ELSE: Zostawiamy wartość z JSON-LD

            # 6. ZDJĘCIA (Link HR z JSON)
            try:
                images = []
                # Pobierz zdjęcie home_default
                if 'home_default' in product_json['cover']['bySize']:
                    home_default_url = self.clean_url(product_json['cover']['bySize']['home_default']['url'])
                    images.append(home_default_url)

                # Pobierz zdjęcie large_default
                if 'large_default' in product_json['cover']['bySize']:
                    large_default_url = self.clean_url(product_json['cover']['bySize']['large_default']['url'])
                    images.append(large_default_url)

                product_data["images"] = images
                logger.info(f"Zdjęcia produktu: {product_data['images']}")
            except Exception as e:
                logger.warning(f"Nie udało się pobrać zdjęć: {e}")

            # --- ZAKOŃCZENIE FUNKCJI ---
            if not product_data["name"]:
                logger.warning("Produkt odrzucony: Nazwa pusta.")
                return None

            return product_data

        except Exception as e:
            logger.error(f"Błąd krytyczny podczas scrapowania (JSON lub ogólny): {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            driver.quit()

    def update_categories_from_breadcrumbs(self, breadcrumb_elements):
        """
        Aktualizuje self.categories na podstawie danych z BreadcrumbList,
        tworząc hierarchię.
        """
        last_parent_id = 0

        # Tworzymy mapowanie URL -> ID dla szybkiego sprawdzania duplikatów
        url_to_id = {c['url']: c['id'] for c in self.categories}

        for element in breadcrumb_elements:
            # Pomijamy 'Strona główna' i sam produkt (zawsze ostatni element)
            if element.get('name', '').lower() == 'strona główna' or element.get('position', 0) == len(
                    breadcrumb_elements):
                continue

            name = element.get('name', '').strip()
            url = self.clean_url(element.get('item', ''))

            if url and name and url not in url_to_id:
                # To jest nowa kategoria, dodajemy ją
                new_id = len(self.categories) + 3

                cat_data = {
                    "id": new_id,
                    "name": name,
                    "url": url,
                    "parent_id": last_parent_id,
                    "active": 1
                }

                self.categories.append(cat_data)
                url_to_id[url] = new_id
                logger.info(f"Nowa kategoria z Breadcrumb (ID:{new_id}, P:{last_parent_id}): {name}")

                # Ustawiamy nową kategorię jako rodzica dla kolejnych elementów
                last_parent_id = new_id

            elif url and url in url_to_id:
                # Jeśli kategoria już istnieje, aktualizujemy ID rodzica dla kolejnego elementu
                last_parent_id = url_to_id[url]

        # Sprawdzamy, czy wszystkie kategorie mają rodzica
        for category in self.categories:
            if category['parent_id'] == 0:
                logger.warning(
                    f"Kategoria '{category['name']}' nie miała rodzica. Ustawiono 'KATEGORIE' jako rodzica.")
                category['parent_id'] = 1

    def download_image(self, url, product_name, index, referer_url):
        """Pobiera zdjęcie i zwraca (Oryginalny URL, Nazwa Pliku)."""
        # --- FIX: AGRESYWNE NAGŁÓWKI DO POBIERANIA OBRAZÓW ---
        HEADERS_IMG = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            # NAJWAŻNIEJSZE: Używamy URL strony detali jako referera
            'Referer': referer_url
        }

        cleaned_url = self.clean_url(url)  # Używamy wyczyszczonego URL

        if not cleaned_url:
            logger.warning(f"URL do zdjęcia jest pusty po czyszczeniu: {url[:60]}")
            return None

        try:
            # Używamy ulepszonych nagłówków
            response = requests.get(cleaned_url, headers=HEADERS_IMG, timeout=10)

            if response.status_code != 200:
                logger.warning(
                    f"BŁĄD HTTP ({response.status_code}): Serwer odrzucił żądanie dla {cleaned_url[:60]}")
                return None

            # Zmiana limitu wymiarów na 300px
            img = Image.open(BytesIO(response.content))
            width, height = img.size

            # --- ZAPIS PLIKU ---
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_'))
            safe_name = safe_name.strip().replace(' ', '_')[:50]
            img_hash = hashlib.md5(cleaned_url.encode()).hexdigest()[:8]

            extension = cleaned_url.split('.')[-1].split('?')[0][:4]
            if extension not in ['jpg', 'jpeg', 'png', 'webp']:
                extension = 'jpg'

            filename = f"{safe_name}_{index}_{img_hash}.{extension}"
            filepath = os.path.join(self.images_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            logger.info(f"Zapisano zdjęcie: {filename} ({width}x{height}px)")

            # ZWRACAMY TERAZ KROTKĘ (ORYGINALNY_URL, LOKALNA_NAZWA_PLIKU)
            return (cleaned_url, filename)

        except Exception as e:
            logger.error(f"Błąd krytyczny podczas zapisywania/pobierania: {e}")
            return None

    def process_product_batch(self, product_urls_batch):
        """Przetwarza batch produktów (wywołuje scrape_product_details)."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Prawidłowa składnia: product_urls_batch zawiera (url, cat_name)
            future_to_url = {
                executor.submit(self.scrape_product_details, url, cat_name): (url, cat_name)
                for url, cat_name in product_urls_batch
            }

            for future in as_completed(future_to_url):
                url, cat_name = future_to_url[future]
                try:
                    product_data = future.result()
                    if product_data and product_data.get("name"):
                        results.append(product_data)
                        logger.info(f"Przetworzono: {product_data['name']} - {product_data.get('price', 'N/A')} PLN")
                except Exception as e:
                    logger.error(f"Błąd: {e}")

        return results

    def download_images_batch(self, products):
        """Pobiera zdjęcia, przekazując URL strony detali jako Referer."""
        total_images = sum(len(p['images']) for p in products)
        logger.info(f"Pobieranie {total_images} zdjęć...")

        download_tasks = []
        for product in products:
            referer_url = product['url']

            for idx, img_url in enumerate(product['images'][:2], 1):
                # ZADANIE: (url, name, idx, referer_url)
                download_tasks.append((img_url, product['name'], idx, referer_url))

        with ThreadPoolExecutor(max_workers=self.max_workers * 2) as executor:
            future_to_task = {
                # Używamy tylko 4 wymaganych argumentów
                executor.submit(self.download_image, url, name, idx, referer_url_arg): (
                    url, name, idx, referer_url_arg)
                for url, name, idx, referer_url_arg in download_tasks
            }

            for future in as_completed(future_to_task):
                url, name, idx, referer_url_arg = future_to_task[future]
                product = next((p for p in products if p['url'] == referer_url_arg), None)

                if not product: continue

                try:
                    # Oczekujemy teraz krotki (original_url, filename)
                    result_tuple = future.result()

                    if result_tuple:
                        original_url, filename = result_tuple

                        if 'local_images' not in product:
                            # Zmieniamy to na listę przechowującą słowniki
                            product['local_images'] = []

                            # Zapisujemy OBA elementy
                        product['local_images'].append({
                            'url': original_url,
                            'filename': filename
                        })
                except Exception:
                    pass

    def export_to_prestashop_csv(self):
        """Eksportuje do CSV w formacie PrestaShop."""
        logger.info("\nEksportowanie...")

        # Kategorie
        # Mapowanie ID na Nazwę dla łatwego znalezienia nazwy rodzica
        id_to_name = {cat['id']: cat['name'] for cat in self.categories}
        id_to_name[0] = ''  # Domyślna nazwa dla braku rodzica

        # Kategorie
        categories_file = os.path.join(self.output_dir, "categories.csv")
        with open(categories_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # UPROSZCZONY NAGŁÓWEK:
            writer.writerow(['ID', 'Active', 'Name', 'Parent Name', 'Root Category'])

            for cat in self.categories:
                parent_name = '' if cat['name'] == 'KATEGORIE' else id_to_name.get(cat['parent_id'], 'KATEGORIE')

                is_root = 1 if cat['id'] == 3 else 0

                # Zapisujemy tylko 5 wymaganych pól
                writer.writerow([
                    cat['id'],
                    cat['active'],
                    cat['name'],
                    parent_name,
                    is_root
                ])

        logger.info(f"Zapisano uproszczoną strukturę kategorii: {categories_file}")

        # Produkty
        products_file = os.path.join(self.output_dir, "products.csv")
        with open(products_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')

            # Nagłówki
            writer.writerow([
                'ID', 'Name', 'Categories', 'Price',
                'Reference', 'Description', 'Usage', 'Weight', 'Brand', 'Image URLs', 'Feature'
            ])

            for idx, product in enumerate(self.products, 3):
                attributes_text = "; ".join(
                    [f"{k}:{v}:0" for k, v in product['attributes'].items()]
                )

                # Dodanie "sposobu użycia" jako cechy
                usage_feature = ""
                if product.get('usage'):
                    usage_feature = f"Sposób użycia:{product['usage']}:0:1"

                # Połączenie cech z innymi atrybutami
                if attributes_text:
                    attributes_text = f"{attributes_text}; {usage_feature}"
                else:
                    attributes_text = usage_feature

                weight = product.get('weight', '')
                if weight:
                    weight = re.sub(r'[^\d.]', '', weight)  # Zachowaj tylko cyfry i kropki

                image_urls = ",".join(product.get('images', []))
                final_category_export = product['category'].replace(';', '^')

                writer.writerow([
                    idx,
                    product['name'],
                    final_category_export,
                    product['price'],
                    product['reference'],
                    product['description'],
                    product.get('usage', ''),  # Nadal zapisujemy "sposób użycia" w osobnej kolumnie
                    weight,
                    product.get('brand', ''),
                    image_urls,
                    attributes_text  # Zaktualizowane cechy
                ])

        logger.info(f"Zapisano produkty: {products_file}")

        # Producenci
        brands_file = os.path.join(self.output_dir, "producenci.csv")
        unique_brands = set(product.get('brand', '').strip() for product in self.products if product.get('brand'))
        with open(brands_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['ID', 'Name', 'Active'])  # Nagłówki pliku CSV
            for idx, brand in enumerate(sorted(unique_brands), 1):
                writer.writerow([idx, brand, 1])

        logger.info(f"Zapisano producentów: {brands_file}")

        # JSON
        json_file = os.path.join(self.output_dir, "all_data.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'categories': self.categories,
                'products': self.products
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"Zapisano JSON: {json_file}\n")

    def run(self, categories_limit=None, products_per_category=None, batch_size=10):
        """
        Uruchamia scraping, bazując na wcześniej zainicjowanej liście self.categories
        i pomija funkcję scrape_all_categories_from_menu.
        """
        start_time = time.time()

        logger.info("=" * 60)
        logger.info("SCRAPER KFD - START")
        logger.info("=" * 60)

        try:
            # 1. KATEGORIE (Ten krok był wcześniej self.scrape_all_categories_from_menu())
            # Ponieważ lista self.categories jest inicjowana ręcznie w __main__,
            # pomijamy ten krok, ale sprawdzamy, czy została zainicjowana.

            if not self.categories:
                logger.error("Brak zainicjowanej kategorii startowej. Kończę.")
                return

            categories_to_process = self.categories[:categories_limit] if categories_limit else self.categories

            # 2. PRODUKTY (Zaczynamy od skanowania linków)
            all_product_urls = []
            for category in categories_to_process:
                # W tym miejscu uruchamia się get_product_urls_from_category,
                # która następnie wywoła scrape_product_details, a ta z kolei
                # zbuduje pełną listę self.categories z Breadcrumbów.
                urls = self.get_product_urls_from_category(
                    category['url'],
                    category['name'],
                    limit=products_per_category
                )
                all_product_urls.extend(urls)
                time.sleep(1)

            if not all_product_urls:
                logger.error("Brak produktów do przetworzenia.")
                return

            logger.info(f"\n{len(all_product_urls)} produktów do przetworzenia")
            logger.info(f"Batch po {batch_size}\n")

            # 3. Batch processing
            for i in range(0, len(all_product_urls), batch_size):
                batch = all_product_urls[i:i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (len(all_product_urls) + batch_size - 1) // batch_size

                logger.info(f"Batch {batch_num}/{total_batches}")

                products_data = self.process_product_batch(batch)

                if products_data:
                    self.download_images_batch(products_data)

                    with self.lock:
                        self.products.extend(products_data)

                logger.info(f"Łącznie: {len(self.products)} produktów\n")

            # 4. Export
            self.export_to_prestashop_csv()

            elapsed = time.time() - start_time
            logger.info("=" * 60)
            logger.info(f"ZAKOŃCZONO w {elapsed / 60:.1f} min")
            logger.info(f"Kategorie: {len(self.categories)}")
            logger.info(f"Produkty: {len(self.products)}")
            logger.info(f"Zdjęcia: {sum(len(p.get('local_images', [])) for p in self.products)}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\nBŁĄD: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    scraper = KFDScraper(
        max_workers=8  
    )

    # --- RĘCZNA DEFINICJA KATEGORII STARTOWEJ ---
    
    TARGET_URL = "https://sklep.kfd.pl/sklep-kfd-c-2.html"
    CATEGORY_NAME = "KATEGORIE"

    # Wstawiamy kategorię, która reprezentuje stronę wejściową
    scraper.categories = [{
        "id": 3,
        "name": CATEGORY_NAME,
        "url": TARGET_URL,
        "parent_id": 0,
        "active": 1,
        "root_category": 1
    }]

    logger.info("--- START PEŁNEGO SKANOWANIA Z WYDOBYCIEM HIERARCHII Z PRODUKTÓW ---")

    

    scraper.run(
        categories_limit=1,  # Przetwarzamy tylko tę jedną, ręcznie dodaną kategorię
        products_per_category=1200,  # Ilosc produktow do pobrania calkowicie
        batch_size=8
    )

    logger.info(f"--- ZAKOŃCZONO. Pobrano {len(scraper.categories)} kategorii z Breadcrumbs. ---")