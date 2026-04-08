import requests
import xml.etree.ElementTree as ET

from vehicle_database import lookup_vehicle

BASE_URL = "https://www.fueleconomy.gov/ws/rest"


def _get_xml_root(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return ET.fromstring(response.text)


def find_vehicle_id(year, make, model):
    url = f"{BASE_URL}/vehicle/menu/options?year={year}&make={make}&model={model}"
    root = _get_xml_root(url)
    option = root.find("menuItem")
    if option is None:
        option = root.find("./menuItem")
    if option is None:
        items = root.findall('.//menuItem')
        if items:
            option = items[0]
    if option is not None:
        return option.findtext("value")
    return None


def normalize_fuel_type(fuel_type):
    if not fuel_type:
        return "gas"
    fuel_type = fuel_type.lower()
    if "electric" in fuel_type or "battery" in fuel_type or "plug-in" in fuel_type or "utility" in fuel_type:
        return "electric"
    return "gas"


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_vehicle_info(year, make, model):
    print(f"Retrieving vehicle info for {year} {make} {model}...")
    vehicle_id = find_vehicle_id(year, make, model)
    if not vehicle_id:
        print("No vehicle found in EPA API, trying local database...")
        fallback = lookup_vehicle(year, make, model)
        if fallback:
            print(f"Found in local database: {fallback}")
            return {
                "vehicle_id": None,
                "fuel_type": fallback["fuel_type"],
                "range_miles": fallback["range_miles"],
                "tank_size": fallback["tank_size"],
                "source": "local-db",
            }
        print("No data found in local database either.")
        return None

    print(f"Found vehicle ID {vehicle_id}, fetching details...")
    url = f"{BASE_URL}/vehicle/{vehicle_id}"
    root = _get_xml_root(url)

    fuel_type = normalize_fuel_type(root.findtext("fuelType") or root.findtext("fuelType1") or root.findtext("fuelType2"))
    range_miles = parse_float(root.findtext("range"))
    if range_miles is None:
        range_miles = parse_float(root.findtext("rangeCity"))
    if range_miles is None:
        range_miles = parse_float(root.findtext("rangeHwy"))
    tank_size = parse_float(root.findtext("tankSize") or root.findtext("fuelTankSize"))

    # For gas vehicles, if range is 0 or None, calculate estimated range from MPG and tank size
    if fuel_type == "gas" and (range_miles is None or range_miles == 0.0) and tank_size:
        city_mpg = parse_float(root.findtext("city08"))
        highway_mpg = parse_float(root.findtext("highway08"))
        if city_mpg and highway_mpg:
            avg_mpg = (city_mpg + highway_mpg) / 2
            range_miles = avg_mpg * tank_size
            print(f"Calculated estimated range for gas vehicle: {range_miles:.0f} miles (avg MPG: {avg_mpg:.1f}, tank: {tank_size} gal)")

    print(f"EPA data: fuel_type={fuel_type}, range_miles={range_miles}, tank_size={tank_size}")

    result = {
        "vehicle_id": vehicle_id,
        "fuel_type": fuel_type,
        "range_miles": range_miles,
        "tank_size": tank_size,
        "source": "EPA",
    }

    if result["range_miles"] in (None, 0.0):
        print("EPA range is missing or zero, trying local database...")
        fallback = lookup_vehicle(year, make, model)
        if fallback:
            print(f"Using local database fallback: {fallback}")
            fallback_result = {
                "vehicle_id": vehicle_id,
                "fuel_type": fallback["fuel_type"],
                "range_miles": fallback["range_miles"],
                "tank_size": fallback["tank_size"],
                "source": "local-db",
            }
            return fallback_result
        else:
            # No local data, use default based on fuel_type
            default_range = 300.0 if result["fuel_type"] == "electric" else 400.0
            print(f"No range data available, using default range: {default_range} miles")
            result["range_miles"] = default_range
            result["source"] = "default"

    return result
