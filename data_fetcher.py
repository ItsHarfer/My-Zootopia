"""
data_fetcher.py

This module is responsible for retrieving animal data from external sources.
Currently, it fetches animal information using the API Ninjas Animal API.

The main function `fetch_data(animal_name)` returns a list of animal dictionaries,
each containing keys such as 'name', 'taxonomy', 'locations', and 'characteristics'.

Example output format:
[
    {
        "name": "Fox",
        "taxonomy": {...},
        "locations": [...],
        "characteristics": {...}
    },
    ...
]
"""

import json

import requests

from config import API_NINJA_KEY, API_NINJA_URL


def fetch_data(endpoint_name: str, animal_name: str) -> list[dict]:
    """
    Sends a GET request to the specified API endpoint with an optional query.
    Returns the JSON response as a list of animal dictionaries.

    :param animal_name: Query value (e.g., 'Fox').
    :param endpoint_name: Query parameter name (e.g., 'name').
    :return: List of animal data dictionaries.
    """
    try:
        response = requests.get(
            f"{API_NINJA_URL}?{endpoint_name}={animal_name}",
            headers={"X-Api-Key": API_NINJA_KEY},
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data

    except requests.RequestException as e:
        print(f"Failed to fetch data from API: {e}")
        return []


def fetch_local_data(file_path: str, is_json: bool = False) -> str | dict:
    """
    Reads data from the specified file path.

    :param file_path: Path to the file to read.
    :param is_json: Whether to parse the file as JSON. Defaults to False.
    :return: Parsed JSON data as a dictionary if is_json is True,
             otherwise the file content as a string.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file) if is_json else file.read()
    except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return "" if not is_json else {}
