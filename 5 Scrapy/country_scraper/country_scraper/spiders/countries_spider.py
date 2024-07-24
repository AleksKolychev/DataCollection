import scrapy


class CountriesSpiderSpider(scrapy.Spider):
    name = "countries_spider"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://tradingeconomics.com/country-list/inflation-rate?continent=world"]


    def parse(self, response):
        rows = response.xpath('//td/a')
        for row in rows:
            country_name = row.xpath('.//text()').get().strip()
            link = row.xpath('.//@href').get()
            yield response.follow(url=link, callback=self.parse_country, meta={
                'country_name': country_name
            })


    def parse_country(self, response):
        rows = response.xpath("//tr[contains(@class, 'datatable')]")
        for row in rows:
            country_name = response.request.meta['country_name']
            related = row.xpath('.//td[1]/a/text()').get().strip()
            last_value = row.xpath('.//td[2]/text()').get()
            previous_value = row.xpath('.//td[3]/text()').get()
            reference = row.xpath('.//td[5]/text()').get().strip()
            unit = row.xpath('.//td[4]/text()').get().strip()
            yield{
                'country_name': country_name,
                'related': related,
                'last_value': last_value,
                'previous_value': previous_value,
                'reference': reference,
                'unit': unit
            }    
            