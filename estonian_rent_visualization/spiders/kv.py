import scrapy
from estonian_rent_visualization.spiders.xpath_descriptors import (
    KV_EE_ADDRESS_DESCRIPTOR
)

BASE_URL = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&deal_type=2&dt_select=2&search_type=old&page='


class KvSpider(scrapy.Spider):
    name = 'kv'

    def start_requests(self):
        urls = [BASE_URL]
        urls += [BASE_URL + f"&page={i}" for i in range(2, 35)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        addresses = response.xpath(KV_EE_ADDRESS_DESCRIPTOR).extract()
        for addr in addresses:
            addr = addr.replace('  ', '')
            addr = addr.replace('\n', '')
            yield {'address': addr}
