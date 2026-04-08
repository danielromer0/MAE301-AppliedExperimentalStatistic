# Road Trip Planner

This Python script helps plan a road trip by finding the best route using Google Maps, determining if your car is gas or electric based on year, make, and model, and recommending stops for fuel or charging.

## Requirements

- Python 3.x
- googlemaps library
- requests library

Install dependencies:
```
pip install googlemaps requests
```

## Setup

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Directions API and Places API for your project.
3. Replace `YOUR_GOOGLE_MAPS_API_KEY` in the script with your actual API key, or set the `GMAPS_API_KEY` environment variable.

4. (Optional) For accurate gas prices, get a free EIA API key from [EIA Open Data](https://www.eia.gov/opendata/register.php).
5. Set the `EIA_API_KEY` environment variable with your EIA API key.

6. (Optional) For accurate EV charging station information, get a free NREL API key from [NREL Developer Network](https://developer.nrel.gov/signup/).
7. Set the `NREL_API_KEY` environment variable with your NREL API key.

If the EPA vehicle lookup fails, the planner now falls back to a built-in vehicle database.

The database is stored in `vehicle_database.py` and is used to provide range and tank size data for common models when the external API returns missing values.

## Usage

Run the script:
```
python roadtrip_planner.py
```

Enter the required information when prompted:
- Starting location
- Destination
- Car year
- Car make
- Car model

The script will output:
- Fuel type of your car
- Total distance and duration
- Recommended stops along the route

## Notes

- Fuel type is determined using the EPA Fuel Economy API, with a local fallback database if the API does not provide range data.
- Stops are recommended based on the vehicle's estimated range, not a fixed interval.
- Gas prices are fetched from the EIA API (national average, updated weekly) if API key is provided.
- For electric vehicles, charging stations are found using the NREL API, which includes pricing information where available.

## Limitations

- Requires Google Maps API key (not free for heavy usage).
- No real-time gas prices; placeholders used.
- Simple stop recommendation logic.
