from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import ApartmentItem



class ReverSpider(Spider):
    name = 'Reverspider'
            
    def start_requests(self):

        start_urls = ["https://rever.vn/s/ho-chi-minh/mua/studio-flat?page=", 
                      "https://rever.vn/s/ho-chi-minh/mua/can-ho?page="]   ## page = {1, 6}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }

        for url in start_urls:
            for i in range(1, 282):
                full_url = url + str(i)  
                yield Request(
                    url=full_url,
                    callback=self.parse_link,
                    headers=headers
                )


    def parse_link(self, response):
        apartment_links = response.xpath('//a[@class="listing-price-link"]/@href').getall()

        self.logger.info(f"Found {len(apartment_links)} apartment links")
        yield from response.follow_all(apartment_links, callback=self.parse_features)

    def parse_features(self, response):
        l = ItemLoader(item=ApartmentItem(), response=response)

        l.add_value('url', response.url)
        l.add_xpath('title', '//header[@class="detail-house"]/h1/text()')
        # l.add_xpath('description', '//p[@class="summary"]/text()')

        l.add_xpath('price', '//div[@class="listing-detail-price-cost"]/strong/text()')
        l.add_value('price', "KXĐ")

        l.add_xpath('price_per_area', '//div[@class="listing-detail-price-cost"]/span/text()')
        l.add_value('price_per_area', "KXĐ")

        l.add_xpath('area', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[4]/p[2]/text()')
        l.add_value('area', "KXĐ")
        
        l.add_xpath('type', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[1]/p[2]/a/text()')

        l.add_xpath('bedrooms', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[2]/p[2]/a/text()')
        l.add_value('bedrooms', "KXĐ")

        l.add_xpath('bathrooms', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[3]/p[2]/text()')
        l.add_value('bathrooms', "KXĐ")

        l.add_xpath('address', '//div[@class="address"]/p/a/text()')
        
        l.add_xpath('direction', '//*[@id="wrap"]/section[1]/div/div[1]/div[1]/header/div[3]/ul/li[5]/text()')
        l.add_value("direction", 'KXĐ')

        # l.add_xpath('floor', '//div[div[contains(text(),"Số tầng :")]]/div[2]/text()')
        # l.add_value("floor", "KXĐ")

        # l.add_xpath('kitchen', '//tr[td[contains(text(),"Bếp")]]/td[6]/text()')
        # l.add_value('kitchen', "available")

        l.add_xpath('law_doc', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[6]/p[2]/text()')
        l.add_value('law_doc', "KXĐ")

        l.add_xpath('furniture', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[5]/p[2]/text()')
        l.add_value('furniture', "KXĐ")

        # l.add_xpath('parking_lot', '//tr[td[contains(text(),"xe hơi")]]/td[6]/text()')
        # l.add_value('parking_lot', 'available')
        
        # l.add_xpath('terrace', '//tr[td[contains(text(),"Sân thượng")]]/td[6]/text()')
        # l.add_value('terrace', 'available')

        # l.add_xpath("entrance", '//div[div[contains(text(),"Đường vào :")]]/div[2]/text()')
        # l.add_value("entrance",  "KXĐ")

        l.add_xpath('utilities', '//*[@id="details-amenities"]/ul/li/text()')
        l.add_value('utilities', ' ')

        l.add_xpath('project', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[8]/p[2]/a/text()')
        l.add_value('project', 'KXĐ')

        l.add_xpath('post_date', '//div[@class="listing-date-updated"]/strong/text()')
        l.add_xpath('id', '//div[@class="listing-id"]/strong/text()')

        yield l.load_item()
