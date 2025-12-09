import requests
import urllib3
import json
import xml.etree.ElementTree as ET

# Wyłączenie ostrzeżeń o niezaufanym certyfikacie
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 1. KONFIGURACJA API I DANYCH
# ==============================================================================

API_URL = "https://localhost:8443/api/"
API_KEY = "9I74XHFJJJA87Y9EB15N3HGIMMU8FDPE"
JSON_FILE_PATH = "data_kfd/all_data.json"

# Kodowanie klucza API w Base64 dla Basic Auth (format: klucz:)
import base64
auth_string = f"{API_KEY}:"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/xml"
}

# Słownik do przechowywania mapowania: { ID z JSON: ID w Prestashop }
category_id_map = {}

# Wczytanie danych z JSON
try:
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    categories = data.get('categories', [])
    print(f"✅ Wczytano {len(categories)} kategorii z pliku JSON.")
    
except FileNotFoundError:
    print(f"BŁĄD: Nie znaleziono pliku {JSON_FILE_PATH}.")
    exit(1)
except Exception as e:
    print(f"BŁĄD podczas wczytywania/parsowania JSON: {e}")
    exit(1)


# ==============================================================================
# 2. FUNKCJE POMOCNICZE
# ==============================================================================

def get_category_by_name_and_parent(category_name, parent_id):
    """Sprawdza, czy kategoria o danej nazwie i rodzicu już istnieje."""
    url_get = f"{API_URL}categories?filter[name]=[{category_name}]&display=full"
    response = requests.get(url_get, headers=headers, verify=False)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        
        for category_node in root.findall(".//category"):
            cat_id_node = category_node.find("id")
            parent_node = category_node.find("id_parent")
            
            if cat_id_node is not None and parent_node is not None:
                if parent_node.text == str(parent_id):
                    return cat_id_node.text
    
    return None


def create_category(category_name, parent_id, description=""):
    """Tworzy nową kategorię w Prestashop."""
    link_rewrite = category_name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('ł', 'l').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z')[:128]
    
    category_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
    <category>
        <id_parent>{parent_id}</id_parent>
        <active>1</active>
        <name>
            <language id="1"><![CDATA[{category_name}]]></language>
        </name>
        <link_rewrite>
            <language id="1"><![CDATA[{link_rewrite}]]></language>
        </link_rewrite>
        <description>
            <language id="1"><![CDATA[{description}]]></language>
        </description>
    </category>
