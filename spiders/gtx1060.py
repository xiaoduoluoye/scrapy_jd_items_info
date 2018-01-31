# -*- coding: utf-8 -*-
import scrapy
from jingdong_GTX1060.items import JingdongGtx1060Item
import urllib2
import json
import re
import sys


class Gtx1060Spider(scrapy.Spider):
    name = 'gtx1060'
    reload(sys)
    sys.setdefaultencoding("utf8")
    allowed_domains = ['search.jd.com']
    # start_urls = ['https://item.jd.com/3350660.html']
    basic_urls = ['https://search.jd.com/Search?keyword=gtx1060&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=6.his.0.0&page=']
    offset = 1
    start_urls = [basic_urls[0] + str(offset)]
    def parse(self, response):
        # node_list = response.xpath("//div[@class='gl-i-wrap']")
        id_list = response.xpath("//div[@id='J_goodsList' and @class='goods-list-v2 gl-type-1 J-goods-list']/ul[1]/li/@data-sku").extract()

        for item_id in id_list:
            item = JingdongGtx1060Item()
            # import ipdb; ipdb.set_trace()
            #获取产品链接
            # item_id = node.extract().encode("utf-8")
            item_url = "https://item.jd.com/" + item_id + ".html"
            item['item_url'] = item_url

            yield scrapy.Request(item_url, meta={'item':item}, callback=self.parse_details, dont_filter=True)

        # import ipdb; ipdb.set_trace()
        # whether_next_page = response.xpath("//a[@class='pn-next']/@href").extract()
        if self.offset<=9:
            # import ipdb; ipdb.set_trace()
            self.offset += 1
            yield scrapy.Request(self.basic_urls[0] + str(self.offset), callback=self.parse, dont_filter=True)

            # name1 = node.xpath("./div[@class='p-name p-name-type-2']/a/em/text()").extract()[0].encode("utf-8")
            # name2 = node.xpath("./div[@class='p-name p-name-type-2']/a/em/font/text()").extract()[0].encode("utf-8")
            # name3 = node.xpath("./div[@class='p-name p-name-type-2']/a/em/text()").extract()[1].encode("utf-8")
            # item['item_name'] = name1 + name2 + name3
            #
            # pre_url = node.xpath("./div[@class='p-name p-name-type-2']/a[@target='_blank']/@href").extract()[0].encode("utf-8")
            # item['item_url'] = pre_url if "http" in pre_url else ("http." + pre_url)
            #
            # item_id = pre_url.split('/')[-1].strip('.html')
            # price_url = "https://p.3.cn/prices/mgets?callback=jQuery1861715&type=1&area=4_48205_52493_0&pdtk=&pduid=1502979112936703030929&pdpin=13663078-352235&pin=13663078-352235&pdbp=0&skuIds=J_"+ item_id +"&ext=11000000&source=item-pc"
            # price = urllib2.urlopen(price_url).read()
            # item['item_price'] = price.split('"')[-2]
            # # sku = item['item_url'].split('/')[-1].strip(".html")
            # # price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
            # # response = urllib2.urlopen(price_url)
            # # content = response.read()
            # # result = json.loads(content)[0]
            # # item['item_price'] = result['p']
            #
            # item['item_haveornot'] = node.xpath("./div[@class='p-stock']/text()").extract()[0].encode("utf-8")
            # yield item

    def parse_details(self, response):
        # item_detal = response.xpath("//")

        item = response.meta['item']
        #获取产品名称
        item['item_name'] = response.xpath("//div[@class='sku-name']/text()").extract()[0].encode("utf-8")
        # import ipdb; ipdb.set_trace()
        #获取产品价格
        item_id = item['item_url'].split('/')[-1].strip('.html')
        price_url = "https://p.3.cn/prices/mgets?callback=jQuery1861715&type=1&area=4_48205_52493_0&pdtk=&pduid=1502979112936703030929&pdpin=13663078-352235&pin=13663078-352235&pdbp=0&skuIds=J_"+ item_id +"&ext=11000000&source=item-pc"
        price = urllib2.urlopen(price_url).read()
        item['item_price'] = price.split('"')[-2]

        #获取店家信息、获取产品是否有货（重庆地区）
        detail_url = "https://c0.3.cn/stock?skuId=" + item_id + "&area=4_48205_52493_0&venderId=1000080223&cat=670,677,679&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}&ch=1&fqsp=0&pduid=1502979112936703030929&pdpin=13663078-352235&detailedAdd=null&callback=jQuery8447360"

        stock_detail = urllib2.urlopen(detail_url).read()

        # import ipdb; ipdb.set_trace()
        # item['item_shopinfo'] = re.findall(r'(?<=vender":").*?(?=")', stock_detail)[0]
        # item['item_haveornot'] = re.findall(r'(?<=<strong>).*?(?=</strong>)', stock_detail)[0]
        item['item_shopinfo'] = re.findall(r'(?<=vender":").*?(?=")', stock_detail)[0].decode("GB18030")
        item['item_haveornot'] = re.findall(r'(?<=<strong>).*?(?=</strong>)', stock_detail)[0].decode("GB18030")
        yield item
