import scrapy
from unsplash_scraper.items import UnsplashImageItem

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/t/']

    def parse(self, response):
        category_urls = response.css('a.FNhv9::attr(href)').getall()
        self.log(f'Found categories: {category_urls}')
        for url in category_urls:
            yield response.follow(url, self.parse_category)

    def parse_category(self, response):
        image_page_urls = response.css('a.cV68d::attr(href)').getall()
        category = response.url.split('/')[-1]
        self.log(f'Found images in category {category}: {image_page_urls}')
        for url in image_page_urls:
            yield response.follow(url, self.parse_image, meta={'category': category})

        next_page = response.css('a[data-test="pagination-next"]::attr(href)').get()
        if next_page:
            self.log(f'Following next page: {next_page}')
            yield response.follow(next_page, self.parse_category)

    def parse_image(self, response):
        item = UnsplashImageItem()
        item['image_urls'] = [response.css('img._2zEKz::attr(src)').get()]
        item['image_name'] = response.css('h1._2yFK-::text').get()
        item['category'] = response.meta['category']
        self.log(f'Scraped image: {item}')
        yield item