</prestashop>
"""
    
    response_post = requests.post(
        f"{API_URL}categories", 
        headers=headers, 
        data=category_xml.encode('utf-8'),
        verify=False
    )
    
    if response_post.status_code == 201:
        root = ET.fromstring(response_post.text)
        new_id = root.find(".//category/id").text
        print(f"  ✓ UTWORZONO '{category_name}' (ID: {new_id}, Parent: {parent_id})")
        return new_id
    else:
        print(f"  ❌ Błąd podczas tworzenia '{category_name}' (Status: {response_post.status_code})")
        print(f"     Odpowiedź: {response_post.text[:500]}")
        return None


def get_or_create_category(category_name, parent_id, description=""):
    """Pobiera ID kategorii lub tworzy ją, jeśli nie istnieje."""
    existing_id = get_category_by_name_and_parent(category_name, parent_id)
    
    if existing_id:
        print(f"  ✓ Kategoria '{category_name}' już istnieje (ID: {existing_id})")
        return existing_id
    
    return create_category(category_name, parent_id, description)


# ==============================================================================
# 3. BUDOWANIE HIERARCHII KATEGORII
# ==============================================================================

def build_category_tree(categories):
    """Buduje drzewo kategorii z parent_id."""
    tree = {}
    for cat in categories:
        parent_id = cat.get('parent_id', 0)
        if parent_id not in tree:
            tree[parent_id] = []
        tree[parent_id].append(cat)
    return tree


def process_category_recursively(category, prestashop_parent_id, category_tree):
    """Przetwarza kategorię i jej dzieci rekurencyjnie."""
    category_name = category['name']
    json_id = category['id']
    
    print(f"\n-> Przetwarzanie: {category_name} (JSON ID: {json_id})")
    
    # Tworzenie/pobieranie kategorii w Prestashop
    prestashop_id = get_or_create_category(
        category_name, 
        prestashop_parent_id,
        description=f"Importowane z KFD - {category.get('url', '')}"
    )
    
    if prestashop_id:
        # Zapisanie mapowania
        category_id_map[json_id] = int(prestashop_id)
        
        # Przetwarzanie dzieci (pod-kategorii)
        children = category_tree.get(json_id, [])
        for child in children:
            process_category_recursively(child, int(prestashop_id), category_tree)
    else:
        print(f"  ❌ Nie udało się przetworzyć '{category_name}'")


# ==============================================================================
# 4. GŁÓWNA LOGIKA IMPORTU
# ==============================================================================

print("\n" + "="*70)
print("START: Importowanie hierarchicznych kategorii z KFD")
print("="*70)

# Mapowanie głównych kategorii Prestashop
PRESTASHOP_ROOT_ID = 2  # "Home" w Prestashop

# Budowanie drzewa kategorii
category_tree = build_category_tree(categories)

# Znajdowanie kategorii głównych - wszystkie z parent_id = 1 (bo ID=1 to root w KFD)
root_categories = category_tree.get(1, [])

print(f"\nZnaleziono {len(root_categories)} kategorii głównych (parent_id=1):")
for cat in root_categories:
    print(f"  - {cat['name']} (ID: {cat['id']})")

# Krok 1: Znalezienie i utworzenie głównej kategorii "KATEGORIE"
kategorie_category = None
other_root_categories = []

for cat in root_categories:
    if cat['name'] == 'KATEGORIE':
        kategorie_category = cat
    else:
        other_root_categories.append(cat)

# Krok 2: Najpierw przetwarzamy kategorię "KATEGORIE" pod "Home"
if kategorie_category:
    print(f"\n-> Tworzenie głównej kategorii KATEGORIE...")
    process_category_recursively(kategorie_category, PRESTASHOP_ROOT_ID, category_tree)
    kategorie_prestashop_id = category_id_map.get(kategorie_category['id'])
    
    if kategorie_prestashop_id:
        # Krok 3: Wszystkie inne kategorie główne umieszczamy pod "KATEGORIE"
        print(f"\n-> Przetwarzanie pozostałych kategorii pod KATEGORIE (ID: {kategorie_prestashop_id})...")
        for root_category in other_root_categories:
            process_category_recursively(root_category, kategorie_prestashop_id, category_tree)
    else:
        print("❌ Nie udało się utworzyć kategorii KATEGORIE")
else:
    # Jeśli nie ma kategorii "KATEGORIE", przetwarzamy wszystko normalnie
    print("\n⚠️ Brak kategorii 'KATEGORIE', przetwarzanie standardowe...")
    for root_category in root_categories:
        process_category_recursively(root_category, PRESTASHOP_ROOT_ID, category_tree)

# Krok 4: Tworzenie kategorii "PRODUCENCI" z podkategoriami dla każdego producenta
print(f"\n-> Tworzenie kategorii PRODUCENCI...")

# Pobierz wszystkich producentów z all_data.json
try:
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        products = data.get('products', [])
    
    # Zbierz unikalne nazwy producentów
    manufacturers = set()
    for product in products:
        brand = product.get('brand', '').strip()
        if brand:
            manufacturers.add(brand)
    
    manufacturers = sorted(list(manufacturers))
    print(f"  Znaleziono {len(manufacturers)} unikalnych producentów")
    
    # Utwórz główną kategorię "PRODUCENCI" pod "Home"
    producenci_id = get_or_create_category(
        "PRODUCENCI",
        PRESTASHOP_ROOT_ID,
        description="Produkty według producentów"
    )
    
    if producenci_id:
        print(f"  ✓ Kategoria PRODUCENCI utworzona (ID: {producenci_id})")
        
        # Utwórz podkategorię dla każdego producenta
        print(f"\n-> Tworzenie {len(manufacturers)} kategorii producentów...")
        for manufacturer_name in manufacturers:
            manufacturer_category_id = get_or_create_category(
                manufacturer_name,
                int(producenci_id),
                description=f"Produkty marki {manufacturer_name}"
            )
            if manufacturer_category_id:
                # Zapisz mapowanie dla późniejszego użycia
                category_id_map[f"manufacturer_{manufacturer_name}"] = int(manufacturer_category_id)
    else:
        print("  ❌ Nie udało się utworzyć kategorii PRODUCENCI")
        
except Exception as e:
    print(f"  ❌ Błąd podczas tworzenia kategorii producentów: {e}")

# ==============================================================================
# 5. ZAPIS MAPOWANIA DO PLIKU
# ==============================================================================

mapping_file = "data_kfd/category_mapping.json"
try:
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(category_id_map, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Mapowanie kategorii zapisano do: {mapping_file}")
except Exception as e:
    print(f"\n❌ Błąd podczas zapisywania mapowania: {e}")

print("\n" + "="*70)
print("ZAKOŃCZONO IMPORT KATEGORII")
print(f"Przetworzone kategorie: {len(category_id_map)}")
print("="*70)
