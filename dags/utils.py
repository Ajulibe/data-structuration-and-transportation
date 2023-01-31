import json
import requests
from datetime import date
from time import mktime

def json_dump_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def read_from_api(url, params):
    response = requests.get(url, params=params)
    return response.json()

def to_seconds_since_epoch(input_date: str) -> int:
    return int(mktime(date.fromisoformat(input_date).timetuple()))