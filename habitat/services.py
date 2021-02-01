import datetime
import logging
import math

import requests
from django.db import IntegrityError

from habitat.models import Record

logger = logging.getLogger(__name__)


def get_habitat_records():
    records_limit_per_call = 10
    url = f"https://data.nationalgrideso.com/api/3/action/datastore_search?resource_id=e3e44433-7614-4c8c-9cbc-7808994d3a72&limit={records_limit_per_call}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["result"]
    total_results = data["total"]
    records = data["records"]

    num_calls_left = math.ceil(total_results / records_limit_per_call) - 1
    num_results_searched = records_limit_per_call
    for i in range(num_calls_left):
        url = f"https://data.nationalgrideso.com/api/3/action/datastore_search?resource_id=e3e44433-7614-4c8c-9cbc-7808994d3a72&limit={records_limit_per_call}&offset={num_results_searched}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["result"]
        records += data["records"]
        num_results_searched += records_limit_per_call

    save_records(records)
    return Record.objects.all()


def save_records(records):
    for record in records:
        if record["Agent/Applicant"] == "Habitat Energy Limited":
            record_data = Record(
                unique_bid_number=record["Unique bid number"],
                accepted_or_rejected=record["Accepted/Rejected"],
                delivery_date=datetime.datetime.strptime(
                    record["Delivery Date"], "%Y-%m-%d"
                ),
            )
            try:
                record_data.save()
            except IntegrityError:
                logger.error(
                    "Couldn't save record. A record with the same bid number likely already exists"
                )
