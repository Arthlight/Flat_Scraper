from time import sleep
import subprocess

# Timeout is measured in seconds
TIMEOUT = 60

while True:
    print('IT WORKED YAY')
    command = 'scrapy crawl ImmobilienScout'
    subprocess.run(command, shell=True)
    sleep(TIMEOUT * 60) # sleep for 1 hour
