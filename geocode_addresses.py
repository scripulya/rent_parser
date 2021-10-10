import logging

import requests
import psycopg2
from tqdm import tqdm

from credentials import (
    DB_CREDENTIALS,
    HERE_ACCESS_TOKEN,
    HERE_CLIENT_ID,
    HERE_CLIENT_SECRET,
    HERE_GRANT_TYPE)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

connection = psycopg2.connect(**DB_CREDENTIALS)
cursor = connection.cursor()

addresses = cursor.execute('SELECT address FROM real_estates;')
addresses = cursor.fetchall()

HERE_URL = 'https://geocode.search.hereapi.com/v1/geocode'

basic_form = {
    'grant_type': HERE_GRANT_TYPE,
    'client_id': HERE_CLIENT_ID,
    'client_secret': HERE_CLIENT_SECRET,
}

headers = {
    'Authorization': f'Bearer {HERE_ACCESS_TOKEN}'
}


def geocode_addresses():
    locations = []
    logger.info("Geocoding process started")
    for i, address in enumerate(tqdm(addresses)):
        address = address[0]
        params = {'q': address}
        response = requests.get(
            HERE_URL, headers=headers,
            data=basic_form, params=params)

        response = response.json()
        locations.append((response['items'], address))
    return locations


def update_addresses_with_coords(locations_collections):
    for collection, address in tqdm(locations_collections):
        if collection != []:
            logger.info(address)
            collection = sorted(
                collection,
                key=lambda x: x['scoring']['queryScore'],
                reverse=True)
            collection = collection[0]
            lat = collection['position']['lat']
            lng = collection['position']['lng']
            logger.info({'lng': lng, 'lat': lat})
            point = f"ST_GeomFromText('POINT({lng} {lat})', 4326)"
            condition = f"WHERE address = '{address}'"
            cursor.execute(f"UPDATE real_estates SET coords = {point} {condition};")

    connection.commit()


if __name__ == '__main__':
    locations = geocode_addresses()
    update_addresses_with_coords(locations)
