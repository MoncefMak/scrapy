import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'jumia'
    allowed_domains = ['www.jumia.dz']

    def start_requests(self):
        yield scrapy.Request(url="https://www.jumia.dz/stockage/")

    def parse(self, response):
        total_pages = response.xpath('//*[@class="pg-w -ptm -pbxl"]/a[last()-2]/text()').get()
        current_page = response.xpath('//*[@class="pg _act"]/text()').get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for i in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://www.jumia.dz/stockage/page={i}')

        for result in response.css('article.prd._fb.col.c-prd'):
            items = {
                'produit': result.css('h3.name::text').get(),
                'prix' : result.css('div.prc::text').get(),
            }
            yield items
