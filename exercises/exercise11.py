from collections import Counter
from datetime import date
from time import mktime


def to_seconds_since_epoch(input_date: str) -> int:
  return int(mktime(date.fromisoformat(input_date).timetuple()))

import requests

BASE_URL = "https://opensky-network.org/api"

params = {
    "airport": "LFPG", # ICAO code for CDG
    "begin": to_seconds_since_epoch("2022-12-01"),
    "end": to_seconds_since_epoch("2022-12-02")
}

cdg_flights = f"{BASE_URL}/flights/departure"

response = requests.get(cdg_flights, params=params)

flights = response.json()

print(flights)

counter = Counter([flight["estArrivalAirport"] for flight in flights if (flight["estArrivalAirport"] is not None and flight["estArrivalAirport"] != "LFPG")])
print(counter.most_common(1))