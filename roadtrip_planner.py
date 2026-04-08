import os
from urllib.parse import urlencode
import googlemaps
import requests
from gas_price_database import lookup_gas_price
from vehicle_info import get_vehicle_info

# Note: You need to get your own Google Maps API key from https://console.cloud.google.com/
# Set it via environment variable GMAPS_API_KEY or replace the default string.
GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY", "AIzaSyBMRKiCAPdJoQtkyHvsg9WtqGOOjiprtm8")

# EIA API key for gas prices (free, register at https://www.eia.gov/opendata/register.php)
EIA_API_KEY = os.environ.get("EIA_API_KEY", "lyeznbocYSSyqJM7WA1VtcAAFcNRW6Ix7JvFCj06")

# NREL API key for EV charging stations (free, register at https://developer.nrel.gov/signup/)
NREL_API_KEY = os.environ.get("NREL_API_KEY", "eGc3hd4T4xQBQECSmtSecoTRa03d7X7NFc2br3So")

# Function to get route
def get_route(start, end):
    if not GMAPS_API_KEY or GMAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Error: Google Maps API key is missing or not configured.")
        print("Set the GMAPS_API_KEY environment variable or update GMAPS_API_KEY in the script.")
        return None, None, None

    try:
        gmaps = googlemaps.Client(key=GMAPS_API_KEY)
        directions = gmaps.directions(start, end, mode="driving")
    except ValueError as exc:
        print(f"Google Maps API error: {exc}")
        return None, None, None
    except Exception as exc:
        print(f"Error fetching route: {exc}")
        return None, None, None

    if directions:
        route = directions[0]
        distance = route['legs'][0]['distance']['text']
        duration = route['legs'][0]['duration']['text']
        steps = route['legs'][0]['steps']
        return distance, duration, steps
    return None, None, None


def build_google_maps_link(start, end, waypoints=None):
    params = {
        "api": 1,
        "origin": start,
        "destination": end,
        "travelmode": "driving",
    }
    if waypoints:
        params["waypoints"] = "|".join(waypoints[:9])
    params = urlencode(params)
    return f"https://www.google.com/maps/dir/?{params}"


def extract_price_value(price_text):
    if not price_text or not price_text.startswith("$"):
        return float("inf")
    try:
        return float(price_text.split()[0].replace("$", ""))
    except (TypeError, ValueError):
        return float("inf")

