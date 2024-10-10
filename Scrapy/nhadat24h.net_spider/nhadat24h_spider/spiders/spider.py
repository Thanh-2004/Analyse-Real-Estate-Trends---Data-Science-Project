from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import ApartmentItem
from twocaptcha import TwoCaptcha
from urllib.parse import urlencode, quote_plus


def ZenRows_api_url(url, api_key):

    # set ZenRows request parameters
    params = {
            "apikey": api_key, 
            "url": url, 
            "js_render":"true", 
            "premium_proxy":"true",
            } 
    # encode the parameters and merge it with the ZenRows base URL
    encoded_params = urlencode(params, quote_via=quote_plus)

    final_url = f"https://api.zenrows.com/v1/?{encoded_params}"

    return final_url


class SosanhSpider(Spider):
    name = 'SosanhNhaspider'
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
        start_urls = ["https://sosanhnha.com/search?iCat=0&iCitId=0&iDisId=0&iWardId=0&iPrice=0&keyword=&page="]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }

        for url in start_urls:
            for i in range(1, 1001):
                full_url = url + str(i)  
                # api_url = ZenRows_api_url(full_url, "3076a7ba298e91a89c11c6eec6d0650f4c3ce975")
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
        apartment_links = response.xpath('//div[@class="info"]/h3/a/@href').getall()

        self.logger.info(f"Found {len(apartment_links)} apartment links")
        yield from response.follow_all(apartment_links, callback=self.parse_features)

    def parse_features(self, response):
        l = ItemLoader(item=ApartmentItem(), response=response)

        l.add_value('url', response.url)
        l.add_xpath('title', '//h1[@class="title"]/text()')
        l.add_xpath('description', '//article[@class="description"]/text()')

        l.add_xpath('price', '//div[div[contains(text(),"Giá :")]]/div[2]/text()')
        l.add_value('price', "KXĐ")

        l.add_xpath('area', '//div[div[contains(text(),"Diện tích :")]]/div[2]/text()')
        l.add_value('area', "KXĐ")
        
        l.add_xpath('type', '//span[@itemprop="name"]/text()')

        l.add_xpath('bedrooms', '//div[div[contains(text(),"Phòng ngủ :")]]/div[2]/text()')
        l.add_value('bedrooms', "KXĐ")

        l.add_xpath('bathrooms', '//div[div[contains(text(),"Phòng tắm :")]]/div[2]/text()')
        l.add_value('bathrooms', "KXĐ")

        l.add_xpath('address', '//div[@class="cla-main-info"]/div[@class="address"]/text()')
        
        l.add_xpath('direction', '//div[div[contains(text(),"Hướng nhà :")]]/div[2]/text()')
        l.add_value("direction", 'KXĐ')

        l.add_xpath('floor', '//div[div[contains(text(),"Số tầng :")]]/div[2]/text()')
        l.add_value("floor", "KXĐ")

        # l.add_xpath('kitchen', '//tr[td[contains(text(),"Bếp")]]/td[6]/text()')
        # l.add_value('kitchen', "available")

        l.add_xpath('law_doc', '//div[div[contains(text(),"Pháp lý :")]]/div[2]/text()')
        l.add_value('law_doc', "KXĐ")

        # l.add_xpath('parking_lot', '//tr[td[contains(text(),"xe hơi")]]/td[6]/text()')
        # l.add_value('parking_lot', 'available')
        
        # l.add_xpath('terrace', '//tr[td[contains(text(),"Sân thượng")]]/td[6]/text()')
        # l.add_value('terrace', 'available')

        l.add_xpath("entrance", '//div[div[contains(text(),"Đường vào :")]]/div[2]/text()')
        l.add_value("entrance",  "KXĐ")

        l.add_xpath('project', '//p[@class="project"]/b[1]/a[1]/text()')
        l.add_value('project', 'KXĐ')

        l.add_xpath('post_date', '//div[div[contains(text(), "Ngày")]]/div[2]/text()')
        l.add_xpath('id', '//div[div[contains(text(), "Mã tin")]]/div[2]/text()')

        yield l.load_item()
