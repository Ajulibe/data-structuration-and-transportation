# Akachukwu Benjamin Ajulibe
# Maheshbhai CHAUHAN

from airflow.decorators import dag, task
from datetime import datetime
import json
from utils import read_from_api, json_dump_to_file


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 29),
    catchup=False
)
def assignment_medium():
    # API endpoint to retrieve stock symbol information
    API_URL = "https://www.alphavantage.co/query"

    @task(multiple_outputs=True)
    def read_data() -> dict:
        # API parameters
        params = {
            "function": "SYMBOL_SEARCH",  # function to search symbols
            "keywords": "tencent",  # search keyword
            "apikey": "demo"  # API key
        }
        # call API to retrieve symbol search results
        search_results = read_from_api(API_URL, params)
        # return search results
        return search_results

    @task
    def count_frankfurt_region(data: dict) -> None:
        # Get the list of search results from the API
        search_results = data["bestMatches"]
        # Initialize a counter for Frankfurt region appearances
        frankfurt_count = 0
        # Iterate through the search results
        for result in search_results:
            # Check if the region of the result is Frankfurt
            if result["4. region"] == "Frankfurt":
                # Increment the counter if it is
                frankfurt_count += 1
        # Print the final count
        print("Frankfurt region appeared in the search results:", frankfurt_count, "times")

    @task
    def write_data(data: dict) -> None:
        # write search results to a file
        json_dump_to_file(data, "./dags/data/search_results.json")

    # Call functions to retrieve and process search results
    results = read_data()
    count_frankfurt_region(results)
    write_data(results)


_ = assignment_medium()
