from django.shortcuts import render
from django.views.generic import TemplateView

from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.signalmanager import SignalManager
from scrapy.utils.project import get_project_settings
from billiard import Process

from .tasks import start_google_spider
import psycopg2

from .SearchPicsScrapy.SearchPicsScrapy.spiders.google_spider import GoogleSpider

# class UrlCrawlerScript(Process):
#     def __init__(self, spider):
#         Process.__init__(self)
#         settings = get_project_settings()
#         self.crawler = Crawler(settings)
#         #self.crawler.configure()
#         self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#         self.spider = spider
#
#     def run(self):
#         self.crawler.crawl(self.spider)
#         self.crawler.start()
#         reactor.run()
#
# def run_spider(search):
#     spider = GoogleSpider(search)
#     crawler = UrlCrawlerScript(spider)
#     crawler.start()
#     crawler.join()


class SearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        print("search")
        print(kwargs['phrase'])
        con = psycopg2.connect(database='spiderdb', user='kira')
        cur = con.cursor()
        cur.execute("SELECT picture FROM search_query WHERE phrase='"+kwargs['phrase']+"';")
        pic_nums = cur.fetchall()
        pic_nums = [num[0] for num in pic_nums]
        pics = []
        for num in pic_nums:
            cur.execute("SELECT * from picture WHERE id="+str(num)+";")
            pics.append(cur.fetchone())
        res_pics=[]
        for i in (range(0, int(len(pics)/2))):
            res_pics.append(pics[i])
            res_pics.append(pics[i+5])
        return render(request, 'search.html', {'pics':res_pics})

class MainView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        con = psycopg2.connect(database='spiderdb', user='kira')
        cur = con.cursor()
        #cur.execute("SELECT phrase FROM search_query;")
        #search_query = cur.fetchall()
        cur.execute("SELECT DISTINCT phrase FROM search_query;")
        names = cur.fetchall()
        print(names)

        names = [name[0] for name in names]
        # if request.POST['search'] not in names:
        #     start_google_spider.apply_async(args=((request.POST['search']),))
        #     cur.execute("SELECT DISTINCT phrase FROM search_query;")
        #     names = cur.fetchall()

        con.close()
        return render(request, 'index.html', {'names':names})

    def get(self, request, *args, **kwargs):
        con = psycopg2.connect(database='spiderdb', user='kira')
        cur = con.cursor()
        cur.execute("SELECT * FROM search_query;")
        search_query = cur.fetchall()
        cur.execute("SELECT DISTINCT phrase FROM search_query;")
        names = cur.fetchall()
        print(names)
        con.close()
        names = [name[0] for name in names]
        return render(request, 'index.html', {'names':names})
        # process = CrawlerRunner({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })
        #
        # process.crawl(GoogleSpider)
        # process.start()
        #

  #      configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
  #      crawler = Crawler(GoogleSpider('cat'), Settings())
  #      runner = CrawlerRunner(Settings())

        #runner.spider = GoogleSpider('cat')
        #runner.signals.connect()

  #      d = runner.crawl(crawler)
       # d.addBoth(lambda _: reactor.stop())
       # reactor.run()

       # from scrapy.cmdline import execute
       # execute(["scrapy", "runspider", "/home/kira/PycharmProjects/SearchPics/SearchPicsDjango/SearchPicsScrapy/SearchPicsScrapy/spiders/google_spider.py"])


        # dispatcher.connect(reactor.stop, signal=signals.spider_closed)
        # spider = GoogleSpider("asd")
        # crawler = Crawler()
        # crawler.configure()
        # crawler.crawl(spider)
        # crawler.start()
        # log.start()
        # log.msg('Running reactor...')
        # reactor.run()  # the script will block here until the spider is closed
        # log.msg('Reactor stopped.')
        # from scrapy.cmdline import execute
        # execute(['cd', 'SearchPicsDjango/SearchPicsScrapy/'])
        # execute(['scrapy', 'crawl', 'google'])
        #cmdline.execute("scrapy runspider SearchPicsScrapy/SearchPicsScrapy/spiders/google_spider.py")
        # spider = GoogleSpider(search="asd")
        # settings = get_project_settings()
        # crawler = Crawler(spider,settings)
        # crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        # #crawler.configure()
        # #crawler.crawl(spider)
        # crawler.start()
        # log.start()
        # reactor.run()
