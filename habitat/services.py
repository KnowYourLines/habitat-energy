import datetime
import logging
import math
from concurrent.futures import as_completed
from http import HTTPStatus

import requests
from requests import HTTPError, Timeout
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError
from requests_futures.sessions import FuturesSession

from habitat.models import Record

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://data.nationalgrideso.com/api/3/action/datastore_search?resource_id=e3e44433-7614-4c8c-9cbc-7808994d3a72"


def get_habitat_records():
    records = gather_records()
    save_records(records)
    return Record.objects.all()


def hit_endpoint(url, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            logger.debug(f"Attempt {attempt} to hit {url}")
            response = requests.get(url)
            logger.debug(f"Successfully hit {url} on attempt {attempt}")
            response.raise_for_status()
            data = response.json()["result"]
            logger.debug(f"Got payload from {url} on attempt {attempt}")
            return data
        except (HTTPError, requests.ConnectionError, Timeout) as exc:
            logger.debug(f"{str(exc)}")
            logger.debug(f"Failed to hit {url} on attempt {attempt}")
            continue


def initial_api_call(records_per_call):
    url = f"{API_ENDPOINT}&limit={records_per_call}"
    data = hit_endpoint(url)
    total_results_count = data["total"]
    records = data["records"]
    return records, total_results_count


def remaining_api_calls(total_results_count, records_per_call, records):
    num_calls_left = math.ceil(total_results_count / records_per_call) - 1
    num_results_searched = records_per_call
    retries = 3
    status_forcelist = [status for status in list(HTTPStatus) if status >= 300]
    retry = Retry(
        total=retries,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)

    with FuturesSession() as session:
        session.mount("https://", adapter)
        futures = [
            session.get(
                f"{API_ENDPOINT}&limit={records_per_call}&offset={num_results_searched * i}"
            )
            for i in range(1, num_calls_left + 1)
        ]
        for future in as_completed(futures):
            try:
                response = future.result()
                records += response.json()["result"]["records"]
            except (RetryError, KeyError) as exc:
                logger.debug(f"{str(exc)}")
    return records


def gather_records():
    records_per_call = 10
    records, total_results_count = initial_api_call(records_per_call)
    records = remaining_api_calls(total_results_count, records_per_call, records)
    return records


def save_records(records):
    record_data = []
    for record in records:
        if record["Agent/Applicant"] == "Habitat Energy Limited":
            record_data.append(
                Record(
                    unique_bid_number=record["Unique bid number"],
                    accepted_or_rejected=record["Accepted/Rejected"],
                    delivery_date=datetime.datetime.strptime(
                        record["Delivery Date"], "%Y-%m-%d"
                    ),
                )
            )
    Record.objects.bulk_create(record_data, ignore_conflicts=True)
