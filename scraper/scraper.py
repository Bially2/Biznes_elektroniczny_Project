#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper KFD.pl - Wersja Finalna z Selenium i optymalizacją pod Prestashop CSV
"""

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
#CHROMEDRIVER_PATH = None  # Ustaw ścieżkę do ChromeDriver, jeśli nie jest w PATH
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

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

        logger.info(f"🚀 Inicjalizacja scrapera KFD (workers: {max_workers})")

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
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # --- NOWY FIX: WZMOCNIONE ARGUMENTY SERWISU ---
        service_args = [
            '--start-maximized', 
            '--disable-dev-shm-usage',
            '--verbose',
            '--start-server-timeout=180' # Dajemy 3 minuty na start drivera
        ]

        if CHROMEDRIVER_PATH:
            service = Service(CHROMEDRIVER_PATH, service_args=service_args)
        else:
            service = Service(service_args=service_args)

        try:
            # Używamy tylko standardowych argumentów konstruktora, ponieważ service_start_timeout nie działa
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            logger.error(f"❌ Nie można uruchomić Chrome. Sprawdź Chromedriver w PATH/ścieżce: {e}")
            raise

    def wait_for_page_load(self, driver, timeout=30):
        """Czeka na załadowanie strony"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)
        except TimeoutException:
            logger.warning("⚠️  Timeout - kontynuuję mimo to")

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

    def scrape_all_categories_from_menu(self):
        """
        Pobiera linki do wszystkich kategorii i podkategorii (P1, P2, P3) ze strony głównej,
        używając wzorca URL do ustalania hierarchii (Parent ID).
        """
        logger.info("📂 Pobieranie hierarchii kategorii z URL Heuristics...")
        driver = self.create_driver()

        try:
            driver.get(self.base_url)

            # 1. Jawne oczekiwanie na pojawienie się JAKIEGOKOLWIEK linku kategorii
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/kategoria-'], a[href*='-c-']"))
            )
            logger.info("✓ Strona i linki kategorii załadowane.")

            # Szukamy WSZYSTKICH linków pasujących do wzorca kategorii z CAŁEGO DOM
            all_category_link_elements = driver.find_elements(
                By.CSS_SELECTOR,
                "a[href*='/kategoria-'], a[href*='-c-']"
            )

            if not all_category_link_elements:
                logger.error("❌ Nie znaleziono żadnych linków pasujących do wzorca URL kategorii.")
                return

            # --- KROK 1: WSTĘPNE ZBIERANIE I FILTROWANIE ---

            # Mapowanie URL -> Dane kategorii
            categories_map = {}
            # Definicja 4 głównych kategorii L1 (na podstawie Twojego zrzutu)
            main_names = ["ODŻYWKI I SUPLEMENTY", "ZDROWE I KONDYCJA", "ŻYWNOŚĆ DIETETYCZNA", "ODZIEŻ I AKCESORIA"]

            for link_elem in all_category_link_elements:
                try:
                    name = link_elem.text.strip()
                    url = self.clean_url(link_elem.get_attribute('href'))

                    if url and len(name) > 3 and url not in categories_map:
                        is_l1 = (name.upper() in main_names)  # Sprawdzamy, czy to jedna z 4 głównych

                        cat_data = {
                            "id": 0,
                            "name": name,
                            "url": url,
                            "parent_id": 0 if is_l1 else -1,  # -1 = Rodzic nieznany (jest podkategorią)
                            "active": 1
                        }
                        categories_map[url] = cat_data

                except Exception:
                    continue

            # --- KROK 2: ALGORYTM USTALANIA RODZIC-DZIECKO ---

            # Sortujemy według długości URL, aby najpierw przetwarzać główne (krótsze URL)
            sorted_categories = sorted(categories_map.values(), key=lambda x: len(x['url']))

            self.categories = []  # Resetujemy, aby budować ostateczną listę
            current_id = 1

            for cat in sorted_categories:
                # 1. Przydziel ID
                cat['id'] = current_id

                # 2. Ustalanie rodzica dla podkategorii (Parent ID = -1)
                if cat['parent_id'] == -1:
                    best_parent_id = 0

                    # Szukamy najlepiej pasującego rodzica (najdłuższy pasujący URL)
                    for potential_parent in self.categories:
                        # Warunki: URL obecnej kategorii zaczyna się od URL rodzica ORAZ nie jest tą samą kategorią
                        if cat['url'].startswith(potential_parent['url']) and cat['url'] != potential_parent['url']:

                            # Logika: Bierzemy najdłuższego pasującego URL (czyli najbliższego rodzica)
                            current_parent_url_len = len(
                                self.categories[best_parent_id - 1]['url'] if best_parent_id else "")
                            if len(potential_parent['url']) > current_parent_url_len:
                                best_parent_id = potential_parent['id']

                    cat['parent_id'] = best_parent_id

                # Finalna weryfikacja (Poziom 1 zostaje z Parent ID = 0)
                if cat['parent_id'] == -1: cat['parent_id'] = 0

                # Dodajemy do listy finalnej
                self.categories.append(cat)
                current_id += 1

                logger.info(f"  ✓ ID {cat['id']} (P:{cat['parent_id']}): {cat['name']}")

        except Exception as e:
            logger.error(f"❌ Błąd krytyczny podczas pobierania menu: {e}")
            import traceback
            traceback.print_exc()
        finally:
            driver.quit()

        logger.info(f"✅ Pobrano {len(self.categories)} kategorii i podkategorii z URL.")

    def get_product_urls_from_category(self, category_url, category_name, limit=None):
        """Pobiera listę URL produktów z kategorii KFD, obsługując paginację i filtrowanie."""
        logger.info(f"🔍 Skanowanie: {category_name} ({category_url})")
        driver = self.create_driver()
        product_urls = []
        page_url = category_url
        page_count = 1
        last_product_count = -1  # Nowa zmienna do śledzenia liczby produktów z poprzedniej strony

        try:
            while page_url:
                logger.info(f"🌐 Ładowanie strony {page_count}: {page_url}")
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
                    logger.warning(f"  ⚠️ Brak produktów na stronie {page_count}.")

                    # WARUNEK ZAKOŃCZENIA 1: Jeśli to nie jest pierwsza strona i nie ma produktów, to jest koniec.
                    if page_count > 1 and last_product_count > 0:
                        logger.info("  ⚠️ Poprzednia strona miała produkty, a ta nie. Koniec paginacji.")
                        break

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
                        logger.warning(f"  ⚠️ Błąd przetwarzania karty: {e}")
                        continue

                if not page_url: break  # Limit osiągnięty

                # --- PORÓWNANIE PRZECIWKO NIESKOŃCZONEJ PĘTLI ---

                # WARUNEK ZAKOŃCZENIA 2: Jeśli liczba produktów jest taka sama jak na poprzedniej stronie,
                # a my próbujemy iść dalej (np. Strona 6 -> Strona 7)
                if page_count > 1 and len(current_page_products) == last_product_count and last_product_count > 0:
                    logger.warning("  ⚠️ Wykryto powtarzanie ostatniej strony. Koniec pętli.")
                    break

                last_product_count = len(current_page_products)

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
                        logger.info(f"  ↪️ Przechodzę do strony {page_count}.")
                    else:
                        page_url = None  # Koniec paginacji (lub błąd czyszczenia URL)

                except NoSuchElementException:
                    page_url = None  # Koniec paginacji (nie ma linku rel='next')
                except Exception as e:
                    logger.warning(f"  ⚠️ Błąd paginacji: {e}")
                    page_url = None  # Zakończ w przypadku nieznanego błędu

        except Exception as e:
            logger.error(f"❌ Błąd podczas skanowania kategorii: {e}")
        finally:
            driver.implicitly_wait(10)
            driver.quit()

        logger.info(f"  ✅ Znaleziono {len(product_urls)} unikalnych URL produktów.")
        return product_urls

    def scrape_product_details(self, product_url, category_name):
        """Pobiera szczegóły produktu, wykorzystując osadzone dane JSON (data-product)."""
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
                "images": []
            }

            # --- KLUCZOWY KROK 1: POBIERANIE DANYCH Z JSON ---
            try:
                # Szukamy kontenera danych Prestashop (zgodnie z załączonym kodem)
                data_element = driver.find_element(By.CSS_SELECTOR, "div.js-product-details")
                json_data_str = data_element.get_attribute('data-product')
                product_json = json.loads(json_data_str)
                logger.info("  ✓ Dane JSON produktu pobrane pomyślnie.")
            except Exception as e:
                logger.error(f"  ❌ Błąd krytyczny: Nie można pobrać/sparsować JSON (data-product): {e}")
                return None

            # --- KROK 2: EKSTRAKCJA DANYCH Z JSON ---

            # 1. NAZWA, CENA, REFERENCJA
            product_data["name"] = product_json.get("name", "").strip()
            # Cena zawiera walutę i jest w formacie "55,55 zł"
            price_text = product_json.get("price", "0.00").replace(u'\xa0zł', '').replace(',', '.')
            product_data["price"] = re.sub(r'[^\d.]', '', price_text)
            product_data["reference"] = product_json.get("reference", product_data["reference"]).strip()

            # 2. OPIS
            # Opis jest w HTML. Używamy Beautiful Soup do usunięcia tagów (jeśli nie jest zbyt skomplikowany)
            raw_description = product_json.get("description", "")
            product_data["description"] = BeautifulSoup(raw_description, 'html.parser').get_text(separator=' ',
                                                                                                 strip=True)[:2000]

            # 3. SPOSÓB UŻYCIA (FIXED z extraContent)
            product_data["usage"] = ""
            extra_content = product_json.get("extraContent", [])
            for item in extra_content:
                if item.get("title", "").lower() == "sposób użycia":
                    # Treść też jest w HTML, parsujemy BS4
                    usage_html = item.get("content", "")
                    product_data["usage"] = BeautifulSoup(usage_html, 'html.parser').get_text(separator=' ',
                                                                                              strip=True)[:1000]
                    logger.info("  ✓ Sposób użycia pobrany z JSON.")
                    break

            # 4. ATRYBUTY (Specyfikacja)
            # Te dane najczęściej nie są w data-product, więc wciąż musimy użyć selektorów dla specyfikacji,
            # ALE usuwamy wszystkie poprzednie selektory dla Nazwy/Ceny/Opisu.
            try:
                spec_table = driver.find_elements(By.CSS_SELECTOR,
                                                  "#product_attributes_list li, .product_attributes_table li")
                for item in spec_table:
                    text = item.text.strip()
                    if ":" in text:
                        key, value = text.split(":", 1)
                        product_data["attributes"][key.strip()] = value.strip()
            except:
                pass

            # 5. ZDJĘCIA (Link HR jest w JSON'ie, ale dla bezpieczeństwa używamy obecnej logiki)
            try:
                # W JSON mamy cover/large_default. Używamy dużego zdjęcia z cover:
                cover_image_url = product_json['cover']['bySize']['large_default']['url']
                product_data["images"] = [self.clean_url(cover_image_url)]
            except:
                # W przypadku błędu JSON, wracamy do logiki Selenium
                main_image_elem = driver.find_element(By.CSS_SELECTOR, "img.js-qv-product-cover")
                product_data["images"] = [self.clean_url(main_image_elem.get_attribute("src"))]

            product_data["images"] = list(set(product_data["images"]))[:2]

            if not product_data["name"]:
                logger.warning("  ⚠️ Produkt odrzucony: Nazwa pusta po parsowaniu JSON.")
                return None

            return product_data

        except Exception as e:
            logger.error(f"  ❌ Błąd krytyczny podczas scrapowania (JSON lub ogólny): {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            driver.quit()

    def download_image(self, url, product_name, index, referer_url):
        """Pobiera zdjęcie z wykorzystaniem Referer Header (URL strony detali)."""

        # --- FIX: AGRESYWNE NAGŁÓWKI DO POBIERANIA OBRAZÓW ---
        HEADERS_IMG = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            # NAJWAŻNIEJSZE: Używamy URL strony detali jako referera
            'Referer': referer_url
        }

        try:
            # Używamy ulepszonych nagłówków
            response = requests.get(url, headers=HEADERS_IMG, timeout=10)

            if response.status_code != 200:
                logger.warning(f"    ⚠️ BŁĄD HTTP ({response.status_code}): Serwer odrzucił żądanie dla {url[:60]}")
                return None

            # Zmiana limitu wymiarów na 300px
            img = Image.open(BytesIO(response.content))
            width, height = img.size

            if min(width, height) < 300:  # Ostateczne minimum
                logger.warning(f"    ⚠️  Zdjęcie za małe: {width}x{height}px (wymagane >300px)")
                return None

            # --- ZAPIS PLIKU ---
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_'))
            safe_name = safe_name.strip().replace(' ', '_')[:50]
            img_hash = hashlib.md5(url.encode()).hexdigest()[:8]

            extension = url.split('.')[-1].split('?')[0][:4]
            if extension not in ['jpg', 'jpeg', 'png', 'webp']:
                extension = 'jpg'

            filename = f"{safe_name}_{index}_{img_hash}.{extension}"
            filepath = os.path.join(self.images_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            logger.info(f"    📷 {filename} ({width}x{height}px) - Zapisano.")
            return filename

        except Exception as e:
            logger.error(f"    ❌ Błąd krytyczny podczas zapisywania/pobierania: {e}")
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
                        logger.info(f"  ✓ {product_data['name']} - {product_data.get('price', 'N/A')} PLN")
                except Exception as e:
                    logger.error(f"  ❌ {e}")

        return results

    def download_images_batch(self, products):
        """Pobiera zdjęcia, przekazując URL strony detali jako Referer."""
        total_images = sum(len(p['images']) for p in products)
        logger.info(f"📷 Pobieranie {total_images} zdjęć...")

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
                # Odpakowujemy argumenty
                url, name, idx, referer_url_arg = future_to_task[future]

                # Odszukujemy obiekt produktu po jego URL (referer_url_arg)
                product = next((p for p in products if p['url'] == referer_url_arg), None)

                if not product: continue

                try:
                    filename = future.result()
                    if filename:
                        if 'local_images' not in product:
                            product['local_images'] = []
                        product['local_images'].append(filename)
                except Exception:
                    pass

    def export_to_prestashop_csv(self):
        """Eksportuje do CSV w formacie PrestaShop."""
        logger.info("\n💾 Eksportowanie...")

        # Kategorie
        # Mapowanie ID na Nazwę dla łatwego znalezienia nazwy rodzica
        id_to_name = {cat['id']: cat['name'] for cat in self.categories}
        id_to_name[0] = 'ROOT'  # Domyślna nazwa dla braku rodzica

        # Kategorie
        categories_file = os.path.join(self.output_dir, "categories.csv")
        with open(categories_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # UPROSZCZONY NAGŁÓWEK:
            writer.writerow(['ID', 'Active', 'Name', 'Parent ID', 'Parent Name'])

            for cat in self.categories:
                parent_name = id_to_name.get(cat['parent_id'], 'Nieznany')

                # Zapisujemy tylko 5 wymaganych pól
                writer.writerow([
                    cat['id'],
                    cat['active'],
                    cat['name'],
                    cat['parent_id'],
                    parent_name
                ])

        logger.info(f"  ✓ Zapisano uproszczoną strukturę kategorii: {categories_file}")

        # Produkty
        products_file = os.path.join(self.output_dir, "products.csv")
        with open(products_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')

            # ZMIANA 1: DODANIE 'Usage' do nagłówka
            writer.writerow([
                'ID', 'Name', 'Categories', 'Price',
                'Reference', 'Description', 'Usage', 'Image URLs', 'Feature'  # Dodano 'Sposób Użycia'
            ])

            for idx, product in enumerate(self.products, 1):
                attributes_text = "; ".join(
                    [f"{k}:{v}:0" for k, v in product['attributes'].items()])

                image_urls = ";".join([f"images/{img}" for img in product.get('local_images', [])])

                writer.writerow([
                    idx,
                    product['name'],
                    product['category'],
                    product['price'],
                    product['reference'],
                    product['description'],
                    product.get('usage', ''),  # ZMIANA 2: Dodanie wartości z nowego pola 'usage'
                    image_urls,
                    attributes_text
                ])

        logger.info(f"  ✓ {products_file}")

        # JSON
        json_file = os.path.join(self.output_dir, "all_data.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'categories': self.categories,
                'products': self.products
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"  ✓ {json_file}\n")

    def run(self, categories_limit=None, products_per_category=None, batch_size=10):
        """Uruchamia scraping"""
        start_time = time.time()

        logger.info("=" * 60)
        logger.info("🚀 SCRAPER KFD - START")
        logger.info("=" * 60)

        try:
            # 1. Kategorie
            self.scrape_all_categories_from_menu()

            if not self.categories:
                logger.error("❌ Brak kategorii - kończę")
                return

            categories_to_process = self.categories[:categories_limit] if categories_limit else self.categories

            # 2. Produkty
            all_product_urls = []
            for category in categories_to_process:
                urls = self.get_product_urls_from_category(
                    category['url'],
                    category['name'],
                    limit=products_per_category
                )
                all_product_urls.extend(urls)
                time.sleep(1)

            if not all_product_urls:
                logger.error("❌ Brak produktów - kończę")
                return

            logger.info(f"\n📊 {len(all_product_urls)} produktów do przetworzenia")
            logger.info(f"⚙️  Batch po {batch_size}\n")

            # 3. Batch processing
            for i in range(0, len(all_product_urls), batch_size):
                batch = all_product_urls[i:i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (len(all_product_urls) + batch_size - 1) // batch_size

                logger.info(f"📦 Batch {batch_num}/{total_batches}")

                products_data = self.process_product_batch(batch)

                if products_data:
                    self.download_images_batch(products_data)

                    with self.lock:
                        self.products.extend(products_data)

                logger.info(f"  ✓ Łącznie: {len(self.products)} produktów\n")

            # 4. Export
            self.export_to_prestashop_csv()

            elapsed = time.time() - start_time
            logger.info("=" * 60)
            logger.info(f"✅ ZAKOŃCZONO w {elapsed / 60:.1f} min")
            logger.info(f"📊 Kategorie: {len(self.categories)}")
            logger.info(f"📦 Produkty: {len(self.products)}")
            logger.info(f"📷 Zdjęcia: {sum(len(p.get('local_images', [])) for p in self.products)}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\n❌ BŁĄD: {e}")
            import traceback
            traceback.print_exc()

    def scrape_single_subcategory_test(self, category_url):
        """Tymczasowa funkcja omijająca pobieranie kategorii, aby od razu skanować produkty."""

        # Tworzymy fałszywą kategorię dla potrzeb testu i eksportu CSV
        test_category_name = "Białko Serwatkowe"

        test_category = {
            "id": 999,
            "name": test_category_name,
            "url": category_url,
            "parent_id": 1,
            "active": 1
        }

        self.categories = [test_category]  # Resetujemy, dodając tylko jedną kategorię

        # 2. Pobieramy tylko JEDEN produkt
        all_product_urls = self.get_product_urls_from_category(
            category_url,
            test_category_name,
            limit=1  # ZMIANA: Pobieramy tylko 1 URL
        )

        if not all_product_urls:
            logger.error("❌ Brak produktów do przetworzenia.")
            return

        logger.info(f"\n📊 {len(all_product_urls)} produktów do przetworzenia z podkategorii.")

        # 3. Przetwarzamy sekwencyjnie
        batch_size = 1  # ZMIANA: Używamy batcha o rozmiarze 1
        self.max_workers = 1  # ZMIANA: Używamy 1 workera, aby widzieć sekwencyjne logi

        for i in range(0, len(all_product_urls), batch_size):
            batch = all_product_urls[i:i + batch_size]
            logger.info(f"📦 Przetwarzanie Batch {i // batch_size + 1}")

            products_data = self.process_product_batch(batch)

            if products_data:
                self.download_images_batch(products_data)

                with self.lock:
                    self.products.extend(products_data)

            logger.info(f"  ✓ Łącznie: {len(self.products)} produktów przetworzonych.")

        # 4. Eksport
        self.export_to_prestashop_csv()


if __name__ == "__main__":
    # --- PARAMETRY DOCELOWE ---
    TARGET_URL = "https://sklep.kfd.pl/bialko-serwatkowe-c-64.html"
    CATEGORY_NAME = "Białko Serwatkowe"

    scraper = KFDScraper(
        max_workers=5  # Użyjemy 5 wątków do szybkiego testu wydajności
    )

    # 1. RĘCZNE USTAWIENIE KATEGORII STARTOWEJ
    # Omijamy problematyczne pobieranie hierarchii, podając tylko URL docelowy
    scraper.categories = [{
        "id": 1,
        "name": CATEGORY_NAME,
        "url": TARGET_URL,
        "parent_id": 0,
        "active": 1
    }]

    logger.info("--- START PEŁNEGO SKANOWANIA Z PAGINACJĄ ---")

    # 2. Uruchamiamy główną funkcję run()
    scraper.run(
        categories_limit=1,  # Przetwarzamy tylko tę jedną, ręcznie dodaną kategorię
        products_per_category=None,  # !!! BRAK LIMITU produktów (pobieramy WSZYSTKIE) !!!
        batch_size=5
    )

    logger.info("--- TEST ZAKOŃCZONY. Sprawdź pliki CSV i folder images ---")