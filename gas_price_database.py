import re


GAS_PRICE_DATABASE = {
    ("phoenix, az", "costco"): 3.69,
    ("phoenix, az", "sam's club"): 3.71,
    ("phoenix, az", "qt"): 3.79,
    ("phoenix, az", "circle k"): 3.85,
    ("phoenix, az", "arco"): 3.83,
    ("phoenix, az", "valero"): 3.88,
    ("phoenix, az", "76"): 3.92,
    ("phoenix, az", "mobil"): 3.95,
    ("phoenix, az", "exxon"): 3.97,
    ("phoenix, az", "shell"): 3.99,
    ("phoenix, az", "chevron"): 4.09,
    ("phoenix, az", "texaco"): 4.05,
    ("phoenix, az", "bp"): 4.01,
    ("phoenix, az", "sinclair"): 3.90,
    ("phoenix, az", "fry's fuel"): 3.76,
    ("phoenix, az", "speedway"): 3.87,
    ("phoenix, az", "7-eleven"): 3.86,
    ("phoenix, az", "love's"): 3.93,
    ("phoenix, az", "travelcenters of america"): 3.97,
    ("phoenix, az", None): 3.89,
    ("tucson, az", "costco"): 3.59,
    ("tucson, az", "sam's club"): 3.63,
    ("tucson, az", "qt"): 3.70,
    ("tucson, az", "circle k"): 3.74,
    ("tucson, az", "arco"): 3.72,
    ("tucson, az", "valero"): 3.78,
    ("tucson, az", "76"): 3.81,
    ("tucson, az", "mobil"): 3.84,
    ("tucson, az", "shell"): 3.89,
    ("tucson, az", "chevron"): 3.95,
    ("tucson, az", "fry's fuel"): 3.67,
    ("tucson, az", "speedway"): 3.76,
    ("tucson, az", None): 3.76,
    ("flagstaff, az", "costco"): 3.92,
    ("flagstaff, az", "sam's club"): 3.95,
    ("flagstaff, az", "qt"): 3.96,
    ("flagstaff, az", "circle k"): 3.99,
    ("flagstaff, az", "valero"): 4.01,
    ("flagstaff, az", "76"): 4.04,
    ("flagstaff, az", "shell"): 4.09,
    ("flagstaff, az", "chevron"): 4.14,
    ("flagstaff, az", None): 4.03,
    ("mesa, az", "costco"): 3.68,
    ("mesa, az", "sam's club"): 3.70,
    ("mesa, az", "qt"): 3.77,
    ("mesa, az", "circle k"): 3.84,
    ("mesa, az", "shell"): 3.97,
    ("mesa, az", "chevron"): 4.06,
    ("mesa, az", "fry's fuel"): 3.75,
    ("mesa, az", None): 3.86,
    ("tempe, az", "costco"): 3.70,
    ("tempe, az", "qt"): 3.80,
    ("tempe, az", "circle k"): 3.86,
    ("tempe, az", "shell"): 4.00,
    ("tempe, az", "chevron"): 4.08,
    ("tempe, az", None): 3.90,
    ("scottsdale, az", "costco"): 3.74,
    ("scottsdale, az", "qt"): 3.84,
    ("scottsdale, az", "circle k"): 3.91,
    ("scottsdale, az", "shell"): 4.05,
    ("scottsdale, az", "chevron"): 4.14,
    ("scottsdale, az", None): 3.97,
    ("glendale, az", "costco"): 3.67,
    ("glendale, az", "sam's club"): 3.69,
    ("glendale, az", "qt"): 3.76,
    ("glendale, az", "circle k"): 3.83,
    ("glendale, az", "shell"): 3.96,
    ("glendale, az", "chevron"): 4.04,
    ("glendale, az", None): 3.85,
    ("chandler, az", "costco"): 3.69,
    ("chandler, az", "sam's club"): 3.71,
    ("chandler, az", "qt"): 3.78,
    ("chandler, az", "circle k"): 3.85,
    ("chandler, az", "shell"): 3.98,
    ("chandler, az", "chevron"): 4.07,
    ("chandler, az", "fry's fuel"): 3.76,
    ("chandler, az", None): 3.87,
    ("gilbert, az", "costco"): 3.70,
    ("gilbert, az", "sam's club"): 3.72,
    ("gilbert, az", "circle k"): 3.86,
    ("gilbert, az", "shell"): 3.99,
    ("gilbert, az", "chevron"): 4.07,
    ("gilbert, az", "fry's fuel"): 3.77,
    ("gilbert, az", None): 3.88,
    ("peoria, az", "costco"): 3.68,
    ("peoria, az", "qt"): 3.77,
    ("peoria, az", "circle k"): 3.84,
    ("peoria, az", "shell"): 3.97,
    ("peoria, az", "chevron"): 4.05,
    ("peoria, az", None): 3.86,
    ("surprise, az", "costco"): 3.66,
    ("surprise, az", "qt"): 3.75,
    ("surprise, az", "circle k"): 3.82,
    ("surprise, az", "shell"): 3.95,
    ("surprise, az", "chevron"): 4.03,
    ("surprise, az", None): 3.84,
    ("prescott, az", "circle k"): 3.93,
    ("prescott, az", "shell"): 4.02,
    ("prescott, az", "chevron"): 4.10,
    ("prescott, az", "sinclair"): 3.96,
    ("prescott, az", None): 3.98,
    ("sedona, az", "circle k"): 4.08,
    ("sedona, az", "shell"): 4.19,
    ("sedona, az", "chevron"): 4.24,
    ("sedona, az", None): 4.15,
    ("yuma, az", "costco"): 3.57,
    ("yuma, az", "circle k"): 3.66,
    ("yuma, az", "arco"): 3.64,
    ("yuma, az", "shell"): 3.81,
    ("yuma, az", "chevron"): 3.89,
    ("yuma, az", None): 3.72,
    ("kingman, az", "love's"): 3.86,
    ("kingman, az", "travelcenters of america"): 3.91,
    ("kingman, az", "shell"): 3.98,
    ("kingman, az", "chevron"): 4.05,
    ("kingman, az", None): 3.92,
    ("los angeles, ca", "costco"): 4.49,
    ("los angeles, ca", "arco"): 4.59,
    ("los angeles, ca", "76"): 4.71,
    ("los angeles, ca", "shell"): 4.89,
    ("los angeles, ca", "chevron"): 4.99,
    ("los angeles, ca", None): 4.74,
    ("san diego, ca", "costco"): 4.45,
    ("san diego, ca", "arco"): 4.55,
    ("san diego, ca", "76"): 4.66,
    ("san diego, ca", "shell"): 4.84,
    ("san diego, ca", "chevron"): 4.94,
    ("san diego, ca", None): 4.69,
    ("las vegas, nv", "costco"): 3.81,
    ("las vegas, nv", "arco"): 3.89,
    ("las vegas, nv", "shell"): 4.04,
    ("las vegas, nv", "chevron"): 4.12,
    ("las vegas, nv", "sinclair"): 3.93,
    ("las vegas, nv", None): 3.96,
    ("albuquerque, nm", "costco"): 3.32,
    ("albuquerque, nm", "circle k"): 3.41,
    ("albuquerque, nm", "shell"): 3.56,
    ("albuquerque, nm", "chevron"): 3.65,
    ("albuquerque, nm", "valero"): 3.46,
    ("albuquerque, nm", None): 3.49,
    ("el paso, tx", "costco"): 3.09,
    ("el paso, tx", "circle k"): 3.14,
    ("el paso, tx", "shell"): 3.28,
    ("el paso, tx", "chevron"): 3.34,
    ("el paso, tx", "valero"): 3.18,
    ("el paso, tx", None): 3.21,
    ("amarillo, tx", "love's"): 3.17,
    ("amarillo, tx", "travelcenters of america"): 3.22,
    ("amarillo, tx", "shell"): 3.31,
    ("amarillo, tx", "chevron"): 3.38,
    ("amarillo, tx", None): 3.24,
    (None, "costco"): 3.65,
    (None, "sam's club"): 3.68,
    (None, "qt"): 3.78,
    (None, "circle k"): 3.84,
    (None, "arco"): 3.81,
    (None, "valero"): 3.87,
    (None, "76"): 3.90,
    (None, "mobil"): 3.94,
    (None, "exxon"): 3.96,
    (None, "shell"): 3.98,
    (None, "chevron"): 4.08,
    (None, "texaco"): 4.03,
    (None, "bp"): 3.99,
    (None, "sinclair"): 3.88,
    (None, "fry's fuel"): 3.74,
    (None, "speedway"): 3.83,
    (None, "7-eleven"): 3.84,
    (None, "love's"): 3.89,
    (None, "travelcenters of america"): 3.93,
}


