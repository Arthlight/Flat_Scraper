"""This module contains a Web Scraper and scrapes ImmobilienScout24.com.

This module's purpose is scraping ImmobilienScout24.com for flat data of
three different cities: Berlin, Hamburg, Munich. This data consists of
things such as price, location, room count and more. This is done via
this module's only class "ImmobilienScoutSpider", which relies on the
third party framework "Scrapy".


  Typical usage example (from command line):

  $ scrapy crawl ImmobilienScout
"""
# Standard library
import requests
import pickle

# Third party
import scrapy


class ImmobilienScoutSpider(scrapy.Spider):
    """Scrapes data from ImmobilienScout24.com.

       This class takes control of scraping
       data from a given website (or websites).
       It first loops through the start_urls
       attribute, sends a HTTP GET Request
       to every single one and passes on the
       received HTML-Document to the parse
       method. From here on the desired
       content gets extracted and sent to
       the HotspotHousing.com API.

       Attributes:
           name: The name of the Scraper as a string.
           start_urls: A list containing all the URLs that shall be scraped.
       """
    name = 'ImmobilienScout'

    # Defined in a list because then you don't need to implement a start_requests() method; If the start_urls class
    # attribute is defined scrapy will fall back to it automatically.
    start_urls = [
        'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?pagenumber=1',
        'https://www.immobilienscout24.de/Suche/de/bayern/muenchen/wohnung-mieten?pagenumber=1',
        'https://www.immobilienscout24.de/Suche/de/hamburg/hamburg/wohnung-mieten?pagenumber=1',
    ]

    def parse(self, response):
        all_flats = response.xpath('//div[@class="result-list-entry__data"]')

        for flatdata in all_flats:
            price = flatdata.xpath('.//dd[@class="font-nowrap font-highlight font-tabular"]/text()').get()
            address = flatdata.xpath('.//button[@title="Auf der Karte anzeigen"]/text()').get().split(', ')

            # If price is None we know this is not a normal listing, but a project still in progress or an ad so we
            # continue. If the length of the address is <= 2, we know we didn't get a street address and so ignore this
            # iteration.
            if price is None or len(address) <= 2:
                continue

            sqm = flatdata.xpath('.//dd[@class="font-nowrap font-highlight font-tabular"]/text()').getall()[1].split()[0]
            street = flatdata.xpath('.//button[@title="Auf der Karte anzeigen"]/text()').get().split(', ')[0].strip()
            area = flatdata.xpath('.//button[@title="Auf der Karte anzeigen"]/text()').get().split(', ')[1].split()[0]
            city = flatdata.xpath('.//button[@title="Auf der Karte anzeigen"]/text()').get().split(', ')[2]
            rooms = flatdata.xpath('.//span[@class="onlyLarge"]/text()').get()
            detail_view_url = (
                    'https://www.immobilienscout24.de/expose/' +
                    flatdata.xpath('.//button[@aria-label="zum Merkzettel hinzufügen"]/@data-id').get()
            )

            # Special case for price
            price = price.replace('€', '')
            price = price.replace('.', '')
            if ',' in price:
                price = price.split(',')[0]
            if int(price) < 1 or int(price) > 10000:
                continue

            # Special case for area:
            if any(char.isdigit() for char in area):
                continue

            # Special case for street:
            if ';' in street:
                street = street.split(';')[0]

            # Special case for sqm
            sqm = sqm.replace(',', '.')
            if float(sqm) < 1:
                continue

            data = {
                'price': price,
                'sqm': sqm,
                'street': street,
                'area': area,
                'city': city,
                'rooms': rooms,
                'detail_view': detail_view_url,
            }
            encoded_data = pickle.dumps(data)
            requests.post('http://localhost:8080/api/flatData/', encoded_data)

        next_page = response.xpath('//a[@data-nav-next-page="true"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)



