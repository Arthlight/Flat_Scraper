"""This script primes the Scraper and reruns it once a month.

This script runs the Scraper and sends a concluding PUT REQUEST
to the HotspotHousing API once the Scraper is finished. As soon
as HotspotHousing receives the PUT REQUEST, the flat data shown
on the maps will be updated. Hereafter this script will sleep
for one month until the same thing happens again.
"""
#standard library
from time import sleep
import subprocess
import requests

# Timeout is measured in seconds
TIMEOUT = 60

while True:
    try:
        requests.post('http://localhost:2000/api/before/')
    except Exception as error:
        print(error)
    else:
        command = 'scrapy crawl ImmobilienScout'
        subprocess.run(command, shell=True)
        try:
            requests.post('http://localhost:2000/api/after/')
        except Exception as error:
            print(error)
        sleep(TIMEOUT * 60000) # sleep for 1 hours #TODO: Change this to 1 month when production ready
