from dataclasses import dataclass

from airflow import DAG
from datetime import datetime, timedelta
from typing import Dict, List
from time import mktime
from datetime import date
from airflow.decorators import dag, task
import requests
import json

default_args = {
    'owner': 'me',
    'start_date': datetime(2022, 1, 1),
    'schedule_interval': '0 1 * * *'
}

@dag(
    default_args=default_args,
    start_date=datetime(2023, 1, 24),
    catchup=False,
)

def easy():
    BASE_URL = "https://opensky-network.org/api"

    def to_seconds_since_epoch(input_date: str) -> int:
        return int(mktime(date.fromisoformat(input_date).timetuple()))

    @task(multiple_outputs=True)
    def fetch_flights() -> Dict:
        params = {
            "airport": "LFPG",  # ICAO code for CDG
            "begin": to_seconds_since_epoch("2022-12-01"),
            "end": to_seconds_since_epoch("2022-12-02")
        }
        cdg_flights = f"{BASE_URL}/flights/departure"
        response = requests.get(cdg_flights, params=params)
        flights = response.json()
        print(json.dumps(flights))
        return {"flights": flights}

    @task
    def write_flights(data: Dict) -> None:
        with open("./dags/data/flights_easy.json", "w") as f:
            json.dump(data['flights'], f)

    flights = fetch_flights()
    write_flights(flights)

_ = easy()