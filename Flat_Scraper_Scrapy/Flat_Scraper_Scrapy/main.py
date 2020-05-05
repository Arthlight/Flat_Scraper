from time import sleep
import subprocess
import requests

# Timeout is measured in seconds
TIMEOUT = 60

while True:
    command = 'scrapy crawl ImmobilienScout'
    subprocess.run(command, shell=True)
    requests.put('http://localhost:2000/api/primer/')
    sleep(TIMEOUT * 60) # sleep for 1 hours #TODO: Change this to 1 month when production ready
