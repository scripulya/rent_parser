import json
import logging

import psycopg2
from tqdm import tqdm

from credentials import DB_CREDENTIALS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

connection = psycopg2.connect(**DB_CREDENTIALS)
cursor = connection.cursor()

QUERY = '''INSERT INTO municipality (name, geom) VALUES
    (%s, ST_Multi(ST_GeomFromGeoJSON(%s)))
'''


def load_municipalities(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        features = data['features']
        for feature in tqdm(features):
            properties = feature['properties']
            name = properties['ONIMI']
            geom = feature['geometry']
            cursor.execute(QUERY, (name, str(geom)))
        connection.commit()


if __name__ == '__main__':
    filepath = 'estonian_municipalities.geojson'
    load_municipalities(filepath)
