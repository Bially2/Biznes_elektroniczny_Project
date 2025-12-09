import os
import json
import requests
import urllib3
import xml.etree.ElementTree as ET
import base64
import mysql.connector

# Wyłączenie ostrzeżeń o niezaufanym certyfikacie
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 1. KONFIGURACJA I GLOBALNY BUFOR KATEGORII
# ==============================================================================

API_URL = "https://localhost:8443/api/"
API_KEY = "9I74XHFJJJA87Y9EB15N3HGIMMU8FDPE"
JSON_FILE_PATH = "data_kfd/all_data.json"
CATEGORY_MAPPING_FILE = "data_kfd/category_mapping.json"
OUTPUT_FILE_PATH = "imported_products_ids.json"

# USTAWIENIA PRESTASHOP
DEFAULT_CATEGORY_ID = 2
DEFAULT_TAX_RULES_GROUP_ID = 0
IMAGE_DIR = "data_kfd/images"
IMAGE_DIR_PNG = "data_kfd/images_converted_png"  # Folder z PNG

# Kodowanie klucza API w Base64 dla Basic Auth (format: klucz:)
auth_string = f"{API_KEY}:"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/xml"
}

# GLOBALNY BUFOR KATEGORII: { JSON_ID: Prestashop_ID }
CATEGORY_ID_MAP = {}

# KONFIGURACJA BAZY DANYCH
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'prestashop'
}


# ==============================================================================
# FUNKCJE POMOCNICZE
# ==============================================================================

def fix_product_state(product_id):
    """Ustawia state=1 w bazie danych dla produktu (wymagane aby był widoczny w panelu admin)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE ps_product SET state = 1 WHERE id_product = %s",
            (product_id,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Stan produktu zaktualizowany (state=1)")
        return True
        
    except Exception as e:
        print(f"Błąd aktualizacji stanu: {e}")
        return False

def load_category_mapping():
    """Wczytuje mapowanie kategorii z pliku JSON."""
    global CATEGORY_ID_MAP
    
    try:
        with open(CATEGORY_MAPPING_FILE, 'r', encoding='utf-8') as f:
            CATEGORY_ID_MAP = json.load(f)
        
        # Konwersja kluczy numerycznych na int, pozostawienie tekstowych bez zmian
        converted_map = {}
        for k, v in CATEGORY_ID_MAP.items():
            try:
                # Próba konwersji na int (dla ID kategorii)
                converted_map[int(k)] = int(v)
            except ValueError:
                # Pozostawienie jako string (dla manufacturer_* kluczy)
                converted_map[k] = int(v)
        
        CATEGORY_ID_MAP = converted_map
        
        print(f"Wczytano mapowanie {len(CATEGORY_ID_MAP)} kategorii z pliku.")
        return True
        
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {CATEGORY_MAPPING_FILE}")
        print("   Najpierw uruchom: python upload_categories.py")
        return False
    except Exception as e:
        print(f"Błąd podczas wczytywania mapowania kategorii: {e}")
        return False


# Cache dla producentów: {nazwa: ID}
MANUFACTURER_CACHE = {}


def get_or_create_manufacturer_id(manufacturer_name):
    """Pobiera lub tworzy producenta."""
    if not manufacturer_name or manufacturer_name.strip() == "":
        return None

    manufacturer_name = manufacturer_name.strip()
    
    # Sprawdzenie w lokalnym cache
    if manufacturer_name in MANUFACTURER_CACHE:
        print(f"Producent '{manufacturer_name}' z cache (ID: {MANUFACTURER_CACHE[manufacturer_name]})")
        return MANUFACTURER_CACHE[manufacturer_name]

    # Pobierz WSZYSTKICH producentów i sprawdź dokładnie
    url_get = f"{API_URL}manufacturers?display=full"
    response = requests.get(url_get, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            
            # Sprawdź każdego producenta
            for manufacturer in root.findall(".//manufacturer"):
                name_node = manufacturer.find(".//name")
                id_node = manufacturer.find("id")
                
                if name_node is not None and id_node is not None:
                    existing_name = name_node.text.strip()
                    existing_id = id_node.text
                    
                    # Porównanie bez względu na wielkość liter
                    if existing_name.lower() == manufacturer_name.lower():
                        print(f"Producent '{manufacturer_name}' już istnieje (ID: {existing_id})")
                        MANUFACTURER_CACHE[manufacturer_name] = existing_id
                        return existing_id
        except Exception as e:
            print(f"Błąd podczas wyszukiwania producenta: {e}")

    # Tworzenie nowego producenta
    link_rewrite = sanitize_link_rewrite(manufacturer_name)

    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
    <manufacturer>
        <name><![CDATA[{manufacturer_name}]]></name>
        <active>1</active>
    </manufacturer>
</prestashop>"""

    response_post = requests.post(
        f"{API_URL}manufacturers",
        headers=headers,
        data=xml_data.encode('utf-8'),
        verify=False
    )

    if response_post.status_code == 201:
        root = ET.fromstring(response_post.text)
        new_id = root.find("./manufacturer/id").text
        print(f"Utworzono producenta '{manufacturer_name}' (ID: {new_id})")
        MANUFACTURER_CACHE[manufacturer_name] = new_id
        return new_id
    else:
        print(f"Błąd tworzenia producenta: {response_post.status_code}")
        print(f"     Odpowiedź: {response_post.text[:300]}")
        return None