# Function to get gas prices from EIA API
def get_gas_price():
    if not EIA_API_KEY or EIA_API_KEY == "YOUR_EIA_API_KEY":
        return "EIA API key not configured"
    
    try:
        url = "https://api.eia.gov/v1/petroleum/PET_EMP_PTE_NUS_DW/data"
        params = {
            "frequency": "weekly",
            "data[0]": "value",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "limit": 1,
            "api_key": EIA_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code != 200:
            if isinstance(data, dict) and 'error' in data:
                message = data['error'].get('message', 'Unknown error')
                return f"Error fetching gas price: {message}"
            return f"Error fetching gas price: HTTP {response.status_code}"

        if isinstance(data, dict) and 'error' in data:
            message = data['error'].get('message', 'Unknown error')
            return f"Error fetching gas price: {message}"

        if 'data' in data and data['data']:
            price = data['data'][0]['value']
            return f"${price} per gallon (national average)"
        else:
            return "Price data not available (EIA returned no data)"
    except Exception as exc:
        return f"Error fetching gas price: {exc}"

# Function to find EV charging stations using NREL API
def find_ev_stations(location, radius=25):
    if not NREL_API_KEY or NREL_API_KEY == "YOUR_NREL_API_KEY":
        return []
    
    try:
        url = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json"
        params = {
            "api_key": NREL_API_KEY,
            "fuel_type": "ELEC",
            "latitude": location[0],
            "longitude": location[1],
            "radius": radius,
            "limit": 3
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code != 200:
            message = data.get('error', {}).get('message', response.reason if hasattr(response, 'reason') else 'Unknown error')
            print(f"Error fetching EV stations: HTTP {response.status_code}: {message}")
            return []

        stations = []
        if 'fuel_stations' in data:
            for station in data['fuel_stations']:
                name = station['station_name']
                address = station.get('street_address', 'Address not available')
                price = station.get('ev_pricing', 'Pricing not available')
                stations.append({'name': name, 'address': address, 'price': price})
        else:
            print("Warning: NREL returned no fuel_stations.")
        return stations
    except Exception as exc:
        print(f"Error fetching EV stations: {exc}")
        return []

# Function to find gas stations or charging stations
def find_stations(location, fuel_type, radius=5000):
    if fuel_type == "electric":
        # Parse location string to tuple
        lat, lng = map(float, location.split(','))
        return find_ev_stations((lat, lng), radius=radius/1000)  # convert meters to km
    else:
        # For gas stations, only keep stations we can price from the local database.
        gmaps = googlemaps.Client(key=GMAPS_API_KEY)
        places = gmaps.places(query="gas station", location=location, radius=radius)
        stations = []
        if 'results' in places:
            for result in places['results']:
                name = result['name']
                address = result.get('formatted_address', 'Address not available')
                price = lookup_gas_price(name, address)
                if not price:
                    continue
                stations.append({'name': name, 'address': address, 'price': price})
                if len(stations) == 3:
                    break
        return stations

# Main function
def main():
    print("Road Trip Planner")
    start = input("Enter starting location: ")
    end = input("Enter destination: ")
    year = input("Enter car year: ")
    make = input("Enter car make: ")
    model = input("Enter car model: ")

    vehicle_data = get_vehicle_info(year, make, model)
    if vehicle_data is None:
        print("Warning: Could not retrieve vehicle range data from the API or local database.")
        fuel_type = "gas"
        vehicle_range_miles = None
    else:
        fuel_type = vehicle_data["fuel_type"]
        vehicle_range_miles = vehicle_data["range_miles"]
        tank_size = vehicle_data.get("tank_size")
        source = vehicle_data.get("source", "unknown")
        print(f"Detected fuel type: {fuel_type} (source: {source})")
        if vehicle_range_miles:
            print(f"Estimated vehicle range: {vehicle_range_miles:.0f} miles")
        if tank_size:
            print(f"Detected tank size: {tank_size} gallons")

    if vehicle_data is None or vehicle_range_miles is None or vehicle_range_miles == 0:
        stop_interval = 200000  # fallback to 200 km if no range is available
    else:
        stop_interval = int(vehicle_range_miles * 1609.34 * 0.8)
        # Removed minimum cap to allow shorter intervals for vehicles with limited range

    if fuel_type not in ("electric", "gas"):
        fuel_type = "gas"

    print(f"Your car fuel type: {fuel_type}")
    distance, duration, steps = get_route(start, end)
    if not distance:
        print("Could not find route.")
        return

    print(f"Total distance: {distance}")
    print(f"Estimated duration: {duration}")
    print(f"Recommended stop interval: {stop_interval / 1609.34:.0f} miles")

    print("\nRecommended stops:")
    cumulative_distance = 0
    next_stop_distance = stop_interval
    last_location = None
    recommended_waypoints = []
    for step in steps:
        step_distance = step['distance']['value']  # meters
        cumulative_distance += step_distance
        while cumulative_distance >= next_stop_distance:
            lat = step['end_location']['lat']
            lng = step['end_location']['lng']
            location = f"{lat},{lng}"
            if location != last_location:
                stations = find_stations(location, fuel_type)
                if stations:
                    stations.sort(key=lambda station: extract_price_value(station["price"]))
                    print(f"At approx {next_stop_distance / 1609.34:.0f} miles from the starting point:")
                    for station in stations:
                        print(f"  - {station['name']} at {station['address']} (Price: {station['price']})")
                    first_stop_address = stations[0]['address']
                    if first_stop_address not in recommended_waypoints:
                        recommended_waypoints.append(first_stop_address)
                    print()  # Add a blank line between stops
                last_location = location
            next_stop_distance += stop_interval

    maps_link = build_google_maps_link(start, end, recommended_waypoints)
    print(f"Google Maps route link: {maps_link}")
    if len(recommended_waypoints) > 9:
        print("Note: Google Maps links support a limited number of waypoint stops, so only the first 9 recommended stops were included in the link.")

if __name__ == "__main__":
    main()
