import scrapy
import re

class BizSpider(scrapy.Spider):

    name = 'findbiz'

    start_urls = [
        'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'
    ]

    headers = {
        'Origin': 'https://findbiz.nat.gov.tw',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1'
    }
    
    body = "qryCond=台積電&fhl=zh_TW&infoType=D&qryType=cmpyType&cmpyType=true&brCmpyType=&busmType=&factType=&lmtdType=&isAlive=all&busiItemMain=&busiItemSub=&sugCont=&sugEmail=&g-recaptcha-response="

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                method='POST',
                headers=self.headers,
                body=self.body,
                callback=self.parse
            )

    def parse(self, response):
        filename = f'temp.txt'
        f = open(filename, 'w')
        panels = response.css('div.panel.panel-default')
        for p in panels:
            comp_data = p.xpath('.//div')
            comp_name = comp_data[0]
            comp_attr = comp_data[1].xpath('text()')[0].get()
            merged_comp_name = ''.join(comp_name.css('::text').getall())
            
            comp_attr = re.sub(r'\t|\r|\n|\xa0', '', comp_attr).split(',')
            f.write(merged_comp_name)
            f.write('\n')
            f.write('\n'.join(comp_attr))
            f.write('\n')
        
        self.log(f'Saved file {filename}')