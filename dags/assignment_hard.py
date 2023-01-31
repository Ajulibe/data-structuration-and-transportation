# Akachukwu Benjamin Ajulibe
# Maheshbhai CHAUHAN

from airflow.decorators import dag, task
from datetime import datetime, timedelta
from dataclasses import astuple, dataclass
from utils import read_from_api, json_dump_to_file, to_seconds_since_epoch
import json
import sqlite3

@dataclass
class Flight:
  icao24: str
  firstSeen: int
  estDepartureAirport: str
  lastSeen: int
  estArrivalAirport: str
  callsign: str
  estDepartureAirportHorizDistance: int
  estDepartureAirportVertDistance: int
  estArrivalAirportHorizDistance: int
  estArrivalAirportVertDistance: int
  departureAirportCandidatesCount: int
  arrivalAirportCandidatesCount: int

@dag(
  schedule=None,
  start_date=datetime(2023, 1, 29),
  catchup=False
)
def assignment_hard():

  BASE_URL = "https://opensky-network.org/api"

  @task(multiple_outputs=True)
  def read_data(ds=None) -> dict:
    # Calculate last week's date
    last_week = datetime.strptime(ds, '%Y-%m-%d') - timedelta(days=7)
    # Calculate last week plus one day
    last_week_plus_one = last_week + timedelta(days=1)

    # API parameters
    params = {
        "airport": "LFPG", # airport code
        "begin": to_seconds_since_epoch(last_week.strftime("%Y-%m-%d")), # begin time in seconds
        "end": to_seconds_since_epoch(last_week_plus_one.strftime("%Y-%m-%d")) # end time in seconds
    }
    # Call API to retrieve flight information
    flight_info = read_from_api(f"{BASE_URL}/flights/departure", params)
    # Print flight information
    print(json.dumps(flight_info))
    # Return flight information
    return {"flights": flight_info}

  @task
  def write_data(flights: dict) -> None:
    json_dump_to_file(flights["flights"], "./dags/data/flights_hard.json")

  @task
  def write_to_db(flights: dict) -> None:
    # convert the flights data into a list of tuples
    flights = [astuple(Flight(**row)) for row in flights["flights"]]

    # create an in-memory SQLite database
    connection = sqlite3.connect(":memory:")
    # create the flights table
    connection.execute("CREATE TABLE flights (icao24 text, firstSeen int, estDepartureAirport text, lastSeen int, estArrivalAirport text, callsign text, estDepartureAirportHorizDistance int, estDepartureAirportVertDistance int, estArrivalAirportHorizDistance int, estArrivalAirportVertDistance int, departureAirportCandidatesCount int, arrivalAirportCandidatesCount int)")
    # insert flight data into the table
    connection.executemany("INSERT INTO flights VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?)", flights)
    # commit changes
    connection.commit()
    # retrieve data from the flights table
    res = connection.execute("SELECT * FROM flights")
    # print each row of data
    for row in res:
      print(row)

  flights = read_data()
  write_data(flights)
  write_to_db(flights)

_ = assignment_hard()