KNOWN_BRANDS = (
    "costco",
    "sam's club",
    "qt",
    "quiktrip",
    "circle k",
    "shell",
    "chevron",
    "texaco",
    "76",
    "mobil",
    "exxon",
    "sinclair",
    "valero",
    "arco",
    "bp",
    "marathon",
    "fry's fuel",
    "kroger fuel",
    "speedway",
    "7-eleven",
    "love's",
    "loves",
    "travelcenters of america",
    "ta",
    "pilot",
    "flying j",
)


def normalize_text(value):
    if not value:
        return ""
    cleaned = re.sub(r"\s+", " ", value.strip().lower())
    return cleaned


def normalize_brand(name):
    text = normalize_text(name)
    alias_map = {
        "quiktrip": "qt",
        "76 gas": "76",
        "extra mile": "chevron",
        "mobil gas": "mobil",
        "exxonmobil": "exxon",
        "kroger fuel center": "fry's fuel",
        "frys fuel": "fry's fuel",
        "frys fuel center": "fry's fuel",
        "frys food and drug fuel center": "fry's fuel",
        "loves": "love's",
        "ta": "travelcenters of america",
        "pilot travel center": "pilot",
        "pilot flying j": "pilot",
    }
    if text in alias_map:
        return alias_map[text]
    for brand in KNOWN_BRANDS:
        if brand in text:
            return alias_map.get(brand, brand)
    return None


def extract_city_state(address):
    if not address:
        return None
    parts = [part.strip().lower() for part in address.split(",") if part.strip()]
    if len(parts) < 3:
        return None
    city = parts[-3]
    state = parts[-2].split()[0]
    if len(state) != 2:
        return None
    return f"{city}, {state}"


def format_price(price, source):
    return f"${price:.2f} per gallon ({source})"


def lookup_gas_price(station_name, address):
    brand = normalize_brand(station_name)
    city_state = extract_city_state(address)

    if city_state and brand and (city_state, brand) in GAS_PRICE_DATABASE:
        return format_price(GAS_PRICE_DATABASE[(city_state, brand)], "local city/brand estimate")
    if city_state and (city_state, None) in GAS_PRICE_DATABASE:
        return format_price(GAS_PRICE_DATABASE[(city_state, None)], "local city average")
    if brand and (None, brand) in GAS_PRICE_DATABASE:
        return format_price(GAS_PRICE_DATABASE[(None, brand)], "brand average")
    return None
