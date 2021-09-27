import scrapy
from estonian_rent_visualization.spiders.xpath_descriptors import (
    ADDRESS_DESCRIPTOR
)


class City24Spider(scrapy.Spider):
    name = 'city24'
    allowed_domains = ['city24.ee']

    def start_requests(self):
        # urls = ['https://www.city24.ee/en/list/rent/apartments']
        base_url = 'https://www.city24.ee/en/list?fr='
        urls = [base_url + str(i) for i in range(23)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        addresses: list = response.xpath(ADDRESS_DESCRIPTOR).extract()

        for address in addresses:
            data = {"address": address}
            yield data
