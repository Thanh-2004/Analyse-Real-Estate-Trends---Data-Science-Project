from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import ApartmentItem
from twocaptcha import TwoCaptcha
from urllib.parse import urlencode, quote_plus



class TownHouseReverSpider(Spider):
    name = 'TownHouseReverspider'
    # allowed_domains = ['https://batdongsan.com.vn/']

    # def start_requests(self):
    #     start_url = ["https://sosanhnha.com/search?iCat=324&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  ## Chung cư
    #                  "https://sosanhnha.com/search?iCat=41&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",   ## Nhà riêng
    #                  "https://sosanhnha.com/search?iCat=325&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  ## Biệt thự
    #                  "https://sosanhnha.com/search?iCat=163&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  ## Nhà mặt phố
    #                     ]
    #     headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    #     }
    #     for i in range(1, 30):
    #         yield Request(url=start_url + str(i),
    #                         callback=self.parse_link,
    #                         headers=headers
    #                     )

            
    def start_requests(self):
        # start_urls = [
        #     "https://sosanhnha.com/search?iCat=324&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  # Chung cư
        #     "https://sosanhnha.com/search?iCat=41&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",   # Nhà riêng
        #     "https://sosanhnha.com/search?iCat=325&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  # Biệt thự
        #     "https://sosanhnha.com/search?iCat=163&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page=",  # Nhà mặt phố
        # ]
        start_urls = ["https://rever.vn/s/ho-chi-minh/mua/nha-pho?page="]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }

        for url in start_urls:
            for i in range(1, 201):
                full_url = url + str(i)  
                yield Request(
                    url=full_url,
                    callback=self.parse_link,
                    headers=headers
                )

        # # one page
        # url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-hoang-cau-phuong-o-cho-dua-prj-d-le-pont-dor-hoang-cau/chinh-chu-ban-gap-tai-du-an-tan-ang-minh-36-ang-98m2-2pn-gia-4-8-ty-lh-0975357268-pr26919881'
        # # url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-5-xa-dong-hoi-prj-eurowindow-river-park/chi-23-7tr-m2-91m2-3pn-2vs-full-noi-that-co-ban-view-nam-h-long-bien-pr28106294'
        # yield Request(url=url, callback=self.parse_features)

    # def start_requests(self):
    # # Đây là proxy từ Free Proxy List
    #     proxy = "http://3076a7ba298e91a89c11c6eec6d0650f4c3ce975:@api.zenrows.com:8001"
        
    #     # URL trang cần crawl
    #     start_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi'

    #     # Lặp qua các trang cần crawl
    #     for i in range(1, 10):
    #         yield Request(
    #             url=start_url + '/p' + str(i), 
    #             callback=self.parse_link,
    #             meta={'proxy': proxy}  # Thêm proxy vào meta
    #         )


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

        l.add_xpath('land_area', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[5]/p[2]/text()')
        l.add_value('land_area', "KXĐ")

        l.add_xpath('floor_area', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[7]/p[2]/text()')
        l.add_value('floor_area', "KXĐ")
        
        l.add_xpath('type', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[1]/p[2]/a/text()')

        l.add_xpath('bedrooms', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[2]/p[2]/a/text()')
        l.add_value('bedrooms', "KXĐ")

        l.add_xpath('bathrooms', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[3]/p[2]/text()')
        l.add_value('bathrooms', "KXĐ")

        l.add_xpath('address', '//div[@class="address"]/p/a/text()')
        
        l.add_xpath('direction', '//*[@id="wrap"]/section[1]/div/div[1]/div[1]/header/div[3]/ul/li[5]/text()')
        l.add_value("direction", 'KXĐ')

        l.add_xpath('floor', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[4]/p[2]/text()')
        l.add_value("floor", "KXĐ")

        # l.add_xpath('kitchen', '//tr[td[contains(text(),"Bếp")]]/td[6]/text()')
        # l.add_value('kitchen', "available")

        l.add_xpath('law_doc', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[9]/p[2]/text()')
        l.add_value('law_doc', "KXĐ")

        l.add_xpath('furniture', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[8]/p[2]/text()')
        l.add_value('furniture', "KXĐ")

        # l.add_xpath('parking_lot', '//tr[td[contains(text(),"xe hơi")]]/td[6]/text()')
        # l.add_value('parking_lot', 'available')
        
        # l.add_xpath('terrace', '//tr[td[contains(text(),"Sân thượng")]]/td[6]/text()')
        # l.add_value('terrace', 'available')

        # l.add_xpath("entrance", '//div[div[contains(text(),"Đường vào :")]]/div[2]/text()')
        # l.add_value("entrance",  "KXĐ")

        l.add_xpath('utilities', '//*[@id="details-amenities"]/ul/li/text()')
        l.add_value('utilities', ' ')

        # l.add_xpath('project', '//*[@id="wrap"]/section[1]/div/div[1]/div[5]/ul/li[8]/p[2]/a/text()')
        # l.add_value('project', 'KXĐ')

        l.add_xpath('post_date', '//div[@class="listing-date-updated"]/strong/text()')
        l.add_xpath('id', '//div[@class="listing-id"]/strong/text()')

        yield l.load_item()