def get_category_ids_for_product(product_data):
    """Pobiera ID kategorii dla produktu na podstawie mapowania."""
    category_string = product_data.get('category', '').strip()
    brand_name = product_data.get('brand', '').strip()
    
    all_category_ids = set()
    default_category_id = str(DEFAULT_CATEGORY_ID)
    
    # === CZĘŚĆ 1: Kategorie produktowe ===
    if category_string:
        # Rozdzielenie ścieżki kategorii na segmenty
        category_names = [name.strip() for name in category_string.split(',') if name.strip()]
        
        if category_names:
            try:
                with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    categories = data.get('categories', [])
                
                # Szukamy ostatniej kategorii (najgłębsza) i jej rodzica
                target_category_name = category_names[-1]
                parent_category_name = category_names[-2] if len(category_names) > 1 else None
                
                # Znajdujemy JSON ID kategorii
                category_json_id = None
                parent_json_id = None
                
                for cat in categories:
                    if cat.get('name') == target_category_name:
                        category_json_id = cat.get('id')
                        parent_json_id = cat.get('parent_id')
                        break
                
                # Dodaj główną kategorię produktu
                if category_json_id and category_json_id in CATEGORY_ID_MAP:
                    prestashop_cat_id = CATEGORY_ID_MAP[category_json_id]
                    all_category_ids.add(str(prestashop_cat_id))
                    default_category_id = str(prestashop_cat_id)
                    
                    # Dodaj kategorię nadrzędną (rodzica)
                    if parent_json_id and parent_json_id in CATEGORY_ID_MAP:
                        parent_prestashop_id = CATEGORY_ID_MAP[parent_json_id]
                        all_category_ids.add(str(parent_prestashop_id))
                    
                    print(f"Kategoria produktu: {' > '.join(category_names)}")
                else:
                    print(f"Nie znaleziono kategorii '{target_category_name}' w mapowaniu")
                    
            except Exception as e:
                print(f"Błąd podczas wyszukiwania kategorii: {e}")
    
    # === CZĘŚĆ 2: Kategoria producenta ===
    if brand_name:
        manufacturer_key = f"manufacturer_{brand_name}"
        if manufacturer_key in CATEGORY_ID_MAP:
            manufacturer_cat_id = CATEGORY_ID_MAP[manufacturer_key]
            all_category_ids.add(str(manufacturer_cat_id))
            print(f"Kategoria producenta: {brand_name}")
        else:
            print(f"Nie znaleziono kategorii producenta '{brand_name}'")
    
    # Jeśli nie znaleziono żadnych kategorii, użyj domyślnej
    if not all_category_ids:
        all_category_ids.add(str(DEFAULT_CATEGORY_ID))
        print(f"Używam domyślnej kategorii")
    
    return list(all_category_ids), default_category_id


