# Scraper i Import Produktów KFD do Prestashop

System do automatycznego pobierania produktów ze sklepu KFD.pl i importu do Prestashop.

## Struktura projektu

```
scraper/
├── scraper.py              # Główny scraper KFD.pl
├── upload_categories.py    # Import kategorii do Prestashop
├── upload_products.py      # Import produktów do Prestashop
├── requirements.txt        # Zależności Python
├── data_kfd/              # Folder z pobranymi danymi
│   ├── all_data.json      # Wszystkie produkty i kategorie
│   ├── categories.csv     # Eksport kategorii
│   ├── products.csv       # Eksport produktów
│   ├── producenci.csv     # Lista producentów
│   ├── category_mapping.json  # Mapowanie ID kategorii
│   ├── images/            # Pobrane zdjęcia produktów
│   └── images_converted_png/  # Zdjęcia w formacie PNG
└── imported_products_ids.json # Log zaimportowanych produktów
```

## Wymagania

- Python 3.8+
- Chrome/Chromium + ChromeDriver
- Prestashop 1.7.8+ z włączonym API

### Instalacja zależności

```bash
pip install -r requirements.txt
```

## Konfiguracja

### 1. Prestashop API

Edytuj zmienne w `upload_categories.py` i `upload_products.py`:

```python
API_URL = "https://localhost:8443/api/"
API_KEY = "TWOJ_KLUCZ_API"
```


## Użycie

### Krok 1: Scraping produktów z KFD

```bash
python scraper.py
```

**Parametry do edycji w kodzie:**
- `max_workers`: liczba wątków (domyślnie 8)
- `products_per_category`: limit produktów na kategorię (domyślnie 8)
- `batch_size`: rozmiar batcha (domyślnie 8)

**Wynik:**
- `data_kfd/all_data.json` - pełne dane JSON
- `data_kfd/categories.csv` - kategorie
- `data_kfd/products.csv` - produkty
- `data_kfd/producenci.csv` - producenci
- `data_kfd/images/` - pobrane zdjęcia

### Krok 2: Import kategorii do Prestashop

```bash
python upload_categories.py
```

**Co robi:**
- Tworzy hierarchię kategorii z JSON
- Tworzy kategorię główną "KATEGORIE"
- Tworzy kategorię "PRODUCENCI" z podkategoriami dla każdej marki
- Zapisuje mapowanie ID do `data_kfd/category_mapping.json`

### Krok 3: Import produktów do Prestashop

```bash
python upload_products.py
```

**Co robi:**
- Importuje produkty z `all_data.json`
- Przypisuje do kategorii (główna + nadrzędna + producent)
- Uploaduje zdjęcia (PNG > JPG)
- Ustawia `state=1` w bazie (widoczność w panelu admin)
- Tworzy producentów jeśli nie istnieją

**Tryb testowy:**
Domyślnie wyłączony. Aby włączyć import tylko 5 produktów, odkomentuj w kodzie:
```python
products_to_import = products_to_import[:5]
```

## Funkcje specjalne

### Fix stanu produktów (state=1)

Produkty importowane przez API wymagają ustawienia `state=1` w bazie danych, aby były widoczne w panelu admin:

```python
def fix_product_state(product_id):
    """Ustawia state=1 w bazie danych"""
```

Jest automatycznie wywoływana po utworzeniu produktu.

### Cache producentów

Zapobiega duplikowaniu producentów:
```python
MANUFACTURER_CACHE = {}  # {nazwa: ID}
```

### Priorytet zdjęć

Kolejność prób uploadowania zdjęcia:
1. `images_converted_png/*.png` (priorytet)
2. `images/original` (oryginalne)
3. `images/*.jpg`
4. `images/*.png`



## Limity i optymalizacja

- **Scraper:** 8 workerów równolegle
- **Batch processing:** Po 8 produktów
- **Timeout:** 60s na stronę
- **Retry:** Automatyczne dla błędów HTTP
- **Rate limiting:** 1s sleep między kategoriami

