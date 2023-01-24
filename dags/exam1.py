# Akachukwu Benjamin Ajulibe


from collections import Counter
from datetime import date
from time import mktime
import json
from airflow.decorators import dag, task
import requests
from datetime import datetime



@dag(
    schedule=None,
    start_date=datetime(2023, 1, 24),
    catchup=False
)
def maingoal():
    BASE_URL = "https://opensky-network.org/api"

    def to_seconds_since_epoch(input_date: str) -> int:
        return int(mktime(date.fromisoformat(input_date).timetuple()))

    @task
    def fetch_flights() -> str:
        params = {
            "airport": "LFPG",  # ICAO code for CDG
            "begin": to_seconds_since_epoch("2022-12-01"),
            "end": to_seconds_since_epoch("2022-12-02")
        }
        cdg_flights = f"{BASE_URL}/flights/departure"
        response = requests.get(cdg_flights, params=params)
        flights = response.json()
        print(json.dumps(flights))
        return json.dumps(flights)

    @task
    def write_flights(data: json) -> None:
        with open("./dags/data/flights.json", "w") as f:
            f.write(data)

    flights = fetch_flights()
    write_flights(flights)

_ = maingoal()
