from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import ApartmentItem


class AloNhadatSpider(Spider):
    name = 'AloNhadatspider'
    # allowed_domains = ['https://batdongsan.com.vn/']

    def start_requests(self):
        # start_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi'
        start_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi"
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }
        for i in range(1, 30):
            yield Request(url=start_url + '/trang--' + str(i)+ '.html',
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

    # def parse_link(self, response):
    #     # base_url = 'https://batdongsan.com.vn'
    #     # apartment_links = response.xpath('//*[@id="product-lists-web"]/div/a')
    #     apartment_links = response.xpath('//*[@id="list-property-box"]/div/div[1]/div[1]/a')

    #     yield from response.follow_all(apartment_links, callback=self.parse_features)
            


            
    def parse_link(self, response):
        apartment_links = response.xpath('//div[@class="ct_title"]/a/@href').getall()

        self.logger.info(f"Found {len(apartment_links)} apartment links")
        yield from response.follow_all(apartment_links, callback=self.parse_features)

    def parse_features(self, response):
        l = ItemLoader(item=ApartmentItem(), response=response)

        l.add_value('url', response.url)
        l.add_xpath('title', '//*[@id="left"]/div[1]/div[1]/h1/text()')
        # l.add_xpath('short_detail', '//*[@id="left"]/div[1]/div[2]/text()')
        l.add_xpath('price', '//*[@id="left"]/div[1]/div[3]/span[1][contains(span[1]/text(), "Giá")]/span[2]/text()')
        l.add_xpath('area', '//*[@id="left"]/div[1]/div[3]/span[2][contains(span[1]/text(), "Diện tích")]/span[2]/text()')
        l.add_xpath('type', '//tr[td[contains(text(),"Loại")]]/td[2]/text()')

        l.add_xpath('bedrooms', '//tr[td[contains(text(),"Số phòng ngủ")]]/td[4]/text()')
        # l.add_xpath('bathrooms', '')
        l.add_xpath('address', '//*[@id="left"]/div[1]/div[4][contains(span[1]/text(), "Địa chỉ")]/span[2]/text()')
        l.add_xpath('direction', '//tr[td[contains(text(),"Hướng")]]/td[4]/text()')
        l.add_xpath('floor', '//tr[td[contains(text(),"Số lầu")]]/td[4]/text()')
        # l.add_xpath('balcony_direction', '')
        l.add_xpath('kitchen', '//tr[td[contains(text(),"Bếp")]]/td[6]/text()')
        l.add_value('kitchen', "available")

        l.add_xpath('law_doc', '//tr[td[contains(text(),"Pháp lý")]]/td[4]/text()')

        l.add_xpath('parking_lot', '//tr[td[contains(text(),"xe hơi")]]/td[6]/text()')
        l.add_value('parking_lot', 'available')
        
        l.add_xpath('terrace', '//tr[td[contains(text(),"Sân thượng")]]/td[6]/text()')
        l.add_value('terrace', 'available')

        l.add_xpath('project', '//tr[td[contains(text(),"Dự án")]]/td[2]/span/a/text()')
        l.add_value('project', 'available')

        l.add_xpath('post_date', '//*[@id="left"]/div[1]/div[1]/span/text()')
        l.add_xpath('id', '//tr[td[contains(text(),"Mã")]]/td[2]/text()')

        yield l.load_item()
