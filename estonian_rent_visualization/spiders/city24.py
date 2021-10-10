import scrapy
from estonian_rent_visualization.spiders.xpath_descriptors import (
    ADDRESS_DESCRIPTOR, CITY_24_PRICE_DESCRIPTOR, CITY_24_LINK_DESCRIPTOR
)


class City24Spider(scrapy.Spider):
    name = 'city24'
    allowed_domains = ['city24.ee']

    def start_requests(self):
        base_url = 'https://www.city24.ee/en/list/rent/apartments?ord=default&str=2&c=EE&usp=true&fr='
        urls = [base_url + str(i) for i in range(23)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        addresses: list = response.xpath(ADDRESS_DESCRIPTOR).extract()
        prices: list = response.xpath(CITY_24_PRICE_DESCRIPTOR).extract()
        links: list = response.xpath(CITY_24_LINK_DESCRIPTOR).extract()

        for address, price, link in zip(addresses, prices, links):
            data = {
                "address": address,
                "price": price,
                "link": link}
            yield data
