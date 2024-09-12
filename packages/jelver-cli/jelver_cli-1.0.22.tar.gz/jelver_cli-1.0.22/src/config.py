import os

DOMAIN = os.getenv('DOMAIN', 'jelver.com')
API_HOST = f'https://api.{DOMAIN}'
APP_HOST = f'https://app.{DOMAIN}'