def sanitize_link_rewrite(text):
    """Czyści tekst dla link_rewrite."""
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'a', 'Ć': 'c', 'Ę': 'e', 'Ł': 'l', 'Ń': 'n',
        'Ó': 'o', 'Ś': 's', 'Ź': 'z', 'Ż': 'z'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')[:128]


# ==============================================================================
# GŁÓWNA PĘTLA IMPORTU
# ==============================================================================

def run_import():
    print("\n" + "="*70)
    print("START: Import produktów do Prestashop")
    print("="*70)
    
    # Krok 1: Wczytanie mapowania kategorii
    if not load_category_mapping():
        return

    # Krok 2: Wczytanie danych produktów
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products_to_import = data.get('products', [])

            # OGRANICZENIE DO PIERWSZYCH 5 PRODUKTÓW (do testów) - WYŁĄCZONE
            # if products_to_import:
            #     products_to_import = products_to_import[:5]
            #     print(f"\nTRYB TESTOWY: Importowanie tylko {len(products_to_import)} produktów")
            
            print(f"\nImportowanie WSZYSTKICH {len(products_to_import)} produktów")

    except Exception as e:
        print(f"BŁĄD: Nie można wczytać danych JSON: {e}")
        return

    imported_products_data = []

    # Krok 3: Pętla importu produktów
    for i, product_data in enumerate(products_to_import, 1):
        print(f"\n{'='*70}")
        print(f"PRODUKT {i}/{len(products_to_import)}: {product_data.get('name', 'Bez nazwy')}")
        print(f"{'='*70}")

        # Przygotowanie danych produktu
        safe_name = product_data.get('name', 'Produkt').strip()
        safe_description = product_data.get('description', '').strip() or safe_name
        safe_description_short = product_data.get('description_short', '')[:400].strip() or safe_name
        safe_link_rewrite = sanitize_link_rewrite(safe_name)
        safe_weight = str(product_data.get('weight', '0.00')).replace(',', '.')
        safe_price = str(product_data.get('price', '0.00')).replace(',', '.')
        safe_reference = product_data.get('reference', '')[:64]

        # Producent
        brand_name = product_data.get('brand', safe_name.split(' ')[0])
        manufacturer_id = get_or_create_manufacturer_id(brand_name)

        # Kategorie
        category_ids, default_category_id = get_category_ids_for_product(product_data)
        category_associations_xml = "".join([f"<category><id>{cat_id}</id></category>" for cat_id in category_ids])

        print(f"  → Nazwa: {safe_name}")
        print(f"  → Cena: {safe_price}")
        print(f"  → Producent ID: {manufacturer_id}")
        print(f"  → Kategoria domyślna ID: {default_category_id}")

        # Budowanie XML produktu
        product_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
    <product>
        <name>
            <language id="1"><![CDATA[{safe_name}]]></language>
        </name>
        <price>{safe_price}</price>
        <id_tax_rules_group>{DEFAULT_TAX_RULES_GROUP_ID}</id_tax_rules_group>
        <id_manufacturer>{manufacturer_id if manufacturer_id else '0'}</id_manufacturer>
        <id_supplier>0</id_supplier>
        <weight>{safe_weight}</weight>
        <active>1</active>
        <available_for_order>1</available_for_order>
        <id_category_default>{default_category_id}</id_category_default>
        <show_price>1</show_price>
        <reference><![CDATA[{safe_reference}]]></reference>
        <description>
            <language id="1"><![CDATA[{safe_description}]]></language>
        </description>
        <description_short>
            <language id="1"><![CDATA[{safe_description_short}]]></language>
        </description_short>
        <link_rewrite>
            <language id="1"><![CDATA[{safe_link_rewrite}]]></language>
        </link_rewrite>
        <associations>
            <categories>{category_associations_xml}</categories>
        </associations>
    </product>
