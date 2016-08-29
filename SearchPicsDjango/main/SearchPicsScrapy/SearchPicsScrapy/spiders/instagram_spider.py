import scrapy
import psycopg2
import random
from scrapy.shell import inspect_response


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]

    def __init__(self, search='asd'):
        print("INIT", search)
        super(InstagramSpider, self).__init__()
        self.search_phrase = search

        self.start_urls = (
            'https://www.instagram.com/explore/tags/' + search,
        )

        # if not self.check_search():
        #     self.start_urls = (
        #         'https://yandex.ua/images/search?text='+search,
        #     )
        # else:
        #     self.start_urls =()

    def check_search(self):
        try:
            con = psycopg2.connect(database='spiderdb', user='kira')
            cur = con.cursor()
            cur.execute("SELECT * FROM search_query;")
            search_query = cur.fetchall()
            for item in search_query:
                if item[1] == self.search_phrase:
                    return True
            return False

        except:
            print("Check search errror")
            return False


    def parse(self, response):
        print("PARSE")
        inspect_response(response, self)
        images_list = response.xpath("/div")
        print(images_list)
        links=''
        for link in links:
            img = link.xpath("./img")
            try:
                link = link.extract()
                link = link.split('src="')[1]
                link = link.split('" onerror=')[0]
            except:
               print("ERROR KEY!", link)
            try:
                img = img.extract()

            except:
                print("ERROR VAL!", link)
            print(link, link)
            #yield {link:link}


    def start_requests(self):
        print("START_REQ")
        for url in self.start_urls:
            headers = {}
            headers['User-Agent'] = str(random.randint(0,255))
#        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            yield scrapy.Request(url, headers=headers, dont_filter=True)