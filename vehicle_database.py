import re
import difflib

VEHICLE_DATABASE = {
    # Toyota
    ("2020", "toyota", "camry"): {"fuel_type": "gas", "range_miles": 420.0, "tank_size": 13.2},
    ("2023", "toyota", "corolla"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 13.2},
    ("2022", "toyota", "rav4"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 14.5},
    ("2021", "toyota", "highlander"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 17.9},
    ("2024", "toyota", "prius"): {"fuel_type": "hybrid", "range_miles": 400.0, "tank_size": 11.4},
    ("2023", "toyota", "tundra"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 22.5},
    ("2022", "toyota", "sienna"): {"fuel_type": "gas", "range_miles": 330.0, "tank_size": 18.0},
    ("2021", "toyota", "4runner"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 23.0},
    ("2020", "toyota", "avalon"): {"fuel_type": "gas", "range_miles": 410.0, "tank_size": 14.5},
    ("2024", "toyota", "crown"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 14.5},

    # Honda
    ("2021", "honda", "accord"): {"fuel_type": "gas", "range_miles": 485.0, "tank_size": 14.8},
    ("2022", "honda", "civic"): {"fuel_type": "gas", "range_miles": 420.0, "tank_size": 12.4},
    ("2023", "honda", "crv"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 14.0},
    ("2020", "honda", "pilot"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 19.5},
    ("2022", "honda", "odyssey"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.5},
    ("2021", "honda", "hrv"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2024", "honda", "insight"): {"fuel_type": "hybrid", "range_miles": 420.0, "tank_size": 10.6},
    ("2023", "honda", "passport"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 19.5},
    ("2020", "honda", "ridgeline"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 19.5},
    ("2022", "honda", "zrv"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 14.0},

    # Ford
    ("2022", "ford", "f150"): {"fuel_type": "gas", "range_miles": 470.0, "tank_size": 25.0},
    ("2024", "ford", "mustang"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 16.0},
    ("2023", "ford", "explorer"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 20.2},
    ("2021", "ford", "bronco"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 16.0},
    ("2022", "ford", "ranger"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 18.0},
    ("2020", "ford", "edge"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.5},
    ("2023", "ford", "escape"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.0},
    ("2024", "ford", "maverick"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 13.8},
    ("2021", "ford", "f250"): {"fuel_type": "gas", "range_miles": 450.0, "tank_size": 34.0},
    ("2022", "ford", "transit"): {"fuel_type": "gas", "range_miles": 300.0, "tank_size": 25.0},

    # Chevrolet
    ("2023", "chevrolet", "silverado"): {"fuel_type": "gas", "range_miles": 450.0, "tank_size": 24.0},
    ("2022", "chevrolet", "equinox"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.6},
    ("2021", "chevrolet", "traverse"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.4},
    ("2020", "chevrolet", "malibu"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 15.8},
    ("2024", "chevrolet", "corvette"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.5},
    ("2023", "chevrolet", "tahoe"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 24.0},
    ("2022", "chevrolet", "suburban"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 28.0},
    ("2021", "chevrolet", "colorado"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 21.0},
    ("2020", "chevrolet", "cruze"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.7},
    ("2024", "chevrolet", "bolt"): {"fuel_type": "electric", "range_miles": 259.0, "tank_size": None},

    # Tesla
    ("2024", "tesla", "model3"): {"fuel_type": "electric", "range_miles": 272.0, "tank_size": None},
    ("2023", "tesla", "modely"): {"fuel_type": "electric", "range_miles": 326.0, "tank_size": None},
    ("2022", "tesla", "models"): {"fuel_type": "electric", "range_miles": 405.0, "tank_size": None},
    ("2021", "tesla", "modelx"): {"fuel_type": "electric", "range_miles": 325.0, "tank_size": None},
    ("2020", "tesla", "cybertruck"): {"fuel_type": "electric", "range_miles": 340.0, "tank_size": None},

    # Nissan
    ("2022", "nissan", "leaf"): {"fuel_type": "electric", "range_miles": 226.0, "tank_size": None},
    ("2023", "nissan", "sentra"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 12.4},
    ("2021", "nissan", "altima"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 16.2},
    ("2020", "nissan", "rogue"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 14.5},
    ("2024", "nissan", "pathfinder"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.5},
    ("2022", "nissan", "titan"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 26.0},
    ("2021", "nissan", "kicks"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 10.8},
    ("2023", "nissan", "ariya"): {"fuel_type": "electric", "range_miles": 289.0, "tank_size": None},
    ("2020", "nissan", "murano"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.0},
    ("2022", "nissan", "frontier"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 21.1},

    # Jeep
    ("2021", "jeep", "wrangler"): {"fuel_type": "gas", "range_miles": 300.0, "tank_size": 18.6},
    ("2023", "jeep", "grandcherokee"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 24.6},
    ("2022", "jeep", "compass"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.5},
    ("2020", "jeep", "renegade"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 12.7},
    ("2024", "jeep", "gladiator"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 22.0},
    ("2021", "jeep", "cherokee"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2023", "jeep", "wagoneer"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 26.5},
    ("2022", "jeep", "grandwagoneer"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 26.5},
    ("2020", "jeep", "patriot"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 13.6},
    ("2024", "jeep", "avenger"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 13.5},

    # BMW
    ("2023", "bmw", "i3"): {"fuel_type": "electric", "range_miles": 153.0, "tank_size": None},
    ("2022", "bmw", "3series"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 15.6},
    ("2021", "bmw", "5series"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.0},
    ("2020", "bmw", "x3"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 17.2},
    ("2024", "bmw", "x5"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 21.9},
    ("2023", "bmw", "i4"): {"fuel_type": "electric", "range_miles": 301.0, "tank_size": None},
    ("2022", "bmw", "i7"): {"fuel_type": "electric", "range_miles": 318.0, "tank_size": None},
    ("2021", "bmw", "x1"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.1},
    ("2020", "bmw", "2series"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 13.7},
    ("2024", "bmw", "ix"): {"fuel_type": "electric", "range_miles": 324.0, "tank_size": None},

    # Subaru
    ("2020", "subaru", "outback"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.5},
    ("2022", "subaru", "forester"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.6},
    ("2021", "subaru", "crosstrek"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.6},
    ("2023", "subaru", "legacy"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.5},
    ("2024", "subaru", "ascent"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.3},
    ("2020", "subaru", "impreza"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2022", "subaru", "wrx"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 16.6},
    ("2021", "subaru", "brz"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 13.2},
    ("2023", "subaru", "solterra"): {"fuel_type": "electric", "range_miles": 222.0, "tank_size": None},
    ("2024", "subaru", "xv"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},

    # Volkswagen
    ("2022", "volkswagen", "id4"): {"fuel_type": "electric", "range_miles": 250.0, "tank_size": None},
    ("2023", "volkswagen", "golf"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2021", "volkswagen", "jetta"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 14.5},
    ("2020", "volkswagen", "tiguan"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.3},
    ("2024", "volkswagen", "atlas"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.6},
    ("2022", "volkswagen", "passat"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.5},
    ("2021", "volkswagen", "arteon"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 17.4},
    ("2023", "volkswagen", "taos"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2020", "volkswagen", "beetle"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 14.5},
    ("2024", "volkswagen", "idbuzz"): {"fuel_type": "electric", "range_miles": 200.0, "tank_size": None},

    # Mazda
    ("2021", "mazda", "cx5"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 15.9},
    ("2023", "mazda", "cx50"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2022", "mazda", "cx9"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.0},
    ("2020", "mazda", "cx3"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 12.7},
    ("2024", "mazda", "cx90"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.0},
    ("2021", "mazda", "mazda3"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 13.2},
    ("2023", "mazda", "mazda6"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.4},
    ("2022", "mazda", "mx5"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 11.9},
    ("2020", "mazda", "rx8"): {"fuel_type": "gas", "range_miles": 300.0, "tank_size": 15.9},
    ("2024", "mazda", "cx30"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 12.7},

    # Kia
    ("2023", "kia", "ev6"): {"fuel_type": "electric", "range_miles": 310.0, "tank_size": None},
    ("2022", "kia", "sportage"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.4},
    ("2021", "kia", "sorento"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 17.7},
    ("2020", "kia", "telluride"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.8},
    ("2024", "kia", "seltos"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2023", "kia", "k5"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.8},
    ("2022", "kia", "carnival"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.0},
    ("2021", "kia", "stinger"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 15.9},
    ("2020", "kia", "soul"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 14.3},
    ("2024", "kia", "ev9"): {"fuel_type": "electric", "range_miles": 304.0, "tank_size": None},

    # Hyundai
    ("2022", "hyundai", "ioniq5"): {"fuel_type": "electric", "range_miles": 303.0, "tank_size": None},
    ("2023", "hyundai", "tucson"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 16.4},
    ("2021", "hyundai", "santafe"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.8},
    ("2020", "hyundai", "palisade"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.8},
    ("2024", "hyundai", "sonata"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2022", "hyundai", "elantra"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 14.0},
    ("2021", "hyundai", "kona"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2023", "hyundai", "venue"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 11.9},
    ("2020", "hyundai", "accent"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 11.9},
    ("2024", "hyundai", "ioniq6"): {"fuel_type": "electric", "range_miles": 361.0, "tank_size": None},

    # GMC
    ("2020", "gmc", "sierra"): {"fuel_type": "gas", "range_miles": 450.0, "tank_size": 24.0},
    ("2022", "gmc", "yukon"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 24.0},
    ("2021", "gmc", "terrain"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.6},
    ("2023", "gmc", "acadia"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 21.7},
    ("2024", "gmc", "canyon"): {"fuel_type": "gas", "range_miles": 400.0, "tank_size": 21.0},
    ("2020", "gmc", "savana"): {"fuel_type": "gas", "range_miles": 300.0, "tank_size": 31.0},
    ("2022", "gmc", "hummer"): {"fuel_type": "electric", "range_miles": 329.0, "tank_size": None},
    ("2021", "gmc", "jimmy"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.6},
    ("2023", "gmc", "denali"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 24.0},
    ("2024", "gmc", "yukonxl"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 28.0},

    # Rivian
    ("2024", "rivian", "r1t"): {"fuel_type": "electric", "range_miles": 314.0, "tank_size": None},
    ("2023", "rivian", "r1s"): {"fuel_type": "electric", "range_miles": 316.0, "tank_size": None},

    # Polestar
    ("2024", "polestar", "2"): {"fuel_type": "electric", "range_miles": 270.0, "tank_size": None},
    ("2023", "polestar", "3"): {"fuel_type": "electric", "range_miles": 300.0, "tank_size": None},

    # Lucid
    ("2023", "lucid", "air"): {"fuel_type": "electric", "range_miles": 516.0, "tank_size": None},

    # Cadillac
    ("2022", "cadillac", "escalade"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 24.0},
    ("2021", "cadillac", "xt5"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 19.0},
    ("2020", "cadillac", "xt6"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.0},
    ("2024", "cadillac", "lyriq"): {"fuel_type": "electric", "range_miles": 300.0, "tank_size": None},
    ("2023", "cadillac", "ct5"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 17.0},

    # Lexus
    ("2023", "lexus", "rx"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.8},
    ("2022", "lexus", "es"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2021", "lexus", "nx"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2020", "lexus", "gx"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 23.0},
    ("2024", "lexus", "lx"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 24.6},

    # Mercedes-Benz
    ("2022", "mercedesbenz", "cclass"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 17.4},
    ("2021", "mercedesbenz", "eclass"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 21.1},
    ("2020", "mercedesbenz", "glc"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 17.4},
    ("2024", "mercedesbenz", "eqs"): {"fuel_type": "electric", "range_miles": 350.0, "tank_size": None},
    ("2023", "mercedesbenz", "eqe"): {"fuel_type": "electric", "range_miles": 279.0, "tank_size": None},

    # Audi
    ("2023", "audi", "a3"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 13.2},
    ("2022", "audi", "a4"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.3},
    ("2021", "audi", "a6"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 19.3},
    ("2020", "audi", "q5"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 18.5},
    ("2024", "audi", "q8"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 22.5},

    # Volvo
    ("2022", "volvo", "xc60"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.5},
    ("2021", "volvo", "xc90"): {"fuel_type": "gas", "range_miles": 350.0, "tank_size": 18.5},
    ("2020", "volvo", "s60"): {"fuel_type": "gas", "range_miles": 380.0, "tank_size": 15.9},
    ("2024", "volvo", "ex90"): {"fuel_type": "electric", "range_miles": 300.0, "tank_size": None},
    ("2023", "volvo", "c40"): {"fuel_type": "electric", "range_miles": 260.0, "tank_size": None},
}


def normalize_vehicle_key(year, make, model):
    return (
        year.strip(),
        re.sub(r"[^a-z0-9]+", "", make.strip().lower()),
        re.sub(r"[^a-z0-9]+", "", model.strip().lower()),
    )


def lookup_vehicle(year, make, model):
    key = normalize_vehicle_key(year, make, model)
    if key in VEHICLE_DATABASE:
        return VEHICLE_DATABASE[key]
    
    # Fuzzy matching
    all_keys = list(VEHICLE_DATABASE.keys())
    make_model = f"{key[1]} {key[2]}"
    candidates = []
    for k in all_keys:
        km = f"{k[1]} {k[2]}"
        if difflib.SequenceMatcher(None, make_model, km).ratio() > 0.8:
            candidates.append(k)
    if candidates:
        # Take the best match
        best = max(candidates, key=lambda k: difflib.SequenceMatcher(None, make_model, f"{k[1]} {k[2]}").ratio())
        return VEHICLE_DATABASE[best]
    return None