</prestashop>
"""

        # Wysyłka produktu
        product_id = None
        response = requests.post(
            f"{API_URL}products", 
            headers=headers, 
            data=product_xml.encode('utf-8'), 
            verify=False
        )

        if response.status_code == 201:
            try:
                root = ET.fromstring(response.text)
                product_id = root.find("./product/id").text
                print(f"Produkt dodany pomyślnie (ID: {product_id})")
                
                # Napraw stan produktu w bazie (state=1 aby był widoczny w panelu admin)
                fix_product_state(product_id)
                
            except Exception as e:
                print(f"Błąd parsowania odpowiedzi produktu: {e}")
                continue
        else:
            print(f"Błąd dodawania produktu (Status: {response.status_code})")
            print(f"     Odpowiedź: {response.text[:300]}")
            continue

        # Dodawanie zdjęcia
        image_id = None
        local_images = product_data.get('local_images', [])

        if local_images and len(local_images) > 0:
            # Użyj drugiego zdjęcia (większe) jeśli jest dostępne, w przeciwnym razie pierwsze
            image_index = 1 if len(local_images) > 1 else 0
            image_filename = local_images[image_index].get('filename', '')

            # Próba ze zdjęciem PNG z folderu images_converted_png
            base_name = os.path.splitext(image_filename)[0]
            
            # Kolejność prób: PNG z converted, oryginalne, JPG
            image_paths_to_try = [
                os.path.join(IMAGE_DIR_PNG, f"{base_name}.png"),  # PRIORYTET: PNG z converted
                os.path.join(IMAGE_DIR, image_filename),           # Oryginalne
                os.path.join(IMAGE_DIR, f"{base_name}.jpg"),       # JPG jeśli istnieje
                os.path.join(IMAGE_DIR, f"{base_name}.png")        # PNG w images
            ]

            # Znajdź pierwsze istniejące zdjęcie
            image_path = None
            for path in image_paths_to_try:
                if os.path.exists(path):
                    image_path = path
                    break

            if image_path:
                try:
                    # Określenie MIME type - akceptujemy tylko JPG, PNG, GIF
                    ext = os.path.splitext(image_path)[1].lower()
                    mime_types = {
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.png': 'image/png',
                        '.gif': 'image/gif'
                    }
                    mime_type = mime_types.get(ext)

                    if not mime_type:
                        print(f"Nieobsługiwany format zdjęcia: {ext}")
                    else:
                        print(f"  → Wysyłanie zdjęcia: {os.path.basename(image_path)} ({mime_type})")
                        
                        with open(image_path, "rb") as image_file:
                            image_response = requests.post(
                                f"{API_URL}images/products/{product_id}",
                                headers={"Authorization": f"Basic {encoded_auth}"},
                                files={
                                    "image": (os.path.basename(image_path), image_file, mime_type)
                                },
                                verify=False
                            )

                        if image_response.status_code in [200, 201]:
                            root_img = ET.fromstring(image_response.text)
                            image_id = root_img.find(".//image/id").text
                            print(f"Zdjęcie dodane pomyślnie (Image ID: {image_id})")
                        else:
                            print(f"Błąd dodawania zdjęcia (Status: {image_response.status_code})")
                            print(f"     Odpowiedź: {image_response.text[:300]}")

                except Exception as e:
                    print(f"Błąd podczas przetwarzania zdjęcia: {e}")
            else:
                print(f"Nie znaleziono pliku zdjęcia: {image_filename}")
                print(f"     Sprawdzono lokalizacje: images_converted_png, images")        # Zapisywanie danych do finalizacji
        imported_products_data.append({
            'product_id': product_id,
            'image_id': image_id,
            'manufacturer_id': manufacturer_id,
            'name': safe_name
        })

    # Zapis finalny
    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(imported_products_data, f, indent=4, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"IMPORT ZAKOŃCZONY")
    print(f"Zaimportowano: {len(imported_products_data)} produktów")
    print(f"Dane zapisano w: {OUTPUT_FILE_PATH}")
    print(f"{'='*70}")


if __name__ == "__main__":
    run_import()
