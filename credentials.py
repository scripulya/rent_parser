import os

from dotenv import load_dotenv

load_dotenv('.env')

DB_CREDENTIALS = {
    'host': os.environ.get('POSTGRES_HOST'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'user': os.environ.get('POSTGRES_USER'),
    'port': os.environ.get('POSTGRES_PORT'),
    'database': os.environ.get('POSTGRES_DATABASE')
}

HERE_ACCESS_TOKEN = os.environ.get('HERE_ACCESS_TOKEN')
HERE_GRANT_TYPE = os.environ.get('HERE_GRANT_TYPE')
HERE_CLIENT_SECRET = os.environ.get('HERE_CLIENT_SECRET')
HERE_CLIENT_ID = os.environ.get('HERE_CLIENT_ID')
